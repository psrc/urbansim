import psycopg2

class Parcels():
    def __init__(my):
        conn_string = "host='paris.urbansim.org' dbname='bayarea' user='urbanvision' password='***'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

	# empty parcels
        s = "select p.* from parcels2010_withgeography as p left outer join buildings2010 as b on (p.parcel_id = b.parcel_id) where b.parcel_id is NULL"
	
	print s
        cursor.execute(s)
	records = cursor.fetchall()
	fnames = [x[0] for x in cursor.description]
	print fnames
	fnames = dict(zip(fnames,range(len(fnames))))
	d = {}
	for r in records:
	    id = r[fnames['parcel_id']]
	    d[id] = [r[fnames['shape_area']],r[fnames['zone_id']]]
        my.parcels = d
	my.parcelfnames = {'shape_area': 0,'zone_id': 1}

        d = {}
	for i in range(1455): d[i] = []
	s = '''
select _zone_id, avg(shape_area)*10.7938 as shape_area from buildings2010 b, buildings2010_sta sta, parcels2010 p
where building_id = building and scenario = 1 and building_type_id = 1 and b.parcel_id = p.parcel_id and residential_units = 1
group by _zone_id order by _zone_id
'''

	print s
        cursor.execute(s)
	records = cursor.fetchall()
	for r in records:
	    zid, size = r
	    d[zid].append(size)
	my.lotsize = d
	
	s = '''
select _zone_id, building_type, sum(building_sqft-non_residential_sqft), sum(residential_units), 
sum(building_sqft-non_residential_sqft)/sum(residential_units) as ave
from buildings2010 b, buildings2010_sta sta
where building_id = building and scenario = 1 and residential_units is not null and building_sqft is not null
group by _zone_id, building_type having sum(residential_units) > 10 and 
sum(building_sqft-non_residential_sqft)/sum(residential_units) > 300 order by _zone_id

'''
	print s
        cursor.execute(s)
	records = cursor.fetchall()
	for r in records:
	    zid, btype, sqft, units, avesqft = r
	    d[(zid,btype)] = avesqft
	my.unitsize = d

    def get_pids(my):
	return my.parcels.keys()

    def get_attr(my,pid,attr_name):
        return my.parcels[pid][my.parcelfnames[attr_name]]

    def get_lotsize(my, zone_id):
	if zone_id not in my.lotsize or len(my.lotsize[zone_id]) == 0: return None
	return int(my.lotsize[zone_id][0])

    def get_unitsize(my, zone_id, btype):
	return my.unitsize.get((zone_id,btype),None)

class Zoning():
    def __init__(my):
        conn_string = "host='paris.urbansim.org' dbname='bayarea' user='urbanvision' password='Visua1ization'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

	# first, zoning
        s = "select * from geography_zoning"
	print s
        cursor.execute(s)
	records = cursor.fetchall()
	fnames = [x[0] for x in cursor.description]
	assert 'id' == fnames[0]
	print fnames
	d = {}
	for r in records:
	    id = r[0]
	    d[id] = r
        my.zoning = d
	my.zoningfnames = dict(zip(fnames,range(len(fnames))))

        # then relate to parcels
        s = "select * from geography_zoning_parcel_relation"
	print s
        cursor.execute(s)
	records = cursor.fetchall()
	fnames = [x[0] for x in cursor.description]
	assert 'zoning' == fnames[1]
	assert 'parcel_id' == fnames[2]
	print fnames
	d = {}
	for r in records:
	    pid = r[2]
	    zid = r[1]
	    d[pid] = zid
	my.pid2zid = d

	s= "select * from geography_building_type_zone_relation"
	print s
        cursor.execute(s)
	records = cursor.fetchall()
	fnames = [x[0] for x in cursor.description]
	assert 'zone' == fnames[1]
	assert 'building_type' == fnames[2]
	d = {}
	for r in records:
	    btype = r[2]
	    zid = r[1]
	    d.setdefault(zid,[])
	    d[zid].append(btype)
	my.zid2btype = d
        
    def get_building_types(my, parcel_id):
	if parcel_id not in my.pid2zid: return None
	zid = my.pid2zid[parcel_id]
	if zid not in my.zid2btype: return None
	return my.zid2btype[zid]

    def get_zoning(my, parcel_id):
	if parcel_id not in my.pid2zid: return None
	zid = my.pid2zid[parcel_id]
	return my.zoning[zid]

    def get_attr(my, zoning, attr_name, default):
        ind = my.zoningfnames[attr_name]
        v = zoning[ind]
        if not v: return default
        return v
