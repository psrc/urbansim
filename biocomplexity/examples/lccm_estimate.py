#
# Opus software. Copyright (C) 1998-2007 University of Washington
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


from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.models.land_cover_change_model import LandCoverChangeModel
from biocomplexity.equation_specification import EquationSpecification
from opus_core.opus_package import OpusPackage
from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.variables.variable_name import VariableName
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from numpy import arange, where
import os

from biocomplexity.opus_package_info import package
parent_dir_path = package().get_package_parent_path()
flt_directory = os.path.join(parent_dir_path, "LCCM_small_test_set_opus", "converted", "data_for_estimation")
years = [1991, 1995]


lc1 =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
    storage_location = os.path.join(flt_directory, str(years[0]))),
    resources=Resources({"lowercase":1}))
lc2 =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
    storage_location = os.path.join(flt_directory, str(years[1]))),
    resources=Resources({"lowercase":1}))
package_path = OpusPackage().get_path_for_package("biocomplexity")  
choices = range(1,15)   
lccm = LandCoverChangeModel(choices, submodel_string="lct")
storage = StorageFactory().get_storage('tab_storage', 
    storage_location=os.path.join(package_path, 'data'))
specification = EquationSpecification(in_storage=storage)
specification.load(in_table_name="lccm_specification_opus_test.tab")
specification.set_dataset_name_of_variables("land_cover")

coef, results = lccm.estimate(specification, lc1, lc2, debuglevel=4)
coef.write(out_storage=storage, out_table_name="lccm_coefficients")