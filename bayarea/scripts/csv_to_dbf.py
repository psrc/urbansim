# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.store.csv_storage import csv_storage
from opus_core.store.dbf_storage import dbf_storage
import os, sys

if len(sys.argv) not in (2,3):
    print("Usage: %s csv_file [dbf_file]" % sys.argv[0])
    sys.exit(0)

csv_file = sys.argv[1]
csv_file = os.path.normpath(csv_file)
csv_path, csv_name = os.path.split(csv_file)
csv_table, csv_ext = os.path.splitext(csv_name)

if len(sys.argv) == 2:
    dbf_path, dbf_table = csv_path, csv_table
elif len(sys.argv) == 3:
    dbf_file = sys.argv[2]
    dbf_file = os.path.normpath(dbf_file)
    dbf_path, dbf_name = os.path.split(dbf_file)
    dbf_table, dbf_ext = os.path.splitext(dbf_name)

csv_store = csv_storage(storage_location=csv_path)
dbf_store = dbf_storage(storage_location=dbf_path)
data = csv_store.load_table(csv_table)
dbf_store.write_table(dbf_table, data)

