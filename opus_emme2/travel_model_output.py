# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from urbansim.datasets.node_travel_data_dataset import NodeTravelDataDataset
from numpy import zeros, float32, indices, round_, concatenate
from opus_core.storage_factory import StorageFactory
from os.path import join
import os, shutil, sys, tempfile

class TravelModelOutput(object):
    """
    A class to access the output of emme/2 travel models.
    Can be used to get the values of any matrix in an emme/2 data bank.
    """
    def __init__(self, emme_cmd='emme2'):
        self.emme_cmd = emme_cmd
        
    def get_travel_data_set(self, zone_set, matrix_attribute_name_map, bank_path, out_storage=None, matrices_created=False):
        """
        Returns a new travel data set containing the given set of emme/2 matrices 
        populated from the emme/2 data bank.  The columns in the travel data set are 
        those given in the attribute name of the map.
        If matrices_created is True, it is assumed that the matrices files are already created in the bank_path.
        """
        # Compute the from and to zone sets
        nzones = zone_set.size()
        comb_index = indices((nzones,nzones))
                                       
        table_name = 'storage'
        in_storage = StorageFactory().get_storage('dict_storage')
        in_storage.write_table(
                table_name=table_name,
                table_data={
                    'from_zone_id':zone_set.get_id_attribute()[comb_index[0].ravel()],
                    'to_zone_id':zone_set.get_id_attribute()[comb_index[1].ravel()],
                    }
            )
                                       
        travel_data_set = TravelDataDataset(in_storage=in_storage, 
            in_table_name=table_name, out_storage=out_storage)
        travel_data_set.load_dataset_if_not_loaded()
        max_zone_id = zone_set.get_id_attribute().max()
        for matrix_name in matrix_attribute_name_map.keys():
            self._put_one_matrix_into_travel_data_set(travel_data_set, max_zone_id, matrix_name, 
                                                     matrix_attribute_name_map[matrix_name], bank_path, matrices_created)
        return travel_data_set
    
    def get_node_travel_data_set(self, matrix_attribute_name_map, bank_path, out_storage=None):
        """
        Returns a new node travel data set containing the given set of emme/2 matrices 
        populated from the emme/2 data bank.  The columns in the travel data set are 
        those given in the attribute name of the map.
        """
                                       
        table_name = 'storage'
        in_storage = StorageFactory().get_storage('dict_storage')
        in_storage.write_table(
                table_name=table_name,
                table_data={
                    'from_node_id':array([], dtype="int32"),
                    'to_node_id':array([], dtype="int32")
                    }
            )
                                       
        node_travel_data_set = NodeTravelDataDataset(in_storage=in_storage, 
            in_table_name=table_name, out_storage=out_storage)

        for file_name in matrix_attribute_name_map.keys():
            self._put_matricies_from_one_file_into_node_travel_data_set(node_travel_data_set, file_name, 
                                                     matrix_attribute_name_map[file_name], bank_path)
        return node_travel_data_set
           
    def _get_matrix_into_data_file(self, matrix_name, max_zone_id, bank_path, file_name="_one_matrix.txt"):
        """
        Get from the emme/2 data bank, this matrix's data for zones
        1 .. max_zone_id.
        """
        # generate a random file name
        temp_macro_file_name = tempfile.NamedTemporaryFile().name
        macro = self._create_emme2_macro_to_extract_this_matrix(matrix_name, max_zone_id, file_name)
        try:
            f = open(temp_macro_file_name, "w")
            f.write(macro)
            f.flush()
            f.close()
            self.run_emme2_macro(os.path.join(os.getcwd(), temp_macro_file_name), bank_path)
        finally:
            os.remove(temp_macro_file_name)
            
    def run_emme2_macro(self, macro_path, bank_path, scenario_number=-1, output_file=None, append_to_output=True):
        """
        Runs this emme/2 macro in the bank specified.
        """
        logger.start_block('Running emme2 macro %s in bank at %s' %
                           (macro_path, bank_path))
        # generate a random file name
        temp_macro_file_name = tempfile.NamedTemporaryFile().name
        prior_cwd = os.getcwd()
        if output_file is None:
            out = ""
        else:
            out = "> %s" % output_file
            if append_to_output:
                out = " >%s" % out
        try:
            os.chdir(bank_path)
            shutil.copy(macro_path, temp_macro_file_name)
            cmd = "%s 000 -m %s" % (self.emme_cmd, temp_macro_file_name)
            if scenario_number != -1:
                cmd = "%s %s" % (cmd, scenario_number)
            cmd = "%s%s" % (cmd, out)
            logger.log_status(cmd)
            if os.system(cmd):
                raise StandardError("Problem with simulation")
        finally:
            os.remove(temp_macro_file_name)
            os.chdir(prior_cwd)
            logger.end_block()
            
    def _put_one_matrix_into_travel_data_set(self, travel_data_set, max_zone_id, matrix_name, attribute_name, bank_path,
                                             matrices_created=False):
        """
        Adds to the given travel_data_set the data for the given matrix
        that is in the emme/2 data bank.
        """
        logger.start_block('Copying data for matrix %s into variable %s' %
                           (matrix_name, attribute_name))
        try:
            if not matrices_created:
                self._get_matrix_into_data_file(matrix_name, max_zone_id, bank_path)
                file_name = "_one_matrix.txt"
            else:
                file_name = "%s_one_matrix.txt" % matrix_name
            file_contents = self._get_emme2_data_from_file(join(bank_path, file_name))
            
            travel_data_set.add_primary_attribute(data=zeros(travel_data_set.size(), dtype=float32), name=attribute_name)
            for line in file_contents:
                from_zone_id, to_zone_id, value = str.split(line)
                zone_index = travel_data_set.get_index_by_origin_and_destination_ids(from_zone_id, to_zone_id)
                travel_data_set.set_values_of_one_attribute(attribute=attribute_name, values=float(value), index=zone_index)
        finally:
            logger.end_block()
            
    def _put_matricies_from_one_file_into_node_travel_data_set(self, node_travel_data_set, file_name, attribute_map, bank_path):
        """
        Adds to the given node_travel_data_set the data for the given matrix
        that is in the emme/2 data bank.
        """
        full_file_name = join(bank_path, file_name)
        f = open(full_file_name, 'r')
        file_contents = map(str.strip, f.readlines())
        f.close()
        header = str.split(file_contents[0])
        attr_to_map_index = array([i for i in range(len(header)) if header[i] in attribute_map.keys()])
        data = {}
        for idx in attr_to_map_index:
            node_travel_data_set.add_primary_attribute(data=zeros(node_travel_data_set.size(), dtype=float32), name=attribute_map[header[idx]])
            data[attribute_map[header[idx]]] = array([], dtype=float32)
        data['from_node_id'] = array([], dtype='int32')
        data['to_node_id'] = array([], dtype='int32')
        logger.log_status('Copying data from node matricies into variable node travel data set' )
        def try_convert_to_float(x):
            try:
                return float(x)
            except:
                logger.log_warning('Invalid value in %s: %s' % (full_file_name, x))
                return 0
        for line in file_contents[1:len(file_contents)]:
            splitted_line = array(map(lambda x: try_convert_to_float(x), str.split(line)), dtype=float32)
            from_node_id, to_node_id = round_(splitted_line[0:2]).astype("int32")
            try:
                idindex = node_travel_data_set.get_id_index([[from_node_id, to_node_id]]) # this will raise error, if this combination of from_node, to_node is not in the dataset
                for idx in attr_to_map_index:
                    value = splitted_line[idx]
                    node_travel_data_set.set_value_of_attribute_by_id(attribute=attribute_map[header[idx]], value=value, 
                                                             id=(from_node_id, to_node_id))
            except:
                # if this combination of from_node, to_node is not in the dataset, add it to the data
                for idx in attr_to_map_index:
                    value = splitted_line[idx]
                    data[attribute_map[header[idx]]] = concatenate((data[attribute_map[header[idx]]], array([value], dtype=float32)))
                data['from_node_id'] = concatenate((data['from_node_id'], array([from_node_id])))
                data['to_node_id'] = concatenate((data['to_node_id'], array([to_node_id])))

        if data[data.keys()[0]].size > 0:
            node_travel_data_set.add_elements(data, require_all_attributes=False)
        
    def _get_emme2_data_from_file(self, full_file_name):
        """Returns a list of all the lines (stripped) in the file. But only the lines that have data on them
           (they begin with a number)
        """
        f = open(full_file_name, 'r')
        file_contents = map(str.strip, f.readlines())
        f.close()
        return filter(lambda line: len(line) > 0 and str.isdigit(line[0]), file_contents)
                
    def _create_emme2_macro_to_extract_this_matrix(self, matrix_name, max_zone_id, file_name="_one_matrix.txt"):
        """Return an emme/2 macrot that will extract this matrix's values."""
        if sys.platform == 'win32':
            external_command = """if exist %(output_file_name)s erase %(output_file_name)s""" % {"output_file_name":file_name}
        else:
            external_command = """rm -f %(output_file_name)s""" % {"output_file_name":file_name}
        emme2_macro = """
~/ one_matrix.dat
~/ This macro:
~/ 1) Sets the output format to 8.4
~/ 2) Outputs the named full matrix
~/    for the i,j pairs 1-%(max_zone_id)d, 1-%(max_zone_id)d.
~/ 3) - - to the new file trips_and_times_by_mode.dat
~/ 4) And exits both the program and EMME/2
~/
~o=39
~!%(external_command)s
reports=?
3.14
~+|4|2|8,4|y|4|n
~+|1|3
%(matrix_name)s
~+|||y|1,%(max_zone_id)d||1,%(max_zone_id)d||2|%(output_file_name)s
q
q
        """
        return emme2_macro % {
            "external_command": external_command,
            "matrix_name":matrix_name, 
            "max_zone_id":max_zone_id,
            "output_file_name":file_name
            }
        
#================================================================================
# Tests
#
# NOTE: 
# Some of these tests can only be run on a machine that has an actual emme/2 
# data bank.
#================================================================================
from opus_core.tests import opus_unittest
from numpy import array, ones
from opus_core.misc import write_to_text_file, write_table_to_text_file
from urbansim.datasets.zone_dataset import ZoneDataset

class TravelModelOutputTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self._has_travel_model = os.environ.has_key('TRAVELMODELROOT')
        if self._has_travel_model:
            self.real_bank_path = os.path.join(os.environ['TRAVELMODELROOT'], 
                                               'baseline_travel_model_psrc',
                                               '2010_06',
                                               'bank1')
        
    def test_get_macro(self):
        from string import find, count
        tm_output = TravelModelOutput()
        macro = tm_output._create_emme2_macro_to_extract_this_matrix('xoxoxo', 9999)
        self.assert_(find(macro, 'xoxoxo'))
        self.assertEqual(count(macro, '9999'), 4)
        
    def test_running_emme2_to_get_matrix(self):
        if self._has_travel_model:
            tm_output = TravelModelOutput()
            tm_output._get_matrix_into_data_file('au1tim', 80, self.real_bank_path)
        else:
            logger.log_warning('Test skipped. TRAVELMODELROOT environment '
                'variable not found.')
        
    def test_getting_emme2_data_into_travel_data_set(self):
        if self._has_travel_model:
            zone_storage = StorageFactory().get_storage('dict_storage')
            zone_table_name = 'zone'
            zone_storage.write_table(
                    table_name=zone_table_name,
                    table_data={
                        'zone_id': array([1,2,3]),
                        'travel_time_to_airport': ones((3,)),
                        'travel_time_to_cbd': ones((3,))
                        },
                )
                         
            travel_data_storage = StorageFactory().get_storage('dict_storage')
            travel_data_table_name = 'travel_data'
            travel_data_storage.write_table(
                    table_name=travel_data_table_name,
                    table_data={
                        'from_zone_id':array([1,1,1,2,2,2,3,3,3]),
                        'to_zone_id':array([1,2,3,1,2,3,1,2,3]),
                        },
                )
            
            travel_data_set = TravelDataDataset(in_storage=travel_data_storage, in_table_name=travel_data_table_name)
            travel_data_set.get_id_attribute()
            tm_output = TravelModelOutput()
            tm_output._get_matrix_into_data_file('au1tim', 3, self.real_bank_path)
            tm_output._put_one_matrix_into_travel_data_set(travel_data_set, 
                                                               3,
                                                               'au1tim', 
                                                               'single_vehicle_to_work_travel_time',
                                                               self.real_bank_path)
            self.assertEqual(travel_data_set.get_attribute('single_vehicle_to_work_travel_time').size, 9)
    
        else:
            logger.log_warning('Test skipped. TRAVELMODELROOT environment '
                'variable not found.')

    def test_getting_several_emme2_data_into_travel_data_set(self):
        if self._has_travel_model:
            num_zones = 30

            zone_storage = StorageFactory().get_storage('dict_storage')
            zone_table_name = 'zone'
            zone_storage.write_table(
                    table_name=zone_table_name,
                    table_data={
                        'zone_id':array(range(num_zones))+1
                        },
                )
            
            zone_set = ZoneDataset(in_storage=zone_storage, in_table_name=zone_table_name)
            matrix_attribute_map = {'au1tim':'single_vehicle_to_work_travel_time',
                                    'biketm':'bike_to_work_travel_time'}
            tm_output = TravelModelOutput()
            travel_data_set = tm_output.get_travel_data_set(zone_set, matrix_attribute_map, self.real_bank_path)
            self.assertEqual(travel_data_set.get_attribute('single_vehicle_to_work_travel_time').size, num_zones*num_zones)
            self.assertEqual(travel_data_set.get_attribute('bike_to_work_travel_time').size, num_zones*num_zones)
            from numpy import ma
            self.assertEqual(False,
                             ma.allclose(travel_data_set.get_attribute('single_vehicle_to_work_travel_time'), 
                                      travel_data_set.get_attribute('bike_to_work_travel_time')))
        else:
            logger.log_warning('Test skipped. TRAVELMODELROOT environment '
                'variable not found.')

    def test_get_node_data_into_node_travel_data_set(self):
        temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        file1 = 'report1'
        temp_file1 = os.path.join(temp_dir, file1)
        write_to_text_file(temp_file1, array(['inode', 'jnode', 'timau', '@corr', 'len', 'result']), delimiter=' ')
        write_table_to_text_file(temp_file1, array([[1,2, 35.6, 4, 1.2, 0], 
                                                    [2,1, 23.5, 3, 0.3,100], 
                                                    [4,10, 2.1, 3, 0.5, 10],
                                                    [3,1, 15.8, 4, 1.1, 5] ]), delimiter = ' ', mode='a')
        file2 = 'report2'
        temp_file2 = os.path.join(temp_dir, file2)
        write_to_text_file(temp_file2, array(['inode', 'jnode', 'volau', 'result']), delimiter=' ')
        write_table_to_text_file(temp_file2, array([[1,2, 110, 0], 
                                                   [3,1, 350, 400], 
                                                   [5,4, 200, 200]]), delimiter = ' ', mode='a')
        
        node_matrix_attribute_map = {file1: {
                                             'timau':'travel_time',
                                             'len':'distance',
                                             '@corr': 'corridor'
                                             },
                                     file2: {
                                             'volau': 'travel_volume'
                                             }
                                     }
        tm_output = TravelModelOutput()
        node_travel_data_set = tm_output.get_node_travel_data_set(node_matrix_attribute_map, temp_dir)
        # size should be 5, since there are 5 unique combinations of from_node, to_node
        self.assertEqual(node_travel_data_set.size(), 5)
        # the dataset should have 6 attributes
        self.assertEqual(len(node_travel_data_set.get_known_attribute_names()), 6)
        self.assertEqual('travel_time' in node_travel_data_set.get_known_attribute_names(), True)
        self.assertEqual('distance' in node_travel_data_set.get_known_attribute_names(), True)
        self.assertEqual('corridor' in node_travel_data_set.get_known_attribute_names(), True)
        self.assertEqual('travel_volume' in node_travel_data_set.get_known_attribute_names(), True)
        self.assertEqual('from_node_id' in node_travel_data_set.get_known_attribute_names(), True)
        self.assertEqual('to_node_id' in node_travel_data_set.get_known_attribute_names(), True)
        # check values of one node
        node = node_travel_data_set.get_data_element_by_id((3,1))
        self.assertEqual(node.corridor, 4)
        self.assertEqual(node.travel_volume, 350)
        shutil.rmtree(temp_dir) 
        
if __name__=='__main__':
    opus_unittest.main()