#==unittest script==#
import os, sys
import unittest
import configure_path
from dataset import DataSet, SetAttribute
from gridcellset.gridcells import GridcellSet
from householdset.households import HouseholdSet
from opus_sampling import SamplingToolbox

class SamplingToolboxTest(unittest.TestCase):
    dirEugene = os.environ['OPUSHOME'] + "/UrbanSim4/data/flt/Eugene_1980_baseyear"
#    storage_dictionary = Resources({"in_base":dirEugene})
#    in_storage = StorageCreator().get_storage("Flt", storage_dictionary)
#    resources = Resources({"in_storage":in_storage})
#    gcs = GridcellSet(resources)
    gcs = GridcellSet(in_storage_type = "flt", in_base = dirEugene)
    gcs.load_dataset(attributes=SetAttribute.ALL)
    hhs = HouseholdSet(in_storage_type = "flt", in_base = dirEugene)
    hhs.load_dataset(attributes=SetAttribute.ALL)

    def testSRS_Sampling(self):
        n = 500
        st = SamplingToolbox(random_seed=(1,1))
        st.sample_individuals(self.gcs, n)
        print st.N
        print st.sampled_individual_index
        self.assertEqual(len(st.sampled_individual_index), n, msg ="Number of individual sampled not equal to the specified arguments")

    def testWeighted_Sampling(self):
        n = 500
        st = SamplingToolbox(random_seed=(1,1))
        weight_array = self.gcs.get_attribute('residential_units')
        st.sample_individuals(self.gcs, n, sampling_method='weighted', weight_array=weight_array)
        print st.N
        print st.sampled_individual_index
        self.assertEqual(len(st.sampled_individual_index), n, msg ="Number of individual sampled not equal to the specified arguments")

    def testStratifited_Sampling(self):
        n = 2
        st = SamplingToolbox(random_seed=(1,1))
        strata_array = self.gcs.get_attribute('zone_id')        
        st.sample_individuals(self.gcs, n, sampling_method='stratified', strata_array=strata_array, \
                     sample_rate=.1) #, weight_attribute='residential_units')
        print st.N
        print st.sampled_individual_index
        print self.gcs.get_attribute('zone_id')[st.sampled_individual_index]
        self.assertEqual(len(st.sampled_individual_index), st.N, msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_SRS_Sampling_by_column(self):
        j = 10
         st = SamplingToolbox(self.hhs)
        st.sample_choiceset(self.gcs, J=j, sampling_method='SRS')
        self.assertEqual(st.sampled_choiceset_index.shape, (self.hhs.size(), j), msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_Weighted_Sampling_by_column(self):
        j = 10
         st = SamplingToolbox(self.hhs)
        weight_array = self.gcs.get_attribute('residential_units')    
        ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='weighted', weight_array=weight_array)
        self.assertEqual(ASample.shape, (self.hhs.size(), j), msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_Stratified_Sampling_by_column(self):
        n=1000; j = 10
         st = SamplingToolbox()
        weight_array = self.hhs.get_attribute('persons')
        strata_array = self.gcs.get_attribute('zone_id')                
        st.sample_individuals(self.hhs, n, sampling_method='weighted', weight_array=weight_array)        
        ASample = st.sample_choiceset(self.gcs, J=1, sampling_method='stratified', strata_array= strata_array) #,weight_attribute='residential_units')
        print "%s*%s" % (st.N, st.J)
        self.assertEqual(ASample.shape, (st.N, st.J), msg ="Number of individual sampled not equal to the specified arguments")

#      def testAlt_SRS_Sampling_by_row(self):
#         n = 5; j = 10
#         st = SamplingToolbox()
#         ISample = st.sample_individual(self.hhs, n)
#          ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='SRS')
#         self.assertEqual(ASample.shape, (n, j), msg ="Number of individual sampled not equal to the specified arguments")

#      def testAlt_Weighted_Sampling_by_row(self):
#         n = 5; j = 10
#         st = SamplingToolbox()
#         ISample = st.sample_individual(self.hhs, n)
#               weight_array = self.gcs.get_attribute('persons')
#          ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='weighted', weight_array=weight_array)
#         self.assertEqual(ASample.shape, (n, j), msg ="Number of individual sampled not equal to the specified arguments")
        
if __name__ == "__main__":
    unittest.main()
