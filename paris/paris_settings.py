# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration

from sandbox.my_settings import MySettings

from urbansim.datasets.neighborhood_dataset import NeighborhoodDataset
    
class ParisSettings(MySettings):
    flt_dir = "c:/urbansim/data/Paris"
    flt_subdir = {
                 "neighborhood":"nb",
                 "household":"hh",
                 "job":"job",
                 "travel_data":"travel_data"
                 }
                 
    dir = "c:/urbansim/data/Paris"
    nbsubdir = "nb"
    db = "paris_estimation"
    outputdb = "paris_estimation_output"
    location_set_dataset = "neighborhood"

    def prepare_session_configuration(self, force_reload=False, debuglevel=4):
        MySettings.prepare_session_configuration(self, force_reload=force_reload, debuglevel=debuglevel)

        if self.use_flt_for_big_datasets:                
            if force_reload or "neighborhood" not in SessionConfiguration().get_dataset_pool():
                if os.path.exists(os.path.join(self.dir, self.nbsubdir)):
                    nbs = NeighborhoodDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=self.dir), 
                                      in_table_name=self.nbsubdir,
                                      out_storage=StorageFactory().get_storage('flt_storage', storage_location=self.outputdir), 
                                      debuglevel=debuglevel)
                    SessionConfiguration().get_dataset_pool()._add_dataset(self.location_set_dataset, nbs)
                else:
                    logger.log_warning(os.path.join(self.dir, self.nbsubdir) + " doesn't exist; try to load neighborhood set from database %s" % self.db)                        