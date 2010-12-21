# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# set the version number for this package
import opus_core.version_numbers
__version__ = opus_core.version_numbers.get_opus_version_number(__name__)

from opus_core.models import *
from opus_core.upc import *