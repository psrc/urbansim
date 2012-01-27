# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.rate_based_model import RateBasedModel
from opus_core.logger import logger
from numpy import where, array, zeros, cumsum, searchsorted, logical_and
from numpy.random import random, uniform

class MortalityModel(RateBasedModel):
    """
    """
    model_name = "Mortality Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name = person_set.get_dataset_name()
        hh_ds_name = household_set.get_dataset_name()
        index = RateBasedModel.run(self, person_set, resources=resources)
        logger.log_status("%s deaths occurred (before accounting for adults saved to prevent orphans)" % (index.size) )

        #avoid orphaning children before we handle them in an adoption model
        person_set.add_attribute(name='mortality_flag', data=zeros(person_set.size(), dtype='b'))
        person_set['mortality_flag'][index] = True

        #identify such households
        person_set.compute_variables('is_adult = person.age > 17')
        household_set.compute_variables('adults = household.aggregate(person.is_adult)')
        person_set.compute_variables("adult_death = person.mortality_flag * person.is_adult")
        household_set.compute_variables("adult_deaths = household.aggregate(person.adult_death)")
        full_adult_mortality = household_set.compute_variables("death_of_all_adults = numpy.logical_and(household.adult_deaths>=1, " + 
                                                                                                       "household.adult_deaths == household.adults)")
        children_at_risk = household_set.compute_variables("children_at_risk=household.aggregate(numpy.logical_not(person.mortality_flag) * (person.age <= 17)) > 0 ")
        hh_at_risk = household_set.compute_variables("at_risk = household.death_of_all_adults * household.children_at_risk")
        idx_hh_at_risk = where(hh_at_risk)[0]
        if idx_hh_at_risk.size > 0:
            #sample 1 adult per household to keep for households with children at risk 
            prob_to_keep = person_set.compute_variables("safe_array_divide((person.adult_death).astype('f'), " + 
                                                                           "person.disaggregate(household.adult_deaths))")

            for idx_hh in idx_hh_at_risk:
                hh_id = household_set['household_id'][idx_hh]
                ps_of_this_hh = where( logical_and(person_set['household_id'] == hh_id,
                                                   person_set['adult_death']
                                                   ))[0]
                if ps_of_this_hh.size == 1:
                    person_set['mortality_flag'][ps_of_this_hh] = False
                else:
                    r = uniform(0,1); cumprob = cumsum(prob_to_keep[ps_of_this_hh])
                    idx_adult_to_keep = searchsorted(cumprob, r)
                    person_set['mortality_flag'][ps_of_this_hh[idx_adult_to_keep]] = False

        idx = where( person_set['mortality_flag'] )[0]
        person_set.delete_one_attribute('mortality_flag')

        logger.log_status("Removing %s records from %s dataset" % (idx.size, person_set.get_dataset_name()) )
        logger.log_status("%s deaths occurred after saving some adults to prevent orphans" % (idx.size) )
        person_set.remove_elements(idx)
        
        ##remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)

        ## it would work better to convert them to computed variables
        ##Update the household table's persons attribute to account for deaths
        if 'persons' in household_set.get_primary_attribute_names():
            persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
            household_set.modify_attribute('persons', persons)
        ##Update the household table's children attribute to account for child deaths
        if 'children' in household_set.get_primary_attribute_names():
            children = household_set.compute_variables('_children = household.aggregate(person.age<18)')
            household_set.modify_attribute('children', children)
        ##Assign "head of the household" status
        if 'head_of_hh' in person_set.get_primary_attribute_names():
            person_set.add_attribute(name='head_score', data=person_set.compute_variables('(person.age)*1.0 + 3.0*(person.education) + exp(-sqrt(sqrt(sqrt(.5*(person.person_id)))))'))
            highest_score = person_set.compute_variables('_high_score = (person.disaggregate(household.aggregate(person.head_score, function=maximum)))*1')
            head_of_hh = person_set.compute_variables('_head_of_hh = (person.head_score == _high_score)*1')
            person_set.modify_attribute('head_of_hh', head_of_hh)
            person_set.delete_one_attribute('head_score')   
        ##Update the age_of_head attribute in the household table to reflect the age of new heads of the household and to reflect the aging of existing heads of household.
        if 'age_of_head' in household_set.get_primary_attribute_names():
            age_of_head = household_set.compute_variables('_age_of_head = household.aggregate(person.head_of_hh * person.age)')
            household_set.modify_attribute('age_of_head', age_of_head)
        ##When a person's spouse dies, change the person's marriage_status from married to widowed. (This has implications for the household formation model)
        ##Note that a marriage_status=1 is supposed to indicate being married to a spouse who resides in the same household.  In the case of marriage_status=2, which indicates married to a spouse who does not live in the household, we cannot tell when someone's spouse dies.  Widowed (marriage_status = 3) includes men.
        if 'marriage_status' in person_set.get_primary_attribute_names():
            widowed = person_set.compute_variables('_last_spouse = (((person.disaggregate(household.aggregate(person.marriage_status == 1)))==1)*1) * ((person.marriage_status == 1)*1)')
            index_widow = where(widowed==1)[0]
            if index_widow.size > 0:
                person_set.modify_attribute('marriage_status', array(index_widow.size*[3]), index_widow)


#from opus_core.tests import opus_unittest
#from opus_core.misc import ismember
#from opus_core.datasets.dataset_pool import DatasetPool
#from opus_core.resources import Resources
#from numpy import array, logical_and, int32, int8, ma, all, allclose
#from scipy import histogram
#from opus_core.datasets.dataset import Dataset
#from urbansim.datasets.household_dataset import HouseholdDataset
#from opus_core.datasets.dataset import Dataset
#from opus_core.storage_factory import StorageFactory
#from itertools.chain import from_iterable
#
#class Tests(opus_unittest.OpusTestCase):
#
#    def setUp(self):
#        households_data = {
#            "household_id":arange(33)+1,
#            "age_of_head": array([]),
#            "persons": array(6*[2] + 2*[3] + 3*[1] + 4*[6] + 2*[1] + 5*[4] +
#                                3*[1]+ 8*[5], dtype=int8),
#            }
#        
#        total_persons = households_data['persons'].sum()
#        persons_data = {
#            "person_id":arange(total_persons)+1,
#            "household_id": array( list(from_iterable([[i] * p for i,p in zip(households_data['household_id'], households_data['persons'])])) ),
#            "member_id": array( list(from_iterable([range(1,p+1) for p in households_data['persons']])) ),
#            "age": array( list(from_iterable([a]+list(randint(0, a, size=p-1)) for a,p in zip(households_data['age_of_head'], households_data['persons']))) ),
#            "job_id": zeros(total_persons)
#            }
#
#        storage = StorageFactory().get_storage('dict_storage')
#        storage.write_table(table_name='hh_set', table_data=households_data)
#        self.hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')
#        storage.write_table(table_name='person_set', table_data=persons_data)
#        self.persons_set = Dataset(in_storage=storage, in_table_name='person_set', dataset_name='person')
#
#    def test_mortality_model_avoids_orhpans(elf):
#
#        mortality_rates = {
#            "year": array([2000, 2000, 2001, 2001]),
#            "age_min": array([ 50,  0,  50,  0]),
#            "age_max": array([100, 49, 100, 49]),
#            "mortality_rate": arange(0.5, 0.5, .8, .8),
#            }
#
#        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
#                           datasets_dict={'household':self.hh_set,
#                                          'person':self.person_set
#                                         })
#        storage = StorageFactory().get_storage('dict_storage')
#        storage.write_table(table_name='mortality_rate', table_data=mortality_rates)
#        model = MortalityModel()
#        model.prepare_for_run(rate_dataset_name='mortality_rate', rate_storage=storage)
#        model.run(self.person_set, 
#                  self.hh_set,
#                  resources=dataset_pool
#                  )
#        
