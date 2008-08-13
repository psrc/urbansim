#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from urbansim.datasets.target_vacancy_dataset import TargetVacancyDataset as UrbansimTargetVacancyDataset

class TargetVacancyDataset(UrbansimTargetVacancyDataset):
    """Set of target vacancies."""

    id_name_default = ["year", "large_area_id"]
    
        
        
