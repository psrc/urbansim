# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.misc import unique
from opus_core.logger import logger
from numpy import array, bool8, logical_not, all, ones, where
import networkx

class EdgeDataset(UrbansimDataset):
    
    id_name_default = ["source","target"]
    in_table_name_default = "edges"
    out_table_name_default = "edges"
    dataset_name = "edge"
    
    def __init__(self, id_values=None, **kwargs):
        self.graph = None
        UrbansimDataset.__init__(self, **kwargs)
    
    def create_graph(self, create_using=networkx.Graph(), nodetype=str, edgetype=str):       
        """see reference on read_edgelist method in networkx.io module"""
                    
        try:
            G=create_using
            G.clear()
        except:
            raise TypeError("Input graph is not a networkx graph type")
    
        # is this a XGraph or XDiGraph?
        if hasattr(G,'allow_multiedges')==True:
            xgraph=True
        else:
            xgraph=False
    
        attrs = self.get_known_attribute_names()
        id_names = self.get_id_name()
        data_attr = [attr for attr in attrs if attr not in id_names]
        sources = self.get_attribute(id_names[0])
        targets = self.get_attribute(id_names[1])
    
        if len(data_attr) == 1:
            data = self.get_attribute(data_attr[0])
        elif len(data_attr) == 0:
            data = None
        else:
            raise "Failed to handle attribute: %s" % data_attr
    
        for i in range(self.size()):
            u = sources[i]; v = targets[i]
            try:
                (u,v)=map(nodetype,(u,v))
            except:
                raise TypeError("Failed to convert edge (%s, %s) to type %s"\
                      %(u,v,nodetype))
    
            if data is not None:
                try:
                   d=edgetype(data[i])
                except:
                    raise TypeError("Failed to convert edge data (%s) to type %s"\
                                    %(data[i], edgetype))
            if xgraph:
                G.add_edge(u,v,d)  # XGraph or XDiGraph
            else:
                G.add_edge(u,v)    # Graph or DiGraph

        self.graph = G
        return self.graph
    
    def get_graph(self, **kwargs):
        """return graph if exists, creates it otherwise"""
        if self.graph is None:
            self.create_graph(**kwargs)
        return self.graph

    def compute_dijkstra_path_length(self, pairs, default_value=999, show_progress=False):
        G = self.get_graph()
        results = []
        if show_progress:
            try:
                from sandbox.progress import ProgressMeter
                p = ProgressMeter(total=len(pairs))
            except:pass
        for orig, dest in pairs:
            if type(dest) != list:
                dest = [dest]
            result = default_value * ones(len(dest))
            if not G.has_node(str(orig)):
                if not show_progress: #suppress warning msgs
                    logger.log_warning("failed to find source node %s in pair (%s, %s); the values are set to %s." \
                                   % (orig, orig, dest, default_value))
            else:
                has_nodes = array([G.has_node(str(x)) for x in dest])
                for node_index in where(logical_not(has_nodes))[0]:
                    if not show_progress:
                        logger.log_warning("failed to find target node %s in pair (%s, %s); the value is set to %s." \
                                       % (dest[node_index], orig, dest, default_value))
                        #result[node_index] = default_value

                if has_nodes.sum() != 0:
                    dest_str = [str(x) for x in dest]
                    valid_targets = [dest_str[x] for x in where(has_nodes)[0]]
                    (length,path) = list_dijkstra(G, str(orig), valid_targets)
                    for target in valid_targets:
                        index = dest_str.index(target)
                        if length.has_key(target):
                            result[index] = length[target]
                        else:
                            if not show_progress:
                                logger.log_warning("failed to find a path from %s to %s; the value is set to %s." \
                                               % (orig, dest[index], default_value))
                            result[index] = default_value
                    
            results.append(result)
            if show_progress:
                try:
                    p.update(1)
                except:pass
        return results

def list_dijkstra(G,source,target=None):
    """
    This is a revsion version of dijkstra function in networkx.paths.py.
    Target could be a list of nodes.
    """
    if type(target) != list:
        target = [target]
    unique_size = len(unique(target))
    
    Dist = {}  # dictionary of final distances
    Paths = {source:[source]}  # dictionary of paths
    seen = {source:0} 
    fringe=networkx.queues.Priority(lambda x: seen[x])
    fringe.append(source)
    
    if not G.is_directed():  G.successors=G.neighbors
    # if unweighted graph, set the weights to 1 on edges by
    # introducing a get_edge method
    # NB: for the weighted graphs (XGraph,XDiGraph), the data
    # on the edge (returned by get_edge) must be numerical
    if not hasattr(G,"get_edge"): G.get_edge=lambda x,y:1

    while fringe:
        v=fringe.smallest()
        if v in Dist: continue # already searched this node.
        Dist[v] = seen[v]
        if v in target:
            unique_size = unique_size - 1
            if unique_size == 0:
                break
            
        for w in G.successors(v):
            vwLength = Dist[v] + G.get_edge(v,w)
            if w in Dist:
                if vwLength < Dist[w]:
                    raise ValueError,\
                          "Contradictory paths found: negative weights?"
            elif w not in seen or vwLength < seen[w]:
                seen[w] = vwLength
                fringe.append(w) # breadth first search
                Paths[w] = Paths[v]+[w]
    return (Dist,Paths)


def get_path_for_origion_and_destination_pairs(G, pairs, default_value=999):

    results = []
    for orig, dest in pairs:
        try:
            result = networkx.dijkstra_path_length(G, str(orig), str(dest))
        except:
            logger.log_warning("failed to find a path from %s to %s; the value is set to %s." \
                               % (orig, dest, default_value))
            result = default_value
        results.append(result)
    return results

def dijkstra_path_length(G,source,target=None):
    """
    This is a modified version of dijkstra_path_length function in netowrkx.paths.py.
    Target could be a list of nodes.
    """
    (length,path)=dijkstra(G,source,target=target)


    if target is not None:
        try:
            return length[target]
        except KeyError:
            raise networkx.NetworkXError, \
                  "node %s not reachable from %s"%(source,target)

    return length


