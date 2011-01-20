# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.opus_package import OpusPackage

class package(OpusPackage):
    name = 'psrc'
    required_opus_packages = ["opus_core", "opus_emme2", "urbansim"]
