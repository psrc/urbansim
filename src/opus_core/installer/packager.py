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

from opus_core.opus_package import OpusPackage
from opus_core.opus_package_info import package
from sets import Set
import os, shutil

class Packager(object):
    """This class utilizes Python's dist and setuptools to easily package OPUS code and 
    create an installer for a given platform"""
    
    def __init__(self):
        pass
    
    def create_installer(self, 
                         package_list,
                         distribution_format,
                         setup_path,
                         version):
        
        opus_core_path = OpusPackage().get_path_for_package('opus_core')
        scripts_path = os.path.join(opus_core_path, 'installer', 
            'scripts_for_Python_Scripts_directory')
        rel_path_template = ("os.path.join('opus_core', 'installer', "
            "'scripts_for_Python_Scripts_directory', '%s')")
        
        scripts = []
        for file in os.listdir(scripts_path):
            if not os.path.isdir(os.path.join(scripts_path, file)):
                scripts.append(rel_path_template % file)
        
        setup_string = \
"""
import os
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "opus",
    version = "%(version)s",
    packages = find_packages(),
    
    #install all files under source control (i.e. XML table schemas, documentation)
    include_package_data = True,

    author = "Center for Urban Simulation and Policy Analysis, University of Washington",
    license = "GNU",
    url = "http://www.urbansim.org",
    scripts = [%(scripts)s
               ]
    )
"""         % {'version':version,
               'scripts':',\n               '.join(scripts),
              }

        setup_file_path = os.path.join(setup_path, 'setup.py')
        open(setup_file_path, 'w').write(setup_string)
                
        manifest_string = \
"""
include ez_setup.py
"""

        for package_to_include in package_list:
            manifest_string += "graft %s \n" % package_to_include
        manifest_string += "exclude *.pyc"
        
        manifest_path = os.path.join(setup_path, 'MANIFEST.in')
        open(manifest_path, 'w').write(manifest_string)        
       
        build_distribution_cmd = "python setup.py %s" % distribution_format
        
        package_dir_path = package().get_package_path()
        
        shutil.copyfile(os.path.join(package_dir_path, "installer", "ez_setup.py"), 
                        os.path.join(setup_path, "ez_setup.py"))
        current_dir = os.getcwd()   
        os.chdir(setup_path)
        os.system(build_distribution_cmd)
        os.chdir(current_dir)

import os.path


if __name__ == "__main__":
    
    # Eventually we will want to remove the dependency on UrbanSim from this
    # code, possibly by allowing command line arguments or a gui.
    package_list = [ "opus_core", 
                     "urbansim" ]
    distribution_format = 'sdist'
    setup_path = os.path.join("..","..","..")
    version = sys.argv[1]
    Packager().create_installer(package_list = package_list,
                                distribution_format = distribution_format,
                                setup_path = setup_path,
                                version = version)
