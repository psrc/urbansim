# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, pickle, time, sys, string, io
try:
    from bayarea.accessibility.pyaccess import PyAccess
except:
    from bayarea.accessibility.pyaccess import PyAccess
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.session_configuration import SessionConfiguration
from opus_core import paths
import numpy
from numpy import array
    
MAXDISTANCE=1500 
path = paths.get_opus_data_path_path("bay_area_parcel","network.jar")
d = pickle.load(open(path))
pya = PyAccess()
pya.createGraph(1,d['nodeids'],d['nodes'],d['edges'],d['edgeweights'])
pya.precomputeRange(MAXDISTANCE)
pya.initializePOIs(7,MAXDISTANCE,1)
dataset_pool = SessionConfiguration().get_dataset_pool()
transit_set = dataset_pool.get_dataset('transit_station')
x = transit_set['x']
y = transit_set['y']
route_type = transit_set['route_type']
agency_id = transit_set['agency_id']
#x = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','x.lf4'))))
#y = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','y.lf4'))))
for i in range(6):
    if i == 1: # bart
        xys = numpy.column_stack((x[agency_id == 6],y[agency_id == 6]))
    elif i == 2: # caltrain
        xys = numpy.column_stack((x[agency_id == 9],y[agency_id == 9]))
    else:
        xys = numpy.column_stack((x[route_type==i],y[route_type==i]))
    pya.initializeCategory(i,xys)

xys = numpy.column_stack((x,y))
pya.initializeCategory(6,xys)


class NodeDataset(UrbansimDataset):
   
    id_name_default = "node_id"
    in_table_name_default = "nodes"
    out_table_name_default = "nodes"
    dataset_name = "node"

    path = paths.get_opus_data_path_path("bay_area_parcel","network.jar")
    d = pickle.load(open(path))

    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        node_ids = self.get_id_attribute()
        node_d = dict(list(zip(self.d['nodeids'],list(range(len(node_ids))))))
        node_ids = [node_d[x] for x in node_ids]
        self.node_ids = array(node_ids, dtype="int32")
        global MAXDISTANCE, pya
        self.MAXDISTANCE = MAXDISTANCE
        self.pya = pya
        
        #x = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','x.lf4'))))
        #y = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','y.lf4'))))
        #xys = numpy.column_stack((x,y))
        #self.pya.initializePOIs(1,.5*1.6*1000,1)
        #self.pya.initializeCategory(0,xys)
   
    # def design_variable_query(self, distance):
        # result = self.pya.computeAllDesignVariables(distance,"LINEALSTREETFEET")
        # return result

    def building_sum_query(self, distance, attribute):
        node_data = self.compute_variables('node.aggregate((building.%s*1.0), intermediates=[parcel])' % (attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        assert distance <= self.MAXDISTANCE
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,0,1,0)
        return result

    def subbuilding_sum_query(self, distance, attribute, table): 
        node_data = self.compute_variables('node.aggregate((%s.%s*1.0), intermediates=[building,parcel])' % (table, attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        assert distance <= self.MAXDISTANCE
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,0,1,0)
        return result

    def building_avg_query(self, distance, attribute):
        node_data = self.compute_variables('node.aggregate((building.%s*1.0), intermediates=[parcel],function=mean)' % (attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        assert distance <= self.MAXDISTANCE
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,1,1,0)
        return result

    def subbuilding_avg_query(self, distance, attribute, table):
        node_data = self.compute_variables('node.aggregate((%s.%s*1.0), intermediates=[building,parcel],function=mean)' % (table, attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        assert distance <= self.MAXDISTANCE
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,1,1,0)
        return result

    def transit_dist_query(self, distance, category=6):
        assert distance <= self.MAXDISTANCE
        assert category < 7
        result = self.pya.findAllNearestPOIs(distance,category)
        return result
