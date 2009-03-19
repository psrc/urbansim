# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from sqlalchemy import *

def get_zones_and_num_hh_to_add():
    """
    This returns a list of zones and the number of
    households to add, excluding the special_zones
    """
    hh_diff = get_hh_differences_by_zone()
    zones_hh_to_add = []
    for i in hh_diff:
        if i[1] > 0:
            zones_hh_to_add.append(i)
    zones_hh_to_add_copy = []
    for j in zones_hh_to_add:
        zones_hh_to_add_copy.append(j)
    for k in zones_hh_to_add:
        if k in special_zones:
           zones_hh_to_add_copy.remove(k)
    return zones_hh_to_add_copy

def add_households(zone_id, num_hh_to_add):
    """
    This adds a given number of households given
    a zone_id
    """
    z_id = str(zone_id)
    n_hh_add = str(num_hh_to_add)
    query_create_temp_table = text("""
                                      CREATE TABLE hhtemp1
                                      SELECT * FROM households_temp WHERE zone_id = %s ORDER BY RAND() LIMIT %s;
                                   """ % (z_id, n_hh_add))
    query_insert_records = text("""INSERT INTO households_temp
                                   SELECT * FROM hhtemp1;
                                """)
    query_drop_temp_table = text("""DROP TABLE IF EXISTS hhtemp1""")
    
    conn.execute(query_create_temp_table)
    conn.execute(query_insert_records)
    conn.execute(query_drop_temp_table)

def add_households_from_nearest_5_zones(zone_id, list_of_zones, num_hh_to_add):
    """
    This adds a given number of households to
    a zone given a list of zone_ids to select from
    """
    z_id = str(zone_id)
    z0 = list_of_zones[0]
    z1 = list_of_zones[1]
    z2 = list_of_zones[2]
    z3 = list_of_zones[3]
    z4 = list_of_zones[4]
    n_hh_add = str(num_hh_to_add)
    query_create_temp_table = text("""
                                      CREATE TABLE hhtemp1
                                      SELECT * FROM households_temp
                                      WHERE
                                          (zone_id = %s) or
                                          (zone_id = %s) or
                                          (zone_id = %s) or
                                          (zone_id = %s) or
                                          (zone_id = %s)
                                          ORDER BY RAND() LIMIT %s;
                                   """ % (z0, z1, z2, z3, z4, n_hh_add))
    query_change_zone_id = text("""UPDATE hhtemp1
                                   SET zone_id = %s;
                                """ % (z_id))
    query_insert_records = text("""INSERT INTO households_temp
                                   SELECT * FROM hhtemp1;
                                """)
    query_drop_temp_table = text("""DROP TABLE IF EXISTS hhtemp1""")
    
    conn.execute(query_create_temp_table)
    conn.execute(query_change_zone_id)
    conn.execute(query_insert_records)
    conn.execute(query_drop_temp_table)


def get_nearest_5_zones(zone_id):
    """
    This returns a list of the nearest 5 zones as
    measured by straight line distance from centroid
    to centroid
    """
    z_id = str(zone_id)
    lst = []
    qry = "select * from zones_all_distances_in_order where orig_zone = %s limit 6" % (z_id)
    result = conn.execute(qry).fetchall()
    for i in range(1,6):
        lst.append(result[i][2])
    return lst


def get_hh_differences_by_zone():
    """
    This returns a list of tuples that give the number of households
    to add or delete by zone
    """
    query_for_hh_differences = text("""select zone_id, diff from hh_diff;""")
    hh_diff = conn.execute(query_for_hh_differences).fetchall()
    return hh_diff

def get_zones_and_num_hh_to_delete():
    """
    This returns a list of zones and the number of
    households to delete
    """
    hh_diff = get_hh_differences_by_zone()
    zones_hh_to_delete = []
    for i in hh_diff:
        if i[1] < 0:
            zones_hh_to_delete.append(i)
    return zones_hh_to_delete

def delete_households(zone_id, num_hh_to_delete):
    """
    This deletes a given number of households for
    a given zone_id
    """
    z_id = str(zone_id)
    num_hh = str(num_hh_to_delete)
    qry = text("delete FROM households_temp where (rand() and zone_id = %s) limit %s;" % (z_id, num_hh))
    conn.execute(qry)

# This is where the action of this script takes place:

# create engine and connection
password = 'CHANGE ME'
engine = create_engine('mysql://urbansim:%s@trondheim/psrc_2005_parcel_baseyear_change_20071120' % (password))
conn = engine.connect()

# These zones have either 0 households from the synthesizer or
# have less than half the needed households from the synthesizer
# These zones will be treated separately
# special_zones = [342,339,135,290,180,233,340,344,167,741,388]
special_zones = [(342,3),(339,6),(135,2),(290,3),(180,2),(233,5),(340,3),(344,1),(167,10),(741,553),(388,6)]

print "DELETING OLD households_temp TABLE..."
qry = text("DROP TABLE IF EXISTS households_temp;")
conn.execute(qry)

print "CREATING NEW households_temp TABLE..."
qry = text("""CREATE TABLE households_temp
              SELECT * FROM psrc_2005_parcel_baseyear_change_20070824.households;
           """)
conn.execute(qry)

print "DELETING HOUSEHOLDS..."
hh_differences_by_zone = get_hh_differences_by_zone()
zones_and_num_hh_to_delete = get_zones_and_num_hh_to_delete()
for i in zones_and_num_hh_to_delete:
    delete_households(i[0], abs(i[1]))

print "ADDING HOUSEHOLDS..."
zones_and_num_hh_to_add = get_zones_and_num_hh_to_add()
for i in zones_and_num_hh_to_add:
    add_households(i[0], i[1])

print "ADDING HOUSHOLDS IN SPECIAL ZONES..."
for i in special_zones:
    list_of_zones = get_nearest_5_zones(i[0])
    add_households_from_nearest_5_zones(i[0], list_of_zones, i[1])

print "RESETTING household_id..."
qry = text("""
            UPDATE households_temp
            SET household_id = null;
           """)
conn.execute(qry)

qry = text("""
            ALTER TABLE households_temp
            MODIFY COLUMN household_id INTEGER NOT NULL DEFAULT NULL AUTO_INCREMENT,
            ADD PRIMARY KEY (household_id);
           """)
conn.execute(qry)

print "DONE"
