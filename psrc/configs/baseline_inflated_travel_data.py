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


from inprocess.psrc_zone.configs.create_post_year_configuration import create_post_year_configuration
from baseline_copied_travel_data import BaselineCopiedTravelData

class BaselineInflatedTravelData(BaselineCopiedTravelData):
    def __init__(self):
        BaselineCopiedTravelData.__init__(self)
        end_year = self['years'][1]
        self['post_year_configuration'] = create_post_year_configuration(end_year, travel_data_multiplication_factor=1.50)
