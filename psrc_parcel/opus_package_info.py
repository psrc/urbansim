# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.opus_package import OpusPackage

class package(OpusPackage):
    name = 'psrc_parcel'
    required_opus_packages = ["opus_core", "opus_emme2", "urbansim", "urbansim_parcel"]
