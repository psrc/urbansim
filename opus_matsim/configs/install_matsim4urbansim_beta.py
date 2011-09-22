# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import urllib2, os, sys
from opus_core.logger import logger
from HTMLParser import HTMLParser
from opus_matsim.models.utils.extract_zip_file import ExtractZipFile

class InstallMATSim4UrbanSim(object):
        
    def __init__(self):
        '''
        Constructor
        '''
        logger.log_status('Start init ...')
        # test if OPUS_HOME variable is set
        try:
            os.environ['OPUS_HOME']
        except:
            logger.log_error('OSPUS_HOME variable not found. Please define OPUS_HOME in your environment variables.')
            logger.log_error('Aborting MATSim4UrbanSim installation!')
            exit()
        
        self.target_path = os.path.join(os.environ['OPUS_HOME'], 'TESTmatsim4urbansim', 'jar')
        self.source_url = 'http://matsim.org/files/builds/'
        self.html_finder = FindLinks()
        
        logger.log_status('... init done!')
    
    def install(self):
        self.__check_and_get_matsim_url()
        self.__load_and_store()
        
    def __check_and_get_matsim_url(self):
        logger.log_status('Checking MATSim download homepage (nightly builds): %s' %self.source_url)
        # parse matsim.org nightly builds webside
        self.html_finder.feed( urllib2.urlopen( self.source_url ).read() )

        if not self.html_finder.allLinksFound():
            logger.log_error('Aborting MATSim4UrbanSim installation!')
            exit()
        
        # building usrls for download preparation
        self.matsim_jar_url = self.source_url + self.html_finder.getMATSimJar()
        self.matsim_lib_url = self.source_url + self.html_finder.getMATSimLib()
        #self.matsim_contrib_url = self.source_url + self.html_finder.getMATSimContrib()
        
        logger.log_status('Checking MATSim download homepage done!')
    
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
        # create symbolic link or shortcut
        symbolic_link = os.path.join( self.target_path, 'matsim4urbansim.jar' )
        if sys.platform.lower() == 'win32':
            try:
                logger.log_status('Creating shortcut %s to MATSim jar file (%s) ...' %(symbolic_link, matsim_jar_target) )
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut( symbolic_link )
            except: logger.log_error('')
        else:
            if os.path.exists( symbolic_link ):
                os.remove( symbolic_link )
            logger.log_status('Creating symbolic link %s to MATSim jar file (%s) ...' %(symbolic_link, matsim_jar_target) )
            os.symlink( matsim_jar_target , symbolic_link )
        
        # downloading matsim lib
        logger.log_status('Loading MATSim libs (zip file) ...')
        content = urllib2.urlopen( self.matsim_lib_url )
        matsim_lib_target = os.path.join( self.target_path, self.html_finder.getMATSimLib() )
        # saving download
        self.__write_on_disc( matsim_lib_target, content.read() )
        # extract (lib) zip file
        unzip = ExtractZipFile( matsim_lib_target, os.path.join( self.target_path, 'libs') )
        unzip.extract()
        # deleting (lib) zip file 
        os.remove( matsim_lib_target )
        
        # downloading contrib jar
        # tnicolai: todo when contrib jar available online
        
    def __write_on_disc(self, target, data):
        logger.log_status('Writing to %s ...' %target)
        outfile = open( target, 'w')
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
            elif at['href'].startswith('contrib.jar'):
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
            # tnicolai: todo when contrib jar is available online!
            pass
        
        return all_found
            
    def getMATSimJar(self):
        return self.matsim_jar
    def getMATSimLib(self):
        return self.matsim_lib
    def getMATSimContrib(self):
        return self.matsim_contrib

# python starts from here
if __name__ == "__main__":
    logger.log_status('Starting MATSim4UrbanSim installation ...')
    install = InstallMATSim4UrbanSim()
    install.install()
    logger.log_status('... MATSim4UrbanSim installation done!')