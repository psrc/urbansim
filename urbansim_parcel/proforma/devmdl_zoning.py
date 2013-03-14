# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import psycopg2
import os

class Zoning():
  def __init__(my,scenario,year):
    passwd = os.environ['OPUS_DBPASS']
    host = os.environ['OPUS_HOST']
    ##dbname should be an argument passed in from the GUI
    conn_string = "host='%s' dbname='denver' port=5433 user='urbanvision' password='%s'" % (host,passwd)   ####Don't hard-code host, dbname
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    # first, zoning
    s = "select * from geography_zoning"
    print s
    cursor.execute(s)
    records = cursor.fetchall()
    fnames = [x[0] for x in cursor.description]
    assert fnames[-1] == "id_class"
    #print fnames
    d = {}
    for r in records:
        id = r[-1]
        d[id] = r

    my.zoning = d
    my.zoningfnames = dict(zip(fnames,range(len(fnames))))

    s = "select id from scenario where name = '%s'" % scenario
    print s
    cursor.execute(s)
    records = cursor.fetchall()
    assert len(records) == 1
    scenarioid = int(records[0][0])

    # then relate to parcels   ######  Need a zoning_for_parcels function in the denver DB and all DBs!!!
    #s = "select * from zoning_for_parcels(%d,'%d-01-01 00:00:00')" % (scenarioid,year)
    # s = "select * from geography_zoning z,geography_zoning_parcel_relation_base zp where z.id = zp.zoning"
    # print s
    # cursor.execute(s)
    # records = cursor.fetchall()
    # fnames = [x[0] for x in cursor.description]
    # #print fnames
    # assert 'parcel_id' == fnames[18]
    # assert 'zoning' == fnames[17]
    # d = {}
    # for r in records:
        # pid = r[18]
        # zid = r[17]
        # d[pid] = zid
    # my.pid2zid = d
    # print "Found %d parcel->zoning relationships" % len(d)

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
    

    s= "select * from geography_parking_requirement where unit = 1"
    print s
    cursor.execute(s)
    records = cursor.fetchall()
    fnames = [x[0] for x in cursor.description]
    assert 'zone' == fnames[1]
    assert 'use' == fnames[2]
    assert 'min_quantity' == fnames[4]
    d = {}
    for r in records:
        btype = r[2]
        zid = r[1]
        parking = r[4]
        d[(zid,btype)] = parking
    my.zid2parking = d
        
  def get_parking_requirements(my, parcel_id, btype):
        if parcel_id not in my.pid2zid: return None
        zid = my.pid2zid[parcel_id]
        key = (zid, btype)
        if key not in my.zid2parking: return None
        return my.zid2parking[key]

  # def get_building_types(my, parcel_id):
        # if parcel_id not in my.pid2zid: return None
        # zid = my.pid2zid[parcel_id]
        # if zid not in my.zid2btype: return None
        # return my.zid2btype[zid]
        
  def get_building_types(my, zid):
        return my.zid2btype[zid]

  def get_zoning(my, parcel_id):
        parcel_id = int(parcel_id)
        if parcel_id not in my.pid2zid:
            return None
        zid = my.pid2zid[parcel_id]
        return my.zoning[zid]

  def get_attr(my, zoning, attr_name, default):
        ind = my.zoningfnames[attr_name]
        v = zoning[ind]
        if not v: return default
        return v
