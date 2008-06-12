#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from control_total_dataset import ControlTotalDataset

class EmploymentControlTotalDataset(ControlTotalDataset):
    id_name_default = ['year', 'sector_id']
    #if both self.id_name_default and id_name argument in __init__ is unspecified, 
    #ControlTotalDataset would use all attributes not beginning with "total"
    #as id_name
    in_table_name_default = "annual_employment_control_totals"
    out_table_name_default = "annual_employment_control_totals"
    dataset_name = "employment_control_total"
    
    def __init__(self, *args, **kwargs):
        ControlTotalDataset(self, what='employment', *args, **kwargs)
        