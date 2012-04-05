DROP TABLE units2010;
DROP SEQUENCE units2010_id_seq;

CREATE SEQUENCE units2010_id_seq;

CREATE TABLE units2010 (
	unit_id integer NOT NULL DEFAULT nextval('units2010_id_seq'::regclass), -- PK
	building_id integer, --FK
	unit_sqft real, --this should be integer but need approximation 
	sale_price integer, --I don't know why this is stored as text
	rent integer, --?
	story integer,
	bedrooms integer
); 

DROP FUNCTION IF EXISTS insert_units();
CREATE FUNCTION insert_units(cnty TEXT) returns void AS $$
DECLARE
	units RECORD;
	multiunits RECORD;
	prev_parcel_id integer := 0;
	num_units integer;
	num_largeapt_units integer;
	text_br text;
	br integer;
	count_units integer;
BEGIN
	FOR units IN ( 
		select	pr.parcel_id,
        		pr.puid,
        		pr.city as city_code,
        		pa.county,
        		pa.city,
        		pa.bldg_sqft as parcel_bldg_sqft,
        		pa.lastsale_val as parcel_lastsale_val,
        		pa.lastsale_date as parcel_lastsale_date,
        		pa.rent_per_sqft as parcel_rent_per_sqft,
        		pa.units as parcel_num_units,
        		hs."Bedrooms" as homesale_bedrooms,
        		to_number(hs."Sale_price", '9999999999') as homesale_sale_price,
        		hs."Sale_date" as homesale_sale_date,
        		hs."SQft" as homesale_sqft,
        		llamd."Units" as largeapt_units,
        		llamd."NumberOfUnits" as largeapt_num_units,
        		llamd."Description" as largeapt_description,
        		llamd."LowRent" as largeapt_lowrent,
        		llamd."HighRent" as largeapt_highrent,
        		(llamd."LowRent" + llamd."HighRent") / 2 as largeapt_avg_rent,
        		llamd."SquareFeet" as largeapt_sqft,
        		llamd."LastUpdated" as largeapt_last_updated,
        		bt.building_type_name,
        		bu.building_id,
        		bu.residential_units as building_residential_units,
        		bu.non_residential_sqft as building_non_residential_sqft,
        		bu.building_sqft as building_building_sqft,
        		(pa.bldg_sqft / pa.units) as parcel_sqft_per_unit,
        		((bu.building_sqft - bu.non_residential_sqft) / bu.residential_units) as building_sqft_per_unit,
        		(pa.bldg_sqft = (bu.building_sqft-bu.non_residential_sqft)) as sqft_parcel_bldg_check_flag,
        		(pa.units = llamd."Units") as units_parcel_largeapt_check_flag,
				(pa.units = bu.residential_units) as units_parcel_building_check_flag
		from public.parcels2010 pr
		left join public.parcels2010_attr pa
    		on pr.puid = pa.puid
		left join public.home_sales2008_2011 hs
    		on pr.puid = cast(hs.puid as int4)
		left join raw.big_appt09_joined_h b
    		on pr.puid = cast(b.puid as int4)
		left join (raw.large_apt_rent l
			join 
				(SELECT "BldgID" as bldg_id, 
					"Description" as descr,
					MAX("LastUpdated") as max_last_updated
				 FROM raw.large_apt_rent
				 GROUP BY "BldgID", "Description") as lamd --large_apt_max_date
    		on (
				l."BldgID" = lamd.bldg_id and
				l."Description" = lamd.descr and
				l."LastUpdated" = lamd.max_last_updated)) as llamd --large_apt_max_date x large_apt_rent
			on b."BldgID" = llamd."BldgID" 
		left join buildings2010 bu
    		on pr.parcel_id = bu.parcel_id
		left join building_types bt
    		on bu.building_type_id = bt.building_type_id 
		left join buildings2010_sta bs
			on bu.building_id = bs.building
		where bt.is_residential = 't'
		and bu.residential_units <> 0 
		and bs.scenario = 1
		--and pr.city in (75, 127)
		and pa.county = cnty
		order by pr.parcel_id ASC, to_date(hs."Sale_date", 'MM/DD/YYYY') DESC,
		 	llamd."LastUpdated" DESC) LOOP
	
		/* First check that parcel units are same as building units */ -- what if it's false? or null?
		/* Removed this check. --jmb */
	--	IF units.units_parcel_building_check_flag = 't' AND units.units_parcel_largeapt_check_flag = 't' THEN
			/* Prefer parcel units. If it's null, take building units */
			IF units.parcel_num_units is null THEN
				num_units := units.building_residential_units;
			ELSE
				num_units := units.parcel_num_units;
			END IF;

			/* Need to deal with multiple buildings and large apts separately */
			IF prev_parcel_id <> units.parcel_id AND units.largeapt_units is null THEN

				/* Loop over number of units */
				FOR i IN 1..num_units LOOP
					/* For first unit in group, add all info */
					IF i = 1 THEN
						EXECUTE 'INSERT INTO units2010 (building_id, unit_sqft, sale_price, bedrooms)
							VALUES (' || units.building_id || ', ' || 
									coalesce(units.parcel_sqft_per_unit, units.building_sqft_per_unit, -1)
									|| ', ' || quote_nullable(units.homesale_sale_price) || ', ' 
									|| quote_nullable(units.homesale_bedrooms) || ')';
					/* Otherwise add only the building ID and square footage */
					ELSE
						EXECUTE 'INSERT INTO units2010 (building_id, unit_sqft) 
							VALUES (' || units.building_id || ', ' ||
									coalesce(units.parcel_sqft_per_unit, units.building_sqft_per_unit) || ')';
					END IF;
				END LOOP;

			/* Large apt data */
			ELSIF units.largeapt_units is not null THEN
				num_largeapt_units := units.largeapt_num_units;
				
				/* Get number of bedrooms*/
				text_br := substring(units.largeapt_description from 1 for 1);
				if text_br ~ '^[A-Za-z]+$' then
					br := 0;
				else
					br = cast(text_br as integer);
				end if;
				
				/* Loop over number of units */
				FOR j IN 1..num_largeapt_units LOOP
					EXECUTE 'INSERT INTO units2010 (building_id, unit_sqft, rent, bedrooms) 
							VALUES (' || units.building_id || ',' || units.largeapt_sqft 
									|| ',' || units.largeapt_avg_rent || ',' || br || ')';
				END LOOP;
			/* Other multiple units	on parcel (for sales only?)*/
			ELSE
				/* If there are no null records, that means there are more sales than units
				   Sales are thus not unique by unit, but there have been multiple sales.
				   Make assumption and keep only most recent sales 
				   Is there a way to tell whether a particular unit has had the sale? */
				SELECT count(*) INTO count_units FROM units2010 
					WHERE building_id = units.building_id
					AND sale_price is NULL;
				IF count_units > 0 THEN
					EXECUTE 'UPDATE units2010 u
						SET unit_sqft = ' || coalesce(units.parcel_sqft_per_unit, units.building_building_sqft) || ',
						sale_price = ' || quote_nullable(units.homesale_sale_price) || ',
						bedrooms = ' || units.homesale_bedrooms || '
						FROM (select unit_id from units2010 where sale_price is null 
							and building_id = ' || units.building_id || '
							order by building_id limit 1) as avail
						WHERE u.building_id = ' || units.building_id || '
						AND u.unit_id = avail.unit_id 
						returning *';
				END IF;
			END IF;
		prev_parcel_id := units.parcel_id;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT insert_units('smt');
SELECT insert_units('son');
SELECT insert_units('ala');
SELECT insert_units('scl');
SELECT insert_units('nap');
SELECT insert_units('sfr');
SELECT insert_units('cnc');
SELECT insert_units('sol');
SELECT insert_units('mar');


--create indexes, PK, FK

