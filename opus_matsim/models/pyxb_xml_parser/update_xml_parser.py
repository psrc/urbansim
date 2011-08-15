# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import time
import datetime
import shutil
import tempfile
from opus_core.logger import logger
import opus_matsim.models.pyxb_xml_parser as pyxb_path
from opus_matsim.models.pyxb_xml_parser.load_xsd import LoadXSD

class UpdateBindingClass(object):
    """Creates a new pyxb xml parser"""
    
    def run(self, xsd_file=None, destination=None, binding_class_name=None, backup=False):
        logger.start_block('Starting to update xml parser for UrbanSim ...')
        
        self.output_pyxb_package_name = None
        self.output_pyxb_package_file = None
        
        # location of xsd file
        if xsd_file == None:
            # download xsd from matsim.org
            xsd_location = self.get_xsd_from_matsim_org()
        else:
            xsd_location = xsd_file
        
        xsd_location = '"file:' + xsd_location + '"'
        
        # name of output package, where the generated bindig classes will be stored
        if binding_class_name == None:
            logger.log_note('Name for PyXB binding class is None! ')
            self.output_pyxb_package_name = 'pyxb_matsim_config_parser'
            logger.log_note('Setting default name for PyXB binding class: %s' %self.output_pyxb_package_name)
        else:
            self.output_pyxb_package_name = binding_class_name
        self.output_pyxb_package_file = self.output_pyxb_package_name + '.py'
        
        # path to the PyXB executables
        pyxb_gen = os.path.join( os.getenv('OPUS_HOME'), 'opus_matsim', 'bin', 'pyxbgen')
        # checking if PyXB is available
        if not os.path.exists( pyxb_gen ):
            raise StandardError('PyXB seems not to be installed on this machine.\nPlease download and install PyXB first. It is available on http://sourceforge.net/projects/pyxb/ (Accessed July 2010).')
        
        # print status information
        logger.log_status('Found PyXB executable: %s' % pyxb_gen)
        binding_class_destination = destination
        if binding_class_destination == None:
            logger.log_note('Destination for binding classes not given. Using default location...')
            binding_class_destination = pyxb_path.__path__[0]
        logger.log_status('Destination directory for PyXB binding classes: %s' % binding_class_destination)
        logger.log_status('XSD reposit: %s' % xsd_location)
        logger.log_status('New pyxb xml binding class: %s' % self.output_pyxb_package_file)
        
        # checking if a previous binding class exsists
        # get current directory
        binding_class = os.path.join(binding_class_destination, self.output_pyxb_package_file)
        if os.path.exists(binding_class):
            logger.log_status('Found a previous binding class')
            if backup: # archiving previous pyxb parser versions
                archive_folder = os.path.join(binding_class_destination, 'xsd_archive')
                if not os.path.exists(archive_folder):
                    logger.log_status("Creating archive folder %s" % archive_folder)
                    os.mkdir(archive_folder)
                # create subfolder
                datetime = time.strftime("%Y_%m_%d_%H-%M-%S", time.gmtime())
                subfolder = os.path.join(archive_folder, datetime)
                os.mkdir(subfolder)
                destination = os.path.join(subfolder, self.output_pyxb_package_file)
                # moving prevoius binding class into archive
                logger.log_status("Moving previous binding class into archive: %s" %destination)
                shutil.move(binding_class, destination)
            else: 
                os.remove( binding_class )
        
        #===========================================================================
        # EXAMPLE:
        # Generating xml binding classes manually.
        #
        # 1) Start a terminal and switch to the place where the xsd is stored. Here its "xsds".
        #
        # 2) Enter the following commandline:
        # /Users/thomas/bin/pyxbgen \
        # > -u Products.xsd -m pro1
        #
        # 3) The following output appears:
        # urn:uuid:4b416ad0-11a5-11df-a29e-001b63930ac1
        # Python for AbsentNamespace0 requires 1 modules
        # Saved binding source to ./pro1.py
        # thomas-nicolais-macbook-pro:xsds thomas$ 
        #
        # 4) The generated classes are ready to use.
        #===========================================================================
        
        # change to binding class destination directory 
        os.chdir(binding_class_destination)
        
        # command line to generate xml binding classes as explained above
        cmd = 'start python %(pyxbgen)s -u %(xsd_location)s -m %(output)s' % {
            'pyxbgen': pyxb_gen,
            'xsd_location': xsd_location,
            'output': self.output_pyxb_package_name}
    
        logger.log_status('Executing command : %s' % cmd)
        # executing command line
        cmd_result = os.system(cmd)
        # checking if some error occurred
        if cmd_result != 0:
            raise StandardError('Executing command failed! Return code = %i' %cmd_result)
        
        # At this point executing command line was successful
        # Now a UrbanSim header is added to the generated binding classes
        
        # read whole file
        f = open(binding_class, "r")
        # binding class will be extended by the UrbanSim header
        content = "# Opus/UrbanSim urban simulation software\n# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington\n# See opus_core/LICENSE\n\n"
        line = f.readline()
        while line:
            content += line
            line = f.readline()
        f.close()
        
        # get current binding class and overwrite with the actual content containing the header
        binding_class = os.path.join(binding_class_destination, self.output_pyxb_package_file)
        print "Path to generated binding class: %s" % binding_class
        # open binding class to add the header
        f = open(binding_class, 'w')
        try:
            f.write(content)
        except Exception:
            logger.log_error("Error occurred while adding the UrbanSim header to the binding class.")
        finally:
            f.close()
        
        logger.log_status('Successful finished. Exit program.')
        logger.end_block()
        return 1 # return code for test class (1 == ok)
    
    def get_xsd_from_matsim_org(self):
        """ Downloads and stores xsd file from matsim.org
        """

        # set temporary output dir for xsd file
        self.temp_dir = tempfile.mkdtemp(prefix='xsd_tmp')

        xsd_reposit = os.path.join(self.temp_dir, 'MATSim4UrbanSimConfigSchema.xsd')
        # set source url for xsd
        url = 'http://matsim.org/files/dtd/MATSim4UrbanSimConfigSchema.xsd'
        
        # load and store xsd
        xsd_loader = LoadXSD(url, xsd_reposit)
        xsd_loader.load_and_store()
        
        # return xsd location
        return xsd_reposit
        

if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-x", "--xsd", dest="xsd_file_name", action="store", type="string",
                      help="Name of file containing xsd")
    parser.add_option("-t", "--testrun", dest="test_run_flag", action="store", type="int",
                      help="Indicates if this is a test run")
    (options, args) = parser.parse_args()
    
    # default: updates with default xsd on matsim.org
    #UpdateBindingClass().run( )
    UpdateBindingClass().run( options.xsd_file_name, None, None, False )
    
    # use this to update a pyxb classes wit custom xsd
    #if options.test_run_flag == 0:
    #    UpdateBindingClass().run( options.xsd_file_name, None, None, False )
    #else:
    #    UpdateBindingClass().run( options.xsd_file_name, None, None, True )
    
    # tnicolai: only testing
    #import opus_matsim.sustain_city.configs as test_path
    #xsd_source = os.path.join(test_path.__path__[0], 'xsd_template', 'MATSim4UrbanSimConfigSchema.xsd')
    

    
    