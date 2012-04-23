# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, cPickle, time, sys, string, StringIO
try:
    from bayarea.accessibility.pyaccess import PyAccess
except:
    from bayarea.accessibility.pyaccess import PyAccess
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.session_configuration import SessionConfiguration
from opus_core import paths
import numpy
from numpy import array

class NodeDataset(UrbansimDataset):
    
    id_name_default = "node_id"
    in_table_name_default = "nodes"
    out_table_name_default = "nodes"
    dataset_name = "node"
    path = paths.get_opus_data_path_path("bay_area_parcel","network.jar")
    d = cPickle.load(open(path))
    pya = PyAccess()
    pya.createGraph(1,d['nodeids'],d['nodes'],d['edges'],d['edgeweights'])
    pya.precomputeRange(500)
    pya.initializePOIs(1,.5*1.6*1000,1)
    x = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','x.lf4'))))
    y = numpy.load((os.path.join(paths.get_opus_data_path_path('bay_area_parcel','base_year_data','2010','transit_stations','y.lf4'))))
    xys = numpy.column_stack((x,y))
    pya.initializeCategory(0,xys)

    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        node_ids = self.get_id_attribute()
        node_d = dict(zip(self.d['nodeids'],range(len(node_ids))))
        node_ids = [node_d[x] for x in node_ids]
        self.node_ids = array(node_ids, dtype="int32")
        
        #dataset_pool = SessionConfiguration().get_dataset_pool() 
        #print dataset_pool.datasets_in_pool()
        #transit_set = dataset_pool.get_dataset('transit_station')

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
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,0,1,0)
        return result

    def subbuilding_sum_query(self, distance, attribute, table): 
        node_data = self.compute_variables('node.aggregate((%s.%s*1.0), intermediates=[building,parcel])' % (table, attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,0,1,0)
        return result

    def building_avg_query(self, distance, attribute):
        node_data = self.compute_variables('node.aggregate((building.%s*1.0), intermediates=[parcel],function=mean)' % (attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,1,1,0)
        return result

    def subbuilding_avg_query(self, distance, attribute, table):
        node_data = self.compute_variables('node.aggregate((%s.%s*1.0), intermediates=[building,parcel],function=mean)' % (table, attribute))
        node_data = array(node_data, dtype="float32")
        self.pya.initializeAccVars(1)
        self.pya.initializeAccVar(0,self.node_ids,node_data)
        result=self.pya.getAllAggregateAccessibilityVariables(distance,0,1,1,0)
        return result

    def transit_dist_query(self, distance):
        result = self.pya.findAllNearestPOIs(distance,0)
        return result
