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

from urbansim.datasets.control_total_dataset import ControlTotalDataset as UrbansimControlTotalDataset

id_name_defaults = {"household":["year", "large_area_id"],
                   "employment":["year", "sector_id", "large_area_id"]}

class ControlTotalDataset(UrbansimControlTotalDataset):
    def __init__(self, what="", **kwargs):
        if what=="household":
            self.id_name_default = id_name_defaults[what]
        elif what=="employment":
            self.id_name_default = id_name_defaults[what]
        else:
            raise RuntimeError("Unknown control total dataset type", what)
        
        UrbansimControlTotalDataset.__init__(self, what=what, **kwargs)
