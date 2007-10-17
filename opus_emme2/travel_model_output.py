#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.misc import get_temp_file_name
from numpy import zeros, float32, indices
from opus_core.storage_factory import StorageFactory
from os.path import join
import os, shutil

class TravelModelOutput(object):
    """
    A class to access the output of emme/2 travel models.
    Can be used to get the values of any matrix in an emme/2 data bank.
    """
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
        travel_data_set.get_id_attribute().max()
        max_zone_id = zone_set.get_id_attribute().max()
        for matrix_name in matrix_attribute_name_map.keys():
            self._put_one_matrix_into_travel_data_set(travel_data_set, max_zone_id, matrix_name, 
                                                     matrix_attribute_name_map[matrix_name], bank_path, matrices_created)
        return travel_data_set
           
    def _get_matrix_into_data_file(self, matrix_name, max_zone_id, bank_path):
        """
        Get from the emme/2 data bank, this matrix's data for zones
        1 .. max_zone_id.
        """
        temp_macro_file_name = get_temp_file_name()
        macro = self._create_emme2_macro_to_extract_this_matrix(matrix_name, max_zone_id)
        try:
            f = open(temp_macro_file_name, "w")
            f.write(macro)
            f.flush()
            f.close()
            self.run_emme2_macro(os.path.join(os.getcwd(), temp_macro_file_name), bank_path)
        finally:
            os.remove(temp_macro_file_name)
            
    def run_emme2_macro(self, macro_path, bank_path, scenario_number=-1):
        """
        Runs this emme/2 macro in the bank specified.
        """
        logger.start_block('Running emme2 macro %s in bank at %s' %
                           (macro_path, bank_path))
        temp_macro_file_name = get_temp_file_name()
        prior_cwd = os.getcwd()
        try:
            os.chdir(bank_path)
            shutil.copy(macro_path, temp_macro_file_name)
            cmd = "emme2 000 -m %s" % (temp_macro_file_name)
            if scenario_number != -1:
                cmd = "%s %s" % (cmd, scenario_number)
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
            file_contents = self._get_emme2_data_from_file(join(bank_path, "_one_matrix.txt"))
            
            travel_data_set.add_primary_attribute(data=zeros(travel_data_set.size(), dtype=float32), name=attribute_name)
            for line in file_contents:
                from_zone_id, to_zone_id, value = str.split(line)
                travel_data_set.set_value_of_attribute_by_id(attribute=attribute_name, value=float(value), 
                                                             id=(int(from_zone_id), int(to_zone_id)))
        finally:
            logger.end_block()
        
    def _get_emme2_data_from_file(self, full_file_name):
        """Returns a list of all the lines (stripped) in the file. But only the lines that have data on them
           (they begin with a number)
        """
        f = open(full_file_name, 'r')
        file_contents = map(str.strip, f.readlines())
        f.close()
        return filter(lambda line: len(line) > 0 and str.isdigit(line[0]), file_contents)
                
    def _create_emme2_macro_to_extract_this_matrix(self, matrix_name, max_zone_id):
        """Return an emme/2 macrot that will extract this matrix's values."""
        emme2_macro = """
~/ one_matrix.dat
~/ This macro:
~/ 1) Sets the output format to 8.4
~/ 2) Outputs the named full matrix
~/    for the i,j pairs 1-%(max_zone_id)d, 1-%(max_zone_id)d.
~/ 3) - - to the new file trips_and_times_by_mode.dat
~/ 4) And exits both the program and EMME/2
~/
~!if exist %(output_file_name)s erase %(output_file_name)s
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
            "matrix_name":matrix_name, 
            "max_zone_id":max_zone_id, 
            "output_file_name":"_one_matrix.txt",
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
        if self._has_travel_model:
            from string import find, count
            tm_output = TravelModelOutput()
            macro = tm_output._create_emme2_macro_to_extract_this_matrix('xoxoxo', 9999)
            self.assert_(find(macro, 'xoxoxo'))
            self.assertEqual(count(macro, '9999'), 4)
        else:
            logger.log_warning('Test skipped. TRAVELMODELROOT environment '
                'variable not found.')
        
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

if __name__=='__main__':
    opus_unittest.main()