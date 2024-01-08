# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# set the version number for this package
import opus_core.version_numbers
__version__ = opus_core.version_numbers.get_opus_version_number(__name__)

import os, opus_core
#hack to make lottery_choices compatiable after being moved to opus_core/upc
path_opus_core = os.path.split(opus_core.__file__)[0]
try:
    __path__.append(os.path.join(path_opus_core, 'upc'))
except:
    pass