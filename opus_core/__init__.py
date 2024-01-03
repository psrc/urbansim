# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# set the version number for this package
import opus_core.version_numbers
__version__ = opus_core.version_numbers.get_opus_version_number(__name__)

import os
try:
    dirname=__path__[0]
    __path__.append(os.path.join(dirname, 'models'))
    __path__.append(os.path.join(dirname, 'upc'))
except:
    pass