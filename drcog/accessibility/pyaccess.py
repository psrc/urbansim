import _pyaccess
from string import split
import numpy
import time
    
class PyAccess():

    # id is an identifier for this graph
    # nodeids is a numpy array of ints that are ids
    # nodexy is a Nx2 array of floats which are the x / y coords (lat / longs)
    # edgedef is a Nx2 array where each row is an edge - the two ints identify
    #         the INDEXES of the nodes, not the nodeids
    # weights the impedances for each each - one to one mapping ot edgedef
    def createGraph(my,id,nodeids,nodexy,edgedef,weights):
        _pyaccess.create_graph(id,nodeids,nodexy,edgedef,weights)

    def initializePOIs(my,numcategories,maxdist,maxitems):
        _pyaccess.initialize_pois(numcategories,maxdist,maxitems)

    def initializeCategory(my,cat,latlongs):
        _pyaccess.initialize_category(cat,latlongs)

    def findNearestPOIs(my,nodeid,radius,number,category):
        return _pyaccess.find_nearest_pois(nodeid,radius,number,category)
    
    def findAllNearestPOIs(my,radius,category):
        l = _pyaccess.find_all_nearest_pois(radius,category)
        return [x if x != -1 else radius for x in l]

    def getOpenWalkscore(my,nodeid):
        return _pyaccess.get_open_walkscore(nodeid)

    def getAllOpenWalkscores(my):
        return _pyaccess.get_all_open_walkscores()

    def initializeAccVars(my,numcategories):
        return _pyaccess.initialize_acc_vars(numcategories)
    
    # this is a possible performance improvement where I presum by node
    # is not going to help much unless there's a lot of data elements though, which there aren't
    def sum_by_group(my,values, groups):
        order = numpy.argsort(groups)
        groups = groups[order]
        values = values[order]
        values.cumsum(out=values)
        index = numpy.ones(len(groups), 'bool')
        index[:-1] = groups[1:] != groups[:-1]
        values = values[index]
        groups = groups[index]
        values[1:] = values[1:] - values[:-1]
        return values, groups

    def initializeAccVar(my,cat,nodeids,accvar,preaggregate=1):
        if preaggregate:
            accvar, nodeids = my.sum_by_group(accvar, nodeids)

        return _pyaccess.initialize_acc_var(cat,nodeids,accvar)

    def LatLongtoNode(my,lat,long):
        xy = numpy.array([(lat,int)],dtype=numpy.int32)
        returntoNode(xy)[0]

    def XYtoNode(my,xy,distance=-1):
        return _pyaccess.xy_to_node(xy,distance)
    
    def getManyAggregateAccessibilityVariables(my,nodeids,radius,index,aggregation, \
																decay):
        return _pyaccess.get_many_aggregate_accessibility_variables(nodeids,radius, \
													index,aggregation,decay)

    def getAllAggregateAccessibilityVariables(my,radius,index,aggregation, \
																decay,gno=0):
        return _pyaccess.get_all_aggregate_accessibility_variables(radius, \
													index,aggregation,decay,gno)
    
    def aggregateAccessibilityVariable(my,nid,radius,index,aggregation,decay):
        return _pyaccess.aggregate_accessibility_variable(nid,radius, \
													index,aggregation,decay)

    def computeDesignVariable(my,nid,radius,typ):
		return _pyaccess.compute_design_variable(nid,radius,typ)
    
    def computeAllDesignVariables(my,radius,typ):
        return _pyaccess.compute_all_design_variables(radius,typ)

    def precomputeRange(my,radius):
        return _pyaccess.precompute_range(radius)
