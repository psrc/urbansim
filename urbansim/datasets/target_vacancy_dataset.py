# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class TargetVacancyDataset(UrbansimDataset):
    """Set of target vacancies."""

    id_name_default = "year"
    in_table_name_default = "target_vacancies"
    out_table_name_default = "target_vacancies"
    dataset_name = "target_vacancy"
    
        
        
