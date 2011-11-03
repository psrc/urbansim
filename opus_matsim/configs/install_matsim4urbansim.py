# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import urllib2, os, sys
import tempfile
from shutil import rmtree
from opus_core.logger import logger
from HTMLParser import HTMLParser
from opus_matsim.models.utils.extract_zip_file import ExtractZipFile
from opus_matsim.models.org.constants import matsim4opus
from opus_core import paths

class InstallMATSim4UrbanSim(object):
        
    def __init__(self):
        '''
        Constructor
        '''
        logger.log_status('Start init ...')

        if paths.get_opus_home_path == None or paths.get_opus_home_path() == "":
            logger.log_error('OSPUS_HOME variable not found. Please define OPUS_HOME in your environment variables.')
            logger.log_error('Aborting MATSim4UrbanSim installation!')
            exit()
        
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.target_path = paths.get_opus_home_path( matsim4opus, 'jar')
        self.source_url = 'http://matsim.org/files/builds/'
        self.html_finder = FindLinks()
        
        logger.log_status('... init done!')
    
    def install(self):
        self.__determine_os()
        self.__check_and_get_matsim_url()
        self.__load_and_store()
        self.__cleanup()
        
    def __determine_os(self):
        self.is_windows_os = sys.platform.lower() == 'win32'
        if(self.is_windows_os):
            logger.log_status('Detected Windows operating system ...')
        else:
            logger.log_status('Detected Unix based operating system ...')
        
    def __check_and_get_matsim_url(self):
        logger.log_status('Checking availability of necessary MATSim files (nightly builds): %s' %self.source_url)
        # parse matsim.org nightly builds webside
        self.html_finder.feed( urllib2.urlopen( self.source_url ).read() )

        if not self.html_finder.allLinksFound():
            logger.log_error('Aborting MATSim4UrbanSim installation!')
            exit()
        
        # building usrls for download preparation
        self.matsim_jar_url = self.source_url + self.html_finder.getMATSimJar() # matsim url
        self.matsim_lib_url = self.source_url + self.html_finder.getMATSimLib() # lib url
        self.matsim_contrib_url = self.source_url + self.html_finder.getMATSimContrib() # contrib url
        
        logger.log_status('Availability check done!')
        
    def __cleanup(self):
        logger.log_status('Cleaning up installation ...')
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir, True) # if second argument == True ignores errors (no exception raised)
        logger.log_status('... done!')
    
    def __load_and_store(self):
        
        logger.log_status('Starting download process ...')
        
        if not os.path.exists( self.target_path ):
            logger.log_status('Directory %s does not exist and will be created.' %self.target_path)
            os.makedirs( self.target_path )
        
        # downloading matsim jar
        content = urllib2.urlopen( self.matsim_jar_url )
        matsim_jar_target = os.path.join( self.target_path, self.html_finder.getMATSimJar() )
        # saving download
        logger.log_status('Loading MATSim.jar ...')
        self.__write_on_disc( matsim_jar_target, content.read() )
        logger.log_status('... MATSim.jar download done!')
        self.__rename(matsim_jar_target, os.path.join( self.target_path, 'matsim.jar' ))
        # create symbolic link or shortcut (this is not used since java can't handle windows shortcuts)
        #self.__create_symbolic_link( matsim_jar_target, 'matsim.jar' )
        
        # downloading matsim lib
        logger.log_status('Loading MATSim libraries ...')
        content = urllib2.urlopen( self.matsim_lib_url )
        matsim_lib_target_tmp = os.path.join( self.temp_dir, self.html_finder.getMATSimLib() )
        # saving download
        self.__write_on_disc( matsim_lib_target_tmp, content.read() )
        logger.log_status('... MATSim libraries download done!')
        # extract (lib) zip file
        unzip = ExtractZipFile( matsim_lib_target_tmp, self.target_path )
        unzip.extract()
        
        # downloading contrib jar
        logger.log_status('Loading MATSim4UrbanSim contribution/extension ...')
        content = urllib2.urlopen( self.matsim_contrib_url )
        # target location to store downloaded tmp zip file
        matsim_contrib_target_tmp = os.path.join( self.temp_dir, self.html_finder.getMATSimContrib() )
        # target location for symbolic link/shortcut
        matsim_contrib_target_final =  os.path.join( self.target_path, self.html_finder.getMATSimContrib().replace('.zip', '') )

        # saving download
        self.__write_on_disc( matsim_contrib_target_tmp, content.read() )
        logger.log_status('... MATSim4UrbanSim download done!')
        # extract contrib zip file
        unzip = ExtractZipFile( matsim_contrib_target_tmp, self.target_path )
        unzip.extract()

        matsim_contrib_new_target =matsim_contrib_target_final.split('matsim4urbansim_')[0] + 'contrib'
        # rename directory
        self.__rename(matsim_contrib_target_final, matsim_contrib_new_target)
        contrib_jar = self.html_finder.getMATSimContrib().rsplit('-r')[0] + '.jar'
        # rename jar file within renamed directory
        self.__rename(os.path.join( matsim_contrib_new_target, contrib_jar ), os.path.join( matsim_contrib_new_target, 'matsim4urbansim.jar' ))
        
        # creating symbolic link (this is not used since java can't handle windows shortcuts)
        #contrib_dir = matsim_contrib_target.replace('.zip', '')
        #contrib_jar = self.html_finder.getMATSimContrib().rsplit('-r')[0] + '.jar'
        #source_file = os.path.join( contrib_dir, contrib_jar )
        #self.__create_symbolic_link(source_file, 'matsim4urbansim.jar')       

    def __rename(self, source, target):
        ''' this renames files or directories
            This is used instead of setting symbolic links or shortcuts since
            java can't handle windows shortcuts ...
        '''
        if os.path.exists( target ):
            if os.path.isfile( target ):
                os.remove( target )
            if os.path.isdir( target ):
                rmtree( target, True )
        os.rename(source, target)
            
    def __create_symbolic_link(self, source_file, link_name):
        ''' this creates a symbolic link / shortcut to a given source_file
            unfortunately java can't handle shortcuts this is why this method 
            is not used anymore
            files are renamed instead
        '''
        symbolic_link = os.path.join( self.target_path, link_name )
        
        if self.is_windows_os: # Windows
            symbolic_link = symbolic_link + '.lnk'
        try: # removing symbolic link / short cut
            os.unlink( symbolic_link )
        except: pass
            
        if self.is_windows_os: # Windows
            try:
                logger.log_status('Creating shortcut %s to (%s) ...' %(symbolic_link, source_file) )
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut( symbolic_link )
                shortcut.Targetpath = source_file
                shortcut.save() 
            except: 
                logger.log_error('Error while creating a shortcut to %s!' % source_file)
                logger.log_error('Installation not successful. Try manual installation as described in opus_matsim_user_guide.pdf in opus_matsim/docs')
                exit()
        else: # Mac, Linux
            logger.log_status('Creating symbolic link %s to (%s) ...' %(symbolic_link, source_file) )
            os.symlink( source_file , symbolic_link )
        
    def __write_on_disc(self, target, data):
        logger.log_status('Writing to %s ...' %target)
        outfile = open( target, 'w')
        # wb for writing binery files in windows
        if self.is_windows_os:
            outfile = open( target, 'wb') 
        outfile.write( data )
        outfile.flush()
        outfile.close()
        logger.log_status('... done!')
        

class FindLinks(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # define key words
        self.matsim_jar = None
        self.matsim_lib = None
        self.matsim_contrib = None
 
    def handle_starttag(self, tag, attrs):
        at = dict(attrs)
        if tag == 'a' and 'href' in at:
            # found MATSim jar
            if at['href'].startswith('MATSim_r'):
                self.matsim_jar = at['href']
            # found MATSim_libs
            elif at['href'].startswith('MATSim_libs.zip'):
                self.matsim_lib = at['href']
            # found contrib
            elif at['href'].startswith('matsim4urbansim'):
                self.matsim_contrib = at['href']
    
    def allLinksFound(self):
        all_found = True
        # checking if all needed links found
        if self.matsim_jar == None:
            logger.log_error('Link to MATSim jar not found!')
            all_found = False
        if self.matsim_lib == None:
            logger.log_error('Link to MATSim lib not found!')
            all_found = False
        if self.matsim_contrib == None:
            logger.log_error('Link to MATSim4Urbansim contribution not found!')
            all_found = False
        
        return all_found
            
    def getMATSimJar(self):
        return self.matsim_jar
    def getMATSimLib(self):
        return self.matsim_lib
    def getMATSimContrib(self):
        return self.matsim_contrib

# python starts from here
if __name__ == "__main__":
    logger.log_status('-----------------------------------------')
    logger.log_status('Starting MATSim4UrbanSim installation ...')
    logger.log_status('-----------------------------------------')
    
    install = InstallMATSim4UrbanSim()
    install.install()
    
    logger.log_status('--------------------------------------')
    logger.log_status('... MATSim4UrbanSim installation done!')
    logger.log_status('--------------------------------------')