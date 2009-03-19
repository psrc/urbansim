# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import tempfile
import os
from urlparse import urlparse
from shutil import rmtree
from opus_core.logger import logger

if os.name == 'nt':
    from nturl2path import pathname2url
    convertntslash = pathname2url
else:
    def convertntslash(arg):
        return arg

def get_ssh_client(ssh_url='', ssh_server_config={}, client_type='plink'):
    return eval('ssh_%s(ssh_url=ssh_url, ssh_server_config=ssh_server_config)' % client_type)

class ssh_client:
    def __init__(self, ssh_url='', ssh_server_config={}):
        self.client_type = None  # generic ssh client
        self.port = 22
        
        if ssh_url:
            o = urlparse(ssh_url)
            self.hostname = o.hostname
            self.username = o.username
            self.password = o.password
            if o.port is not None:
                self.port = o.port
        elif ssh_server_config:
            self.hostname = ssh_server_config.get('hostname')
            self.username = ssh_server_config.get('username')
            self.password = ssh_server_config.get('password')
            self.port = ssh_server_config.get('port', self.port)
        
    def execute_cmd_and_get_return_value(self, cmd):
        pass
    
    def execute_cmd_and_get_stdout(self, cmd, raise_at_error=False):
        pass
    
    def exists_remotely(self, name):
        """
        check whether name (file name or directory name) exists on sftp
        """
        cmd = 'python -c "import os; print(os.path.exists(\'%s\'))"' % name
        return eval(self.execute_cmd_and_get_stdout(cmd))
    
    def isdir(self, name):
        """return True if name is an existing directory
        generic implementation with python
        """
        cmd = 'python -c "import os; print(os.path.isdir(\'%s\'))"' % name
        return eval(self.execute_cmd_and_get_stdout(cmd))
    
    def makedirs(self, path):
        """ make recursive directories on sftp server
        generic implementation with python
        """
        cmd = 'python -c "import os; os.makedirs(\'%s\')"' % path
        return self.execute_cmd_and_get_stdout(cmd)

    def remove(self, filepath):
        """remove a file
        generic implementation with python
        """
        cmd = 'python -c "import os; os.remove(\'%s\')"' % filepath
        return self.execute_cmd_and_get_stdout(cmd)
    
    def rmtree(self, path):
        """Recursively delete a directory tree.
        generic implementation with python
        """
        cmd = 'python -c "import shutil; shutil.rmtree(\'%s\')"' % path
        return self.execute_cmd_and_get_stdout(cmd)
    
    def get_remote_temp_dir(self):
        """
        """
        cmd = "python -c 'import tempfile; print tempfile.mkdtemp()'"
        return self.execute_cmd_and_get_stdout(cmd)
    
    def glob(self, path_pattern):
        """
        generic implementation with python
        """
        cmd = 'python -c "from glob import glob; print glob(\'%s\')"' % path_pattern
        return eval(self.execute_cmd_and_get_stdout(cmd))
        
    
    def listdir(self, path):
        """ os.listdir
        generic implementation with python
        """
        cmd = 'python -c "import os; print os.listdir(\'%s\')"' % path
        return eval(self.execute_cmd_and_get_stdout(cmd))

    def put(self, src, target):
        pass
    
    def get(self, src, target):
        pass

paramiko = None
try:
    import paramiko
except:
    pass

class ssh_paramiko(ssh_client):
    
    def __init__(self, ssh_url='', ssh_server_config={}):
        ssh_client.__init__(self, ssh_url=ssh_url, ssh_server_config=ssh_server_config)
        
        if not paramiko:
            raise ImportError, 'Error importing paramiko.'
        
        self.client_type = 'paramiko'        
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname,
                         port = self.port,
                         username=self.username,
                         password=self.password,
                         pkey=self.load_key_if_exists())
        #self.ssh._transport.set_keepalive(60)

        self.sftp = self.ssh.open_sftp()

    def __del__(self):
        try:
            #self.sftp.close()
            self.ssh.close()
        except:
            pass

    def load_key_if_exists(self, key_file=None):
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
    
    def execute_cmd_and_get_stdout(self, cmd, raise_at_error=False):
        """
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        stderr_msg = stderr.readlines() 
        if len(stderr_msg) > 0:
            logger.log_error("Error encountered executing cmd through ssh:\n" + ''.join(stderr_msg))
            if raise_at_error:
                raise RuntimeError, "Error encountered executing cmd through ssh:\n" + ''.join(stderr_msg)
    
        results = stdout.readlines()
        if len(results)==1:
            results=results[0].strip()
            
        stdin.close(); stdout.close(); stderr.close()
        return results

    def mput(self, src, target):
        """ file/path pattern is not supported
        works when src and target are both directories
        
        Note src behaves differently with and without an ending slash:
        mput('C:\\src_dir\\data_dir', '/tmp/target_dir') ends up with cotents in local directory data_dir in /tmp/target_dir/data_dir on server
        mput('C:\\src_dir\\data_dir\\', '/tmp/target_dir') ends up with cotents in local directory data_dir in /tmp/target_dir on server
        """
        target = convertntslash(target)
        if os.path.isdir(src):
            basedir = os.path.basename(src)
            subdirs = os.listdir(src)
            for subdir in subdirs:
                self.mput(os.path.join(src, subdir), convertntslash(os.path.join(target, basedir, subdir)) )
        else:
            target_dirname = os.path.dirname(target)
            if not self.exists_remotely(target_dirname):
                self.makedirs(target_dirname)
            return self.sftp.put(src, target)
                
    def mget(self, src, target):
        """ file/path pattern is not supported
        works when src and target are both directories
        
        Note src behaves differently with and without an ending slash:
        mget('/tmp/src_dir/data_dir',  'C:\\target_dir') ends up with cotents in remote directory data_dir in C:\\target_dir\\data_dir locally
        mget('/tmp/src_dir/data_dir/', 'C:\\target_dir') ends up with cotents in remote directory data_dir in C:\\target_dir locally
        """
        src = convertntslash(src)
        if self.isdir(src):
            basedir = os.path.basename(src)
            subdirs = self.listdir(src)
            for subdir in subdirs:
                self.mget(os.path.join(src, subdir), os.path.join(target, basedir, subdir))
        else:
            target_dirname = os.path.dirname(target)
            if not os.path.exists(target_dirname):
                os.makedirs(target_dirname)
            return self.sftp.get(src, target)
        
class ssh_plink(ssh_client):

    def __init__(self, ssh_url='', ssh_server_config={}):
        ssh_client.__init__(self, ssh_url=ssh_url, ssh_server_config=ssh_server_config)
        
        ##make sure plink.exe and pscp.exe are in search PATH
        self.plink = 'plink.exe'
        self.pscp = 'pscp.exe'
        #self.plink = os.popen3('where plink.exe')[1].readlines()
        #if len(self.plink) > 1:
            #self.plink = self.plink[0].strip()

        #self.pscp = os.popen3('where pscp.exe')[1].readlines()
        #if len(self.pscp) > 1:
            #self.pscp = self.pscp[0].strip()
        
        if not self.plink:
            raise RuntimeError, "plink.exe cannot be found in the current directory or in paths in the PATH environment variable."       
        if not self.pscp:
            raise RuntimeError, "plink.exe cannot be found in the current directory or in paths in the PATH environment variable."
        self.client_type = 'plink'
        
    def _write_cmd_string_to_temp_file(self, cmd):
        """ This is to work around quotes cannot be sufficiently escaped in some cases in Windows
        """
        fn, filename = tempfile.mkstemp()
        os.write(fn, cmd)
        os.close(fn)
        return filename
    
    def execute_cmd_and_get_return_value(self, cmd):
        cmdfilename = self._write_cmd_string_to_temp_file(cmd)
        return_value = os.system("%s -ssh -l %s -pw %s %s -m %s " % (self.plink, self.username, self.password, self.hostname, cmdfilename))
        os.remove(cmdfilename)
        return return_value
    
    def execute_cmd_and_get_stdout(self, cmd, raise_at_error=False):
        """TODO: rewrite for python2.6 using subprocess module
        """
        cmdfilename = self._write_cmd_string_to_temp_file(cmd)
        stdin, stdout, stderr = os.popen3("%s -ssh -l %s -pw %s %s -m %s " % (self.plink, self.username, self.password, self.hostname, cmdfilename))
        
        stderr_msg = stderr.readlines() 
        if len(stderr_msg) > 0:
            logger.log_error("Error encountered executing cmd through ssh:\n" + ''.join(stderr_msg))
            if raise_at_error:
                raise RuntimeError, "Error encountered executing cmd through ssh:\n" + ''.join(stderr_msg)
    
        results = stdout.readlines()
        if len(results)==1:
            results=results[0].strip()
            
        stdin.close(); stdout.close(); stderr.close()
        os.remove(cmdfilename)
        return results
    
    def mput(self, src, target):
        target = convertntslash(target)
        if os.path.isdir(src) and not self.exists_remotely(target):
            self.makedirs(target)
        return_value = os.system("%s -sftp -r -q -l %s -pw %s %s %s:%s" % (self.pscp, 
                                                                     self.username, 
                                                                     self.password, 
                                                                     src, 
                                                                     self.hostname,target))
        return return_value
    
    def mget(self, src, target):
        src = convertntslash(src)
        if self.isdir(src) and not os.path.exists(target):
            os.makedirs(target)
        return_value = os.system("%s -sftp -r -q -l %s -pw %s %s:%s %s" % (self.pscp, 
                                                                     self.username, 
                                                                     self.password, 
                                                                     self.hostname, src, 
                                                                     target))
        return return_value