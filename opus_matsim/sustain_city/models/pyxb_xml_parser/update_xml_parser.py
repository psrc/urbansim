# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
import time
import datetime
import shutil
from opus_core.logger import logger
import opus_matsim.sustain_city.models.pyxb_xml_parser as pyxb_path
import opus_matsim.sustain_city as sc_path

class UpdateBindingClass(object):
    """Creates a new pyxb xml parser"""
    
    def run(self, xsd_file, binding_class_destination=None, test_run=False):
        logger.start_block('Starting to update xml parser for UrbanSim ...')
        
        # name of the current xsd file
        xsd_name = xsd_file
        # path to the PyXB executables
        pyxb_gen = os.path.join( os.getenv('HOME'), 'bin', 'pyxbgen')
        # name of output package, where the generated bindig classes will be stored
        output = 'pyxb_matsim_config_parser'
        output_file = output + '.py'
    
        # checking if PyXB is available
        if not os.path.exists( pyxb_gen ):
            logger.log_error("PyXB seems not to be installed on this machine.")
            logger.log_error("Please download and install PyXB first. It is available on http://sourceforge.net/projects/pyxb/ (Accessed July 2010).")
            logger.end_block()
            sys.exit(-1) # return code for test class (-1 == faild) 
        
        # print status information
        logger.log_status('Pyxb executable found: %s' % pyxb_gen)
        local_path = binding_class_destination
        if local_path == None:
            local_path = pyxb_path.__path__[0]
        logger.log_status('Current working directory: %s' % local_path)
        logger.log_status('XSD name: %s' % xsd_name)
        logger.log_status('New pyxb xml binding class: %s' % output_file)
        
        # checking if a previous binding class exsists
        # get current directory
        binding_class = os.path.join(local_path, output_file)
        if os.path.exists(binding_class):
            logger.log_status('A previous binding class is found')
            if test_run:
                os.remove( binding_class)
            else: # archiving previous pyxb parser versions
                archive_folder = os.path.join(local_path, 'xsd_archive')
                if not os.path.exists(archive_folder):
                    logger.log_status("Creating archive folder %s" % archive_folder)
                    os.mkdir(archive_folder)
                # create subfolder
                datetime = time.strftime("%Y_%m_%d-%H:%M:%S", time.gmtime())
                subfolder = os.path.join(archive_folder, datetime)
                os.mkdir(subfolder)
                destination = os.path.join(subfolder, output_file)
                # moving prevoius binding class into archive
                logger.log_status("Moving previous binding class into archive")
                shutil.move(binding_class, destination)
        
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
        
        # comand line to generate xml bindig classes as explained above
        cmd = 'cd %(local_path)s ; %(pyxbgen)s -u %(xsd_name)s -m %(output)s' % {
            'local_path': local_path,
            'pyxbgen': pyxb_gen,
            'xsd_name': xsd_name,
            'output': output}
    
        logger.log_status('Executing command : %s' % cmd)
        # executing comand line
        cmd_result = os.system(cmd)
        # checking if some error occured
        if cmd_result != 0:
            logger.log_error('Error.')
            logger.end_block()
            sys.exit(-1) # return code for test class (-1 == faild) 
        
        # Everything ok
        
        # read whole file
        f = open(binding_class, "r")
        # content will contain the whole binding class code and the UrbanSim header
        content = "# Opus/UrbanSim urban simulation software\n# Copyright (C) 2005-2009 University of Washington\n# See opus_core/LICENSE\n\n"
        line = f.readline()
        while line:
            content += line
            line = f.readline()
        f.close()
        
        # get current binding class and overwrite with the actual content containing the header
        binding_class = os.path.join(local_path, output_file)
        print "Path to generated binding class: %s" % binding_class
        # open binding class to add the header
        f = open(binding_class, 'w')
        try:
            f.write(content)
        except Exception:
            logger.log_error("Error occured while adding the UrbanSim header to the binding class.")
        finally:
            f.close()
            
        
        logger.log_status('Successful finished. Exit program.')
        logger.end_block()
        return 1 # return code for test class (1 == ok) 

if __name__ == "__main__":
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("-x", "--xsd", dest="xsd_file_name", action="store", type="string",
    #                   help="Name of file containing xsd")
    # parser.add_option("-t", "--testrun", dest="test_run_flag", action="store", type="boolean",
    #                   help="Indicates if this is a test run")
    # (options, args) = parser.parse_args()

    UpdateBindingClass().run('MATSim4UrbanSimConfigSchema.xsd')
    
    