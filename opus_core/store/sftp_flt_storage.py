#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.store.storage import Storage
from shutil import rmtree
from urlparse import urlparse
from file_flt_storage import file_flt_storage, FltError
from glob import glob
import tempfile
import stat
import os, re

if os.name == 'nt':
    from nturl2path import pathname2url
    convertpath = pathname2url
else:
    def convertpath(arg):
        return arg

try:
    import paramiko
except ImportError:
    paramiko = None


class sftp_flt_storage(file_flt_storage): 
    """ this class derives from file_flt_storage and handles flt stored on a remote computer through sftp
    """
       
    def __init__(self, storage_location):
        """
        storage_location = 'sftp://[username:passwd@]my.hostname.com/home/users/cache_dir'
        it is recommended to store sftp user and password in system environment variables or in a security key,
        instead of passing in as plain text.
        """
        o = urlparse(storage_location)
        hostname = o.hostname
        username = o.username or os.environ.get('URBANSIMUSERNAME', None) or os.environ.get('TRAVELMODELUSERNAME', None)
        password = o.password or os.environ.get('URBANSIMPASSWORD', None) or os.environ.get('TRAVELMODELPASSWORD', None)
        if o.port is not None:
            port = o.port
        else:
            port = 22
        self._base_directory_remote = o.path
        self._base_directory = self._base_directory_local = tempfile.mkdtemp(prefix='opus_tmp')

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname,
                         port = port,
                         username=username,
                         password=password,
                         pkey=load_key_if_exists())
        #self.ssh._transport.set_keepalive(60)

        self.sftp = self.ssh.open_sftp()

    def __del__(self):
        #if hasattr(self, 'ssh') or hasattr(self, 'sftp'):
        try:
            self.sftp.close()
            self.ssh.close()
        except:
            pass
        rmtree(self._get_base_directory())
        
    def has_table(self, table):
        if exists_remotely(self.sftp, self._get_base_directory_remote()):
            files = self.sftp.listdir(self._get_base_directory_remote())
            if table in files:
                return True
        return False
        
    def get_storage_location(self):
        return self._base_directory_local

    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        local_files = self._get_files(table_name=table_name)
        remote_files = self._get_remote_files(table_name=table_name)
        for i in range(len(local_files)):
            local_file = local_files[i]
            if not os.path.exists(os.path.dirname(local_file.get_name())):
                os.makedirs(os.path.dirname(local_file.get_name()))
            remote_file = remote_files[i]
            self.sftp.get(remote_file.get_name(), local_file.get_name())
            
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
        dataset_path = self._get_base_directory_remote()
        if exists_remotely(self.sftp, dataset_path):
            file_names = self.sftp.listdir(dataset_path)
            return [os.path.basename(name) for name in file_names 
                    if _isdir(self.sftp, name) and len(self.get_column_names(name))>0 ]
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
        remote_dir = convertpath( os.path.join(self._get_base_directory_remote(), table_name) )

        if not exists_remotely(self.sftp, remote_dir):
            _makedirs(self.sftp, remote_dir)
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
                    self.sftp.remove(existing_files[i].get_name())
                elif n > 1:
                    message = "Column '%s' has multiple files with different file extensions:\n" % column_name
                    message += "Either the process of copying files into this directory is flawed, or there is a bug in Opus."
                    raise FltError(message)   
                    
        file_flt_storage.write_table(self, table_name, table_data)
        
        for column_name in column_names:
            local_file = glob(os.path.join(local_dir, '%s.*' % column_name))[0]
            remote_file = convertpath( os.path.join(remote_dir, os.path.basename(local_file) ) )
            self.sftp.put(local_file, remote_file)
        
    def _get_files(self, table_name=''):
        return self._get_local_files(table_name=table_name)

    def _get_local_files(self, table_name=''):
        dataset_path = os.path.join(self._get_base_directory(), table_name)
                                    
        remote_files = self._get_remote_files(table_name=table_name)
        return [self.storage_file(os.path.join(dataset_path, os.path.basename(remote_file.get_name()))) for remote_file in remote_files]
    
    def _get_remote_files(self, table_name=''):        
        dataset_path = convertpath( os.path.join(self._get_base_directory_remote(), table_name) )
        if exists_remotely(self.sftp, dataset_path):
            file_names = self.sftp.listdir(dataset_path)
            return [self.storage_file( convertpath(os.path.join(dataset_path, name))) for name in file_names]
        else:
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
    
    def listdir_in_base_directory(self):
        return self.sftp.listdir( self._get_base_directory_remote() )


def load_key_if_exists(key_file=None):
    key=None
    if key_file is None:  #look into ~/[.]ssh/id_*
        patterns = ['~/.ssh/id_rsa', '~/ssh/id_rsa']
    else:
        patterns = [key_file] + ['~/.ssh/id_rsa', '~/ssh/id_rsa']
        
    key_file = [os.path.expanduser(file) for file in patterns if os.path.exists(os.path.expanduser(file))]
    if len(key_file) != 0:
        key_file = key_file[0]    
        key = paramiko.RSAKey.from_private_key_file(key_file)
    
    return key

def exists_remotely(sftp, name):
    """
    check whether name (file name or directory name) exists on sftp
    sftp is a SFTPClient object in paramiko module
    """
    try:
        stat = sftp.stat(name)
        return True
    except IOError:
        return False
    else:
        raise RuntimeError, "Error checking file status for %s on remote host" % (name)

def _isdir(sftp, name):
    """return True if name is an existing directory
    """
    isdir = False
    if not exists_remotely(sftp, name):
        return isdir
    
    try:
        mode = sftp.lstat(name).st_mode
    except os.error:
        mode = 0
    if stat.S_ISDIR(mode):
        isdir = True
    else:
        isdir = False
    
    return isdir

def _makedirs(sftp, path):
    """ make recursive directories on sftp server
    sftp is a SFTPClient object in paramiko module
    """
    head, tail = os.path.split(path)
    if not exists_remotely(sftp, head):
        _makedirs(sftp, head)
    if not exists_remotely(sftp, path):
        sftp.mkdir(path)

def _rmtree(sftp, path, ignore_errors=False, onerror=None):
    """Recursively delete a directory tree.
    sftp is a SFTPClient object in paramiko module
    (adapted from rmtree in shutils module)
    """
    if ignore_errors:
        def onerror(*args):
            pass
    elif onerror is None:
        def onerror(*args):
            raise
    names = []
    try:
        names = sftp.listdir(path)
    except os.error, err:
        onerror(sftp.listdir, path, sys.exc_info())
    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = sftp.lstat(fullname).st_mode
        except os.error:
            mode = 0
        if stat.S_ISDIR(mode):
            _rmtree(sftp, fullname, ignore_errors, onerror)
        else:
            try:
                sftp.remove(fullname)
            except os.error, err:
                onerror(os.remove, fullname, sys.exc_info())
    try:
        sftp.rmdir(path)
    except os.error:
        onerror(os.rmdir, path, sys.exc_info())

def get_stdout_for_ssh_cmd(ssh, cmdline):
    """get stdout after running cmdline through ssh channel
    ssh is a SSHClient object from paramiko module
    """
    stdin, stdout, stderr = ssh.exec_command(cmdline)
    stderr_msg = stderr.readlines() 
    if len(stderr_msg) > 0:
        raise RuntimeError, "Error encountered executing cmd through ssh:" + stderr_msg

    results = stdout.readlines()
    if len(results)==1:
        results=results[0].strip()
        
    stdin.close(); stdout.close(); stderr.close()
    return results

def get_temp_dir_remote(ssh):
    """
    """
    cmdline = "python -c 'import tempfile, sys; print tempfile.mkdtemp()'"
    return get_stdout_for_ssh_cmd(ssh, cmdline)

def redirect_sftp_url_to_local_tempdir(filename):
    """ if filename is a remote sftp URL, redirect file to local tempdir
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

def skip_test():
    if paramiko is None:
        return True
    ## skip unittest if the connection cannot be authenticated
    sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
    try:
        storage = sftp_flt_storage(sftp_location)
        return True
    except:
        from opus_core.logger import logger 
        logger.log_warning('Skipping sftp_flt_storage unit tests -- no ssh access or could not authenticate.')
        return False

class SftpFltStorageTests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        if skip_test():
            return
        years = [1980, 1981]
        datasets = ['base_year', 'cities']

        opus_core_path = OpusPackage().get_opus_core_path()
        sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
        self.storage = sftp_flt_storage(sftp_location)
        self.remote_temp_dir = get_temp_dir_remote(self.storage.sftp.sock.get_transport())
        self.storage._base_directory_remote = os.path.join(self.remote_temp_dir, 'data', 'test_cache', '1980')

        for year in years:
            local_test_data_path = os.path.join(
                opus_core_path, 'data', 'test_cache', str(year))
            base_directory_remote = os.path.join(self.remote_temp_dir, 'data', 'test_cache', str(year))

            for dataset in datasets:
                local_dir_name = os.path.join(local_test_data_path, dataset)
                remote_dir_name = os.path.join(base_directory_remote, dataset)
                _makedirs(self.storage.sftp, remote_dir_name)
                for file in glob(os.path.join(local_dir_name, '*.*')):
                    short_file_name = os.path.basename(file)
                    self.storage.sftp.put(file, os.path.join(remote_dir_name, short_file_name))
            
    def tearDown(self):
        if skip_test():
            return
        if exists_remotely(self.storage.sftp, self.remote_temp_dir):
            _rmtree(self.storage.sftp, self.remote_temp_dir)
    
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
        self.storage._base_directory_remote = os.path.join(self.remote_temp_dir, 'data', 'test_cache', '1981')
        expected = ['base_year', 'cities']
        actual = self.storage.get_table_names()
        expected.sort()
        actual.sort()
        self.assertEquals(expected, actual)
        
class StorageWriteTests(TestStorageInterface):

    def setUp(self):
        if skip_test():
            return
        opus_core_path = OpusPackage().get_opus_core_path()
        local_test_data_path = os.path.join(
            opus_core_path, 'data', 'test_cache', '1980')
        sftp_location = 'sftp://%s@%s' % (TESTUSERNAME, TESTHOSTNAME)
        self.storage = sftp_flt_storage(sftp_location)
        self.remote_temp_dir = get_temp_dir_remote(self.storage.sftp.sock.get_transport())
        self.storage._base_directory_remote = os.path.join(self.remote_temp_dir)
        self.sftp_location = sftp_location + self.remote_temp_dir
        self.table_name = 'testtable'
            
    def tearDown(self):
        if skip_test():
            return
        if exists_remotely(self.storage.sftp, self.remote_temp_dir):
            _rmtree(self.storage.sftp, self.remote_temp_dir)
            
    def test_write_char_array(self):
        if skip_test():
            return
        expected = array(['string1', 'string227'])
        table_data = {
            'char_column': expected,
            }

        remote_file_name = os.path.join(self.storage._get_base_directory_remote(), self.table_name, 'char_column.iS9')
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, 'char_column.iS9')
        
        self.storage.write_table(self.table_name, table_data)
        self.assert_(exists_remotely(self.storage.sftp, remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, dtype='|S9')
        self.assert_((expected==actual).all())
        
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

        remote_file_name = os.path.join(self.storage._get_base_directory_remote(), self.table_name, file_name)
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, file_name)
        
        self.storage.write_table(self.table_name, table_data)
        self.assert_(exists_remotely(self.storage.sftp, remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, dtype=numpy_dtype)
        self.assert_((expected==actual).all())

        
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


        remote_file_name = os.path.join(self.storage._get_base_directory_remote(), self.table_name, file_name)
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, file_name)
        
        self.storage.write_table(self.table_name, table_data)
        self.assert_(exists_remotely(self.storage.sftp, remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)
        actual = fromfile(local_file_name, numpy_ext)
        self.assert_((expected_float==actual).all())


        remote_file_name = os.path.join(self.storage._get_base_directory_remote(), self.table_name, 'bool_column.ib1')
        local_file_name = os.path.join(self.storage._get_base_directory(), self.table_name, 'bool_column.ib1')
        self.storage.write_table(self.table_name, table_data)
        self.assert_(exists_remotely(self.storage.sftp, remote_file_name))

        os.remove(local_file_name)
        self.storage.load_table(self.table_name)        
        actual = fromfile(local_file_name, '|b1')
        self.assert_((expected_bool == actual).all())
        
    def test_writing_column_to_file_when_file_of_same_column_name_and_different_type_already_exists(self):
        if skip_test():
            return
        
        column_name= "some_column"
        os.mkdir(os.path.join(self.storage._get_base_directory(), self.table_name)) 
        existing_file = file(os.path.join(self.storage._get_base_directory(), self.table_name, column_name + ".li4"), "w")
        existing_file.close()
        remote_file = os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li4")
        if not exists_remotely(self.storage.sftp, os.path.dirname(remote_file)):
            _makedirs(self.storage.sftp, os.path.dirname(remote_file))
        self.storage.sftp.put(existing_file.name, remote_file)
        
        storage = sftp_flt_storage(storage_location=self.sftp_location)
        ## Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        
        storage.write_table(table_name=self.table_name, table_data=my_data)
        self.assert_(not (exists_remotely(self.storage.sftp, remote_file)))
        self.assert_(exists_remotely(self.storage.sftp, os.path.join(self.storage._get_base_directory_remote(), 
                                                                self.table_name, column_name + ".li8")))

    def test_writing_column_to_file_when_two_files_of_same_column_name_and_different_type_already_exist(self):        
        if skip_test():
            return

        column_name= "some_column"
        os.mkdir(os.path.join(self.storage._get_base_directory(), self.table_name)) 
        existing_file_1 = file(os.path.join(self.storage._get_base_directory() , self.table_name, column_name + ".li4"), "w")
        existing_file_1.close()
        existing_file_2 = file(os.path.join(self.storage._get_base_directory() , self.table_name, column_name + ".bi4"), "w")
        existing_file_2.close()           

        remote_file_1 = os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li4")
        if not exists_remotely(self.storage.sftp, os.path.dirname(remote_file_1)):
            _makedirs(self.storage.sftp, os.path.dirname(remote_file_1))
        self.storage.sftp.put(existing_file_1.name, remote_file_1)
        remote_file_2 = os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".bi4")
        if not exists_remotely(self.storage.sftp, os.path.dirname(remote_file_2)):
            _makedirs(self.storage.sftp, os.path.dirname(remote_file_2))
        self.storage.sftp.put(existing_file_2.name, remote_file_2)

        storage = sftp_flt_storage(storage_location=self.sftp_location)        
        # Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        self.assertRaises(FltError, storage.write_table, self.table_name, my_data)
        self.assert_(not (exists_remotely(self.storage.sftp, os.path.join(self.storage._get_base_directory_remote(), self.table_name, column_name + ".li8"))))        

    def test_write_table_columns_with_different_sizes(self):
        if not skip_test():
            super(StorageWriteTests,self).test_write_table_columns_with_different_sizes()
                
    def test_write_table_no_data_to_write(self):
        if not skip_test():
            super(StorageWriteTests,self).test_write_table_no_data_to_write()
                
if __name__ == '__main__':
    opus_unittest.main()
