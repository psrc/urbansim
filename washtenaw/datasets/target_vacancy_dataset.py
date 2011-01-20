# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.target_vacancy_dataset import TargetVacancyDataset as UrbansimTargetVacancyDataset

class TargetVacancyDataset(UrbansimTargetVacancyDataset):
    """Set of target vacancies."""

    id_name_default = ["year", "large_area_id"]
    target_attribute_name = 'target_vacancy_rate'
    
        
        
