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

from rate_dataset import RateDataset

class BusinessRelocationRateDataset(RateDataset):

    id_name_default = ["sector_id"]
    dataset_name = "business_relocation_rate"
    probability_attribute = "business_relocation_probability"
    in_table_name_default = "annual_relocation_rates_for_business"
    out_table_name_default = "annual_relocation_rates_for_business"