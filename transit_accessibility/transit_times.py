# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


import os, time
import networkx as NX
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset

print("Program started at %s" % time.asctime())

fh=open("C:/bhylee/GIS/Transit/IATBR06/03Network/psrc_edges_num.edgelist") # <<<< INPUT EDGELIST FILE
G=NX.read_edgelist(fh,create_using=NX.XDiGraph(),edgetype=int)

print("Done reading edgelist at %s" % time.asctime())

input_file = "C:/bhylee/GIS/Transit/IATBR06/03Network/psrc_o_d.txt" # <<<< INPUT ORIGIN/DESTINATION FILE
input_file_dir, input_file_name = os.path.split(input_file)
in_fh = open(os.path.join(input_file_dir,input_file_name), 'r')

#output
output_file = "results.tab"
out_fh = open(os.path.join(input_file_dir,output_file), 'w')
out_fh.write("orig\tdest\ttime\n")

#storage = StorageFactory().get_storage('tab_storage', subdir='store',
#    storage_location=input_file_dir)
#dataset = Dataset(in_storage = storage, id_name = ['orig','dest'], in_table_name = input_file_name)

#origs = dataset.get_attribute("orig")
#dests = dataset.get_attribute("dest")

firstline = in_fh.readline()
first_col, sec_col = firstline.strip().split("\t")
columns = {}

i = 0
lines = in_fh.readlines()
print("Done reading O/D at %s" % time.asctime())
print("Number of O/D pairs is %s" % len(lines))

for line in lines:
#for i in range(origs.size()):
    columns[first_col], columns[sec_col] = line.strip().split("\t")
    print("O/D pair", i+1)
    i = i + 1
    try:
        result = NX.dijkstra_path_length(G, str(columns["orig"]), str(columns["dest"]))
    except:
        result = "N/A"
    out_fh.write("%s\t%s\t%s\n" % (columns[first_col],columns[sec_col],result))
    out_fh.flush()

in_fh.close()
out_fh.close()
print("Program completed at %s" % time.asctime())