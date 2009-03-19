# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.target_vacancy_dataset import TargetVacancyDataset as UrbansimTargetVacancyDataset

class TargetVacancyDataset(UrbansimTargetVacancyDataset):
    """Set of target vacancies."""

    id_name_default = ["year", "large_area_id"]
    
        
        
