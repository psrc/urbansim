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
from opus_core.opus_package import OpusPackage


class package(OpusPackage):
    name = 'opus_core'

    required_external_packages = ['numpy>=1.0.2', 'MySQL-python>=1.2.0']
    required_opus_packages = []
    optional_external_packages = ['matplotlib>=0.87', 'Numeric>=23.8',
                                  'rpy>=0.4.6']
