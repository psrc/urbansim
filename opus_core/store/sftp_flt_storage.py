# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.store.storage import Storage
from shutil import rmtree
from urllib.parse import urlparse
from .file_flt_storage import file_flt_storage, FltError
from opus_core.ssh_client import get_ssh_client, convertntslash
from glob import glob
import tempfile
import stat
import os, re

class sftp_flt_storage(file_flt_storage): 
    """ this class derives from file_flt_storage and handles flt stored on a remote computer through sftp
    """
       
    def __init__(self, storage_location, client_type='paramiko'):
        """
        storage_location = 'sftp://[username:passwd@]my.hostname.com/home/users/cache_dir'
        it is recommended to store sftp user and password in system environment variables or in a security key,
        instead of passing in as plain text.
        """
        server_config = {'port':22}
        o = urlparse(storage_location)
        server_config['hostname'] = o.hostname
        server_config['username'] = o.username or os.environ.get('URBANSIMUSERNAME', None) or os.environ.get('TRAVELMODELUSERNAME', None)
        server_config['password'] = o.password or os.environ.get('URBANSIMPASSWORD', None) or os.environ.get('TRAVELMODELPASSWORD', None)
        if o.port is not None:
            server_config['port'] = o.port
        
        self.ssh_client = get_ssh_client(ssh_server_config=server_config, client_type=client_type)
        
        self._base_directory_remote = o.path
        self._base_directory = self._base_directory_local = tempfile.mkdtemp(prefix='opus_tmp')


    def __del__(self):
        rmtree(self._get_base_directory())
        
    def has_table(self, table):
        if self.ssh_client.exists_remotely(self._get_base_directory_remote()):
            files = self.ssh_client.listdir(self._get_base_directory_remote())
            if table in files:
                return True
        return False
        
    def get_storage_location(self):
        return self._base_directory_local

    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        remote_dataset_path = convertntslash( os.path.join(self._get_base_directory_remote(), table_name) )
        local_dataset_path = self._get_base_directory()
        self.ssh_client.mget( remote_dataset_path,  local_dataset_path)

        return file_flt_storage.load_table(self, table_name, column_names=column_names, lowercase=lowercase)
    
    def get_column_names(self, table_name, lowercase=True):
        #same as in file_flt_storage
        files = self._get_files(table_name)
        
        result = [file.get_short_name() for file in files]
        if lowercase:
            result = [file.lower() for file in result]

        return result
    
    def _get_base_directory(self):
        return self._base_directory_local

    def _get_base_directory_remote(self):
        return self._base_directory_remote
    
    def get_table_names(self):
        dataset_path = convertntslash(self._get_base_directory_remote())
        if self.ssh_client.exists_remotely(dataset_path):
            result = []
            file_paths = self.ssh_client.glob(dataset_path+'/*')
            for file_path in file_paths:
                if self.ssh_client.isdir(file_path):
                    file_name = os.path.basename(file_path)
                    if len(self.get_column_names(file_name))>0:
                        result.append(file_name)
            return result
        else:
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
    
    def write_table(self, table_name, table_data):
        """
        'table_name' specifies the subdirectory relative to base directory. 
        'table_data' is a dictionary where keys are the column names and values 
            are value arrays of the corresponding columns. 
        """

        unused_column_size, column_names = self._get_column_size_and_names(table_data)
        
        local_dir = os.path.join(self._get_base_directory(), table_name)
        remote_dir = convertntslash( os.path.join(self._get_base_directory_remote(),table_name ))
        remote_base_dir = convertntslash( self._get_base_directory_remote() )

        if not self.ssh_client.exists_remotely(remote_dir):
            self.ssh_client.makedirs(remote_dir)
        else:
            ## handle existing files with column_name
            existing_files = self._get_remote_files(table_name=table_name)
            existing_file_short_names = [file.get_short_name() for file in existing_files]

            for column_name in column_names:
                n = existing_file_short_names.count(column_name)
                if n == 0:
                    continue
                elif n == 1:
                    i = existing_file_short_names.index(column_name)
                    self.ssh_client.remove(existing_files[i].get_name())
                elif n > 1:
                    message = "Column '%s' has multiple files with different file extensions:\n" % column_name
                    message += "Either the process of copying files into this directory is flawed, or there is a bug in Opus."
                    raise FltError(message)   
                    
        file_flt_storage.write_table(self, table_name, table_data)
        
        self.ssh_client.mput(local_dir, remote_base_dir)
        
    def _get_files(self, table_name=''):
        return self._get_local_files(table_name=table_name)

    def _get_local_files(self, table_name=''):
        dataset_path = os.path.join(self._get_base_directory(), table_name)
                                    
        remote_files = self._get_remote_files(table_name=table_name)
        return [self.storage_file(os.path.join(dataset_path, os.path.basename(remote_file.get_name()))) for remote_file in remote_files]
    
    def _get_remote_files(self, table_name=''):        
        dataset_path = convertntslash( os.path.join(self._get_base_directory_remote(), table_name) )
        if self.ssh_client.exists_remotely(dataset_path):
            dataset_file_pattern = dataset_path + '/*.*'
            file_names = self.ssh_client.glob(dataset_file_pattern)
            return [self.storage_file( name ) for name in file_names]
        else:
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
    
    def listdir_in_base_directory(self):
        return self.ssh_client.listdir( self._get_base_directory_remote() )


def redirect_sftp_url_to_local_tempdir(filename):
    """ if filename is a remote sftp URL, redirect file to local tempdir
    For log file location
    """
    if type(filename) == str and re.search("^sftp://", filename):
        local_filename = urlparse(filename).path
        local_filename = os.path.join(tempfile.gettempdir(), 
                                      os.path.basename( os.path.dirname(local_filename) ), 
                                      os.path.basename(local_filename))
        if not os.path.exists( os.path.dirname(local_filename) ):
            os.makedirs( os.path.dirname(local_filename) )
        
        return local_filename
    else:
        return filename
        
        

import os, sys
from opus_core.tests import opus_unittest
from opus_core.opus_package import OpusPackage
from opus_core.store.storage import TestStorageInterface
from opus_core.tests.utils.cache_extension_replacements import replacements
from numpy import array, fromfile, int32
from shutil import rmtree
from tempfile import mkdtemp
from getpass import getuser

TESTUSERNAME = getuser()
TESTHOSTNAME = 'localhost'

try:
    import paramiko    
except:
    paramiko = None

def skip_test():
    if paramiko is None:
        return True
    ## skip unittest if the connection cannot be authenticated
    sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
    try:
        storage = sftp_flt_storage(sftp_location)
        return False
    except:
        from opus_core.logger import logger 
        logger.log_warning('Skipping sftp_flt_storage unit tests -- no ssh access or could not authenticate.')
        return True

class SftpFltStorageTests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        if skip_test():
            return
        years = [1980, 1981]
        datasets = ['base_year', 'cities']

        opus_core_path = OpusPackage().get_opus_core_path()
        sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
        self.storage = sftp_flt_storage(sftp_location)
        self.remote_temp_dir = self.storage.ssh_client.get_remote_temp_dir()
        self.storage._base_directory_remote = os.path.join(self.remote_temp_dir, 'data', 'test_cache', '1980')

        for year in years:
            local_test_data_path = os.path.join(
                opus_core_path, 'data', 'test_cache', str(year))
            base_directory_remote = os.path.join(self.remote_temp_dir, 'data', 'test_cache', str(year))

            for dataset in datasets:
                local_dir_name = os.path.join(local_test_data_path, dataset)
                remote_dir_name = base_directory_remote
                self.storage.ssh_client.mput(local_dir_name, remote_dir_name)
            
    def tearDown(self):
        if skip_test():
            return
        if self.storage.ssh_client.exists_remotely(self.remote_temp_dir):
            self.storage.ssh_client.rmtree(self.remote_temp_dir)
    
    def test_get_files(self):
        if skip_test():
            return
        expected = ['city_id', 'city_name']
        expected.sort()
        actual = self.storage.get_column_names('cities')
        actual.sort()
        self.assertEqual(expected, actual)
        
    def test_load_table(self):
        if skip_test():
            return
        expected = {
            'city_id': array([3, 1, 2], dtype='<i4'),
            'city_name': array(['Unknown', 'Eugene', 'Springfield']),
            }
        actual = self.storage.load_table('cities')
        self.assertDictsEqual(expected, actual)
        
    def test_get_table_names_1981(self):
        if skip_test():
            return
        self.storage._base_directory_remote = convertntslash( os.path.join(self.remote_temp_dir, 'data', 'test_cache', '1981') )
        expected = ['base_year', 'cities']
        actual = self.storage.get_table_names()
        expected.sort()
        actual.sort()
        self.assertEqual(expected, actual)
        
class StorageWriteTests(TestStorageInterface):

    def setUp(self):
        if skip_test():
            return
        opus_core_path = OpusPackage().get_opus_core_path()
        local_test_data_path = os.path.join(
            opus_core_path, 'data', 'test_cache', '1980')
        sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
        self.storage = sftp_flt_storage(sftp_location)
        self.remote_temp_dir = self.storage.ssh_client.get_remote_temp_dir()
        self.storage._base_directory_remote = self.remote_temp_dir
        self.sftp_location = sftp_location + self.remote_temp_dir
        self.table_name = 'testtable'
            
    def tearDown(self):
        if skip_test():
            return
        if self.storage.ssh_client.exists_remotely(self.remote_temp_dir):
            self.storage.ssh_client.rmtree(self.remote_temp_dir)
            
    def test_write_char_array(self):
        if skip_test():
            return
        expected = array(['string1', 'string227'])
        table_data = {
            'char_column': expected,
            }

        remote_file_name = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, 'char_column.iS9'))
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, 'char_column.iS9')
        
        self.storage.write_table(self.table_name, table_data)
        self.assertTrue(self.storage.ssh_client.exists_remotely(remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, dtype='|S9')
        self.assertTrue((expected==actual).all())
        
    def test_write_int_array(self):
        if skip_test():
            return
        expected = array([100, 70])
        table_data = {
            'int_column': expected,
            }
        # file_name is e.g. 'int_column.li4' for a little-endian 32 bit machine
        file_name = 'int_column.%(endian)si%(bytes)u' % replacements
        # numpy_dtype is e.g. '<i4' for a little-endian 32 bit machine
        numpy_dtype = '%(numpy_endian)si%(bytes)u' % replacements

        remote_file_name = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, file_name))
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, file_name)
        
        self.storage.write_table(self.table_name, table_data)
        self.assertTrue(self.storage.ssh_client.exists_remotely(remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, dtype=numpy_dtype)
        self.assertTrue((expected==actual).all())

        
    def test_write_float_and_boolean_array(self):
        if skip_test():
            return
        expected_float = array([100.17, 70.00])
        expected_bool = array([True, False])
        table_data = {
            'float_column': expected_float,
            'bool_column': expected_bool,
            }
        if sys.byteorder=='little':
            file_name = 'float_column.lf8'
            numpy_ext = '<f8'
        else:
            file_name = 'float_column.bf8'
            numpy_ext = '>f8'


        remote_file_name = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, file_name))
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, file_name)
        
        self.storage.write_table(self.table_name, table_data)
        self.assertTrue(self.storage.ssh_client.exists_remotely(remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, numpy_ext)
        self.assertTrue((expected_float==actual).all())


        remote_file_name = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, 'bool_column.ib1'))
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, 'bool_column.ib1')
        self.storage.write_table(self.table_name, table_data)
        self.assertTrue(self.storage.ssh_client.exists_remotely(remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)        
        actual = fromfile(local_file_name, '|b1')
        self.assertTrue((expected_bool == actual).all())
        
    def test_writing_column_to_file_when_file_of_same_column_name_and_different_type_already_exists(self):
        if skip_test():
            return
        
        column_name= "some_column"
        os.mkdir(os.path.join(self.storage._get_base_directory(), self.table_name)) 
        existing_file = file(os.path.join(self.storage._get_base_directory(), self.table_name, column_name + ".li4"), "w")
        existing_file.close()
        remote_file = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li4"))
        if not self.storage.ssh_client.exists_remotely(os.path.dirname(remote_file)):
            self.storage.ssh_client.makedirs(os.path.dirname(remote_file))
        self.storage.ssh_client.mput(existing_file.name, remote_file)
        
        storage = sftp_flt_storage(storage_location=self.sftp_location)
        ## Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        
        storage.write_table(table_name=self.table_name, table_data=my_data)
        self.assertTrue(not (self.storage.ssh_client.exists_remotely(remote_file)))
        new_remote_file = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li8"))
        self.assertTrue(self.storage.ssh_client.exists_remotely(new_remote_file))

    def test_writing_column_to_file_when_two_files_of_same_column_name_and_different_type_already_exist(self):        
        if skip_test():
            return

        column_name= "some_column"
        os.mkdir(os.path.join(self.storage._get_base_directory(), self.table_name)) 
        existing_file_1 = file(os.path.join(self.storage._get_base_directory() , self.table_name, column_name + ".li4"), "w")
        existing_file_1.close()
        existing_file_2 = file(os.path.join(self.storage._get_base_directory() , self.table_name, column_name + ".bi4"), "w")
        existing_file_2.close()           

        remote_file_1 = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li4"))
        if not self.storage.ssh_client.exists_remotely(os.path.dirname(remote_file_1)):
            self.storage.ssh_client.makedirs(os.path.dirname(remote_file_1))
        self.storage.ssh_client.mput(existing_file_1.name, remote_file_1)
        remote_file_2 = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".bi4"))
        if not self.storage.ssh_client.exists_remotely(os.path.dirname(remote_file_2)):
            self.storage.ssh_client.makedirs(os.path.dirname(remote_file_2))
        self.storage.ssh_client.mput(existing_file_2.name, remote_file_2)

        storage = sftp_flt_storage(storage_location=self.sftp_location)        
        # Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        self.assertRaises(FltError, storage.write_table, self.table_name, my_data)
        new_remote_file = convertntslash(os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li8"))
        self.assertTrue(not (self.storage.ssh_client.exists_remotely(new_remote_file)))        

    def test_write_table_columns_with_different_sizes(self):
        if not skip_test():
            super(StorageWriteTests,self).test_write_table_columns_with_different_sizes()
                
    def test_write_table_no_data_to_write(self):
        if not skip_test():
            super(StorageWriteTests,self).test_write_table_no_data_to_write()
                
if __name__ == '__main__':
    opus_unittest.main()
