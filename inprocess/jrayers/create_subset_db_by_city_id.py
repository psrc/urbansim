#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
dbconfig = DatabaseServerConfiguration()
dbserver = DatabaseServer(dbconfig)

# city_id to subset database on (70=Seattle)
city_id = str(70)
# flattened database to use as input data
input_db = 'psrc_2005_parcel_baseyear_flattened_20080425'
# output database to create subset data in (must exist)
output_db = 'seattle_2000_parcel_baseyear_data_20080425'

tables_to_copy = [
    'home_based_employment_location_choice_model_coefficients',
    'home_based_employment_location_choice_model_specification',
    'non_home_based_employment_location_choice_model_coefficients',
    'non_home_based_employment_location_choice_model_specification',
    'household_location_choice_model_coefficients',
    'household_location_choice_model_specification',
    'real_estate_price_model_coefficients',
    'real_estate_price_model_specification',
    'land_use_types',
    'generic_land_use_types',
    'employment_sectors',
    'employment_adhoc_sector_groups',
    'employment_adhoc_sector_group_definitions',
    'development_templates',
    'development_template_components',
    'annual_relocation_rates_for_households',
    'annual_relocation_rates_for_jobs',
    'building_sqft_per_job',
    'building_types',
    'job_building_types',
    'urbansim_constants',
    'target_vacancies',
    'household_characteristics_for_ht',
    'development_constraints',
    'demolition_cost_per_sqft',
    ]

queries = [
    'DROP TABLE IF EXISTS %s.parcels;' % (output_db),
    'CREATE TABLE %s.parcels SELECT * FROM %s.parcels WHERE city_id = %s;' % (output_db, input_db, city_id),
    'CREATE INDEX parcels_out_parcel_id on %s.parcels (parcel_id);' % (output_db),
    'CREATE INDEX parcels_out_grid_id on %s.parcels (grid_id);' % (output_db),
    #'DROP INDEX gridcells_in_grid_id ON %s.gridcells;' % (input_db),
    'CREATE INDEX gridcells_in_grid_id3 ON %s.gridcells (grid_id);' % (input_db),
    'DROP TABLE IF EXISTS %s.gridcells;' % (output_db),
    'CREATE TABLE %s.gridcells SELECT g.* FROM %s.gridcells g, %s.parcels p WHERE g.grid_id = p.grid_id GROUP BY g.grid_id' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.cities;' % (output_db),
    'CREATE TABLE %s.cities SELECT * FROM %s.cities WHERE city_id = %s;' % (output_db, input_db, city_id),
    'DROP TABLE IF EXISTS %s.counties;' % (output_db),
    'CREATE TABLE %s.counties SELECT c.* FROM %s.counties c WHERE c.county_id = (SELECT county_id FROM %s.parcels GROUP BY county_id);' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.fazes;' % (output_db),
    'CREATE TABLE %s.fazes SELECT f.* FROM %s.fazes f, %s.parcels p WHERE f.faz_id = p.faz_id GROUP BY f.faz_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.large_areas;' % (output_db),
    'CREATE TABLE %s.large_areas SELECT l.* FROM %s.large_areas l, %s.parcels p WHERE l.large_area_id = p.large_area_id GROUP BY l.large_area_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.zones;' % (output_db),
    'CREATE TABLE %s.zones SELECT z.* FROM %s.zones z, %s.parcels p WHERE z.zone_id = p.zone_id GROUP BY z.zone_id;' % (output_db, input_db, output_db),
    'CREATE TABLE %s.travel_data1 SELECT td.* FROM %s.travel_data td, %s.zones z WHERE td.from_zone_id = z.zone_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.travel_data;' % (output_db),
    'CREATE TABLE %s.travel_data SELECT td.* FROM %s.travel_data1 td, %s.zones z WHERE td.to_zone_id = z.zone_id;' % (output_db, output_db, output_db),
    'DROP TABLE %s.travel_data1;' % (output_db),
    'DROP TABLE IF EXISTS %s.constant_taz_columns' % (output_db),
    'CREATE TABLE %s.constant_taz_columns SELECT c.* FROM %s.constant_taz_columns c, %s.zones z WHERE c.taz = z.zone_id GROUP BY c.taz, c.year;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.buildings;' % (output_db),
    'CREATE TABLE %s.buildings SELECT b.* FROM %s.buildings b, %s.parcels p WHERE b.parcel_id = p.parcel_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.households;' % (output_db),
    'CREATE INDEX households_in_building_id3 ON %s.households(building_id);' % (input_db),
    'CREATE INDEX buildings_out_building_id2 ON %s.buildings(building_id);' % (output_db),
    'CREATE TABLE %s.households SELECT h.* FROM %s.households h, %s.buildings b WHERE h.building_id = b.building_id;' % (output_db, input_db, output_db),
    'CREATE INDEX households_id3 ON %s.households(household_id);' % (output_db),
    'CREATE INDEX households_id4 ON %s.persons(household_id);' % (input_db),    
    'CREATE TABLE %s.persons SELECT p.* FROM %s.persons p, %s.households h WHERE p.household_id = h.household_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.jobs;' % (output_db),
    'CREATE INDEX jobs_in_building_id3 ON %s.jobs(building_id);' % (input_db),
    'CREATE TABLE %s.jobs SELECT j.* FROM %s.jobs j, %s.buildings b WHERE j.building_id = b.building_id;' % (output_db, input_db, output_db),
    'DROP TABLE IF EXISTS %s.annual_employment_control_totals;' % (output_db),
    'CREATE TABLE %s.annual_employment_control_totals SELECT * FROM %s.annual_employment_control_totals;' % (output_db, input_db),
    'UPDATE %s.annual_employment_control_totals SET total_home_based_employment = total_home_based_employment * ((SELECT COUNT(*) FROM %s.jobs) / (SELECT COUNT(*) FROM %s.jobs));' % (output_db, output_db, input_db),
    'UPDATE %s.annual_employment_control_totals SET total_non_home_based_employment = total_non_home_based_employment * ((SELECT COUNT(*) FROM %s.jobs) / (SELECT COUNT(*) FROM %s.jobs));' % (output_db, output_db, input_db),
    'DROP TABLE IF EXISTS %s.annual_household_control_totals;' % (output_db),
    'CREATE TABLE %s.annual_household_control_totals SELECT * FROM %s.annual_household_control_totals;' % (output_db, input_db),
    'UPDATE %s.annual_household_control_totals SET total_number_of_households = total_number_of_households * ((SELECT COUNT(*) FROM %s.households) / (SELECT COUNT(*) FROM %s.households));' % (output_db, output_db, input_db)
    ]

# Copies all tables that are a complete copy
for i in tables_to_copy:
    query = "CREATE TABLE %s.%s SELECT * FROM %s.%s;" % (output_db, i, input_db, i)
    dbserver.DoQuery(query)
    print 'Finished copying %s...' % (i)

# Creates all tables that are a subset of the original data
for i in queries:
    dbserver.DoQuery(i)
    print 'Finished:  %s' % (i)




