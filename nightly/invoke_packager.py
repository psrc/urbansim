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

import os, os.path, sys
from opus_core.installer.packager import Packager

directories = os.listdir("..")

package_list = []
for dir in directories:
    if os.path.isdir(os.path.join("..", dir)):
        if not dir == '.metadata' and not dir == 'nightly':
            package_list.append(os.path.join("..", dir))

# Mark each Opus package as part of the installer, by adding the 
# __from_installer__ file to each Opus package.
for package_dir in package_list:
    f = open(os.path.join(package_dir, '__from_installer__.py'), 'w')
    f.close()

setup_path = os.path.join("..")
version = sys.argv[1]

Packager().create_installer(distribution_format = 'sdist',
                            package_list = package_list,
                            setup_path = setup_path,
                            version = version)

Packager().create_installer(distribution_format = 'bdist_wininst',
                            package_list = package_list,
                            setup_path = setup_path,
                            version = version)