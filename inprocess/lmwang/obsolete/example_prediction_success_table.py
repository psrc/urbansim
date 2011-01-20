# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus.core.sampling_functions import sample_choice
from opus.sandbox.estimation_toolbox import count_agents_by_location
from opus.core.opusnumarray import sum
from numarray import zeros, where, Float32,ones, array
from numarray.nd_image import sum as nd_image_sum
import copy

#def copy_dataset(dataset):
#    attr_list = ['set', 'attribute_names', 'id_mapping', 'nonderived_attribute_names']
#    new_dataset = copy.copy(dataset)
#    for attr in attr_list:
#        exec("new_dataset." + attr + " = copy.deepcopy(dataset." + attr + ")")
#    return new_dataset

def plot_prediction_map(LCM, location_set, observed_choices_id, choice_method='mc', 
                        main="", xlab="x", ylab="y", min_value=None, max_value=None, file=None):
    """refer to docstring of create_prediction_success_table"""
    #plot map for observed location choices
    counts = count_agents_by_location(location_set, observed_choices_id)
    location_set.add_attribute(counts,"counts_of_observed_agents")
        
    location_set.plot_map('counts_of_observed_agents', main=main, xlab=xlab, ylab=ylab, min_value=min_value, max_value=max_value, file=file)
    location_set.unload_one_attribute("counts_of_observed_agents")
    
    
    #plot map for prediction location choices/demands
    LCM.simulate_step()
    choices = sample_choice(LCM.model.probabilities, choice_method)
    choices_index = LCM.model_resources.translate("index")[choices]
    
    choices_id = location_set.get_id_attribute()[choices_index]
    counts = count_agents_by_location(location_set, choices_id[ai])
    location_set.add_attribute(counts,"counts_of_predicted_agents")
                
    location_set.plot_map('counts_of_predicted_agents', main=main, xlab=xlab, ylab=ylab, min_value=min_value, max_value=max_value, file=file)
    location_set.unload_one_attribute("counts_of_predicted_agents")

def get_predicted_agent_set(LCM, agent_set, location_set, agents_index=None, choice_method="MC"):
    LCM.simulate_step()
    choices = sample_choice(LCM.model.probabilities, choice_method)
    choices_index = LCM.model_resources.translate("index")[choices]
    choices_id = location_set.get_id_attribute()[choices_index]
    agent_set_sim = copy.deepcopy(agent_set)
    agent_set_sim.set_values_of_one_attribute(location_set.get_id_name()[0], choices_id, agents_index)
        
    return agent_set_sim
    
def create_prediction_success_table(LCM, location_set, observed_choices_id, geographies=[], \
                                    choice_method='mc', data_objects=None):
    """this function creates a table tabulating number of agents observed versus predicted by geographies for location choice model
    LCM is an instance of Location Choice Model after run_estimation,
    location_set is the set of location in simulation, e.g. gridcell,
    observed_choice_id is the location_set id (e.g. grid_id) observed,
    geographies is a list of geographies to create prediction sucess table for,
    choice_method is the method used to select choice for agents, either mc or max_prob
    data_objects is the same as data_objects used to run LCM simulation, but includes entries for geographies
    """
    LCM.simulate_step()
    choices = sample_choice(LCM.model.probabilities, choice_method)
    choices_index = LCM.model_resources.translate("index")[choices]   #translate choices into index of location_set
    #maxprob_choices = sample_choice(LCM.model.probabilities, method="max_prob")  #max prob choice
    #maxprob_choices_index = LCM.model_resources.translate("index")[maxprob_choices]
    results = []
    
    gcs = location_set
    for geography in geographies:
        geo = data_objects.translate(geography)
        
        #get geo_id for observed agents
        gc_index = gcs.get_id_index(observed_choices_id)
        if geo.id_name[0] not in gcs.get_attribute_names():
            gcs.compute_variables(geo.id_name[0], resources=data_objects)
        geo_ids_obs = gcs.get_attribute(geo.id_name[0])[gc_index]
        
#        obs = copy.deepcopy(agent_set)
#        obs.subset_by_index(agents_index)
#        obs.set_values_of_one_attribute(gcs.id_name[0], observed_choices_id)
        #resources.merge({"household": obs}) #, "gridcell": gcs, "zone": zones, "faz":fazes})
#        obs.compute_variables(geo.id_name[0], resources=resources)
#        obs_geo_ids = obs.get_attribute(geo.id_name[0])
        
        #get geo_id for simulated agents
        geo_ids_sim = gcs.get_attribute(geo.id_name[0])[choices_index]        
        
        #sim = copy_dataset(obs)
        #sim.set_values_of_one_attribute(gcs.id_name[0], gcs.get_id_attribute()[mc_choices_index]) 
        #resources.merge({"household": sim})
    
        geo_size = geo.size()
        myids = geo.get_id_attribute()
        
        pred_matrix = zeros((geo_size, geo_size))
        p_success = zeros((geo_size,)).astype(Float32)
        
        f = 0
        for geo_id in myids:
            ids = geo_ids_sim[where(geo_ids_obs == geo_id)] #get simulated geo_id for agents observed in this geo_id
            #resources.merge({"agents_index": agents_index_in_geo, "agent":sim})
            what = ones(ids.size())
            pred_matrix[f] = array(nd_image_sum(what, labels=ids, index=myids))
            print pred_matrix[f]
            if sum(pred_matrix[f]) > 0:
                p_success[f] = float(pred_matrix[f, f])/sum(pred_matrix[f])
    
            #sim.increment_version(gcs.id_name[0])  #to trigger recomputation in next iteration
            f += 1
            
        print p_success
        results.append((pred_matrix.copy(), p_success.copy()))
        
    return results