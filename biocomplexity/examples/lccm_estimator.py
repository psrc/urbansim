# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.models.land_cover_change_model import LandCoverChangeModel
from biocomplexity.equation_specification import EquationSpecification
from opus_core.opus_package import OpusPackage
from biocomplexity.opus_package_info import package
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from numpy import arange, where
from urbansim.estimation.estimator import Estimator
from opus_core.logger import logger
from time import time
import os

from opus_core.sampling_toolbox import sample_noreplace
from opus_core.variables.variable_name import VariableName

class LCCMEstimator(Estimator):
    def __init__(self, **kargs):
#        Estimator.__init__(self, settings=None, run_land_price_model_before_estimation=False, **kargs) # <-- old __init__
#        Estimator.__init__(self, config=None, save_estimation_results=True) # <-- new __init__ doesn't work, but not needed

        parent_dir_path = package().get_package_parent_path()
        package_path = OpusPackage().get_path_for_package("biocomplexity")  
        self.storage = StorageFactory().get_storage('tab_storage', 
            storage_location=os.path.join(package_path, 'data'))

        ## 1. directory path of full (4 county spatial extent) dataset
        flt_directory = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County")

        ## 2. select (uncomment) from one the following choices of directory pathes of subsetted sample input data/variables
#        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_small_test_set_opus")
        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_estimation_all")
#        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_estimation_all_orig")
#        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_suburban_orig")
#        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_urban")
#        flt_directory_est = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_urban_orig")

        ## note - must rename lct-forusewith91sample.Float32 to lct.lf4 if doing 1991-1995
        ## note - must rename lct-forusewith95sample.Float32 to lct.lf4 if doing 1995-1999
        
        ## 3. select (uncomment) from one the following choices of land cover data (input data) date pairs (years) 
#        years = [1991, 1995]
        years = [1995, 1999]
#        years = [1999, 2002]
        
        self.lc1 =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
            storage_location = os.path.join(flt_directory_est, str(years[0]))),
            resources=Resources({"lowercase":1}))
        self.lc2 =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
            storage_location = os.path.join(flt_directory_est, str(years[1]))),
            resources=Resources({"lowercase":1}))
        
        self.lc1_all =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
            storage_location = os.path.join(flt_directory, str(years[0]))),
            resources=Resources({"lowercase":1}))
        self.lc1_all.flush_dataset()
        self.lc2_all =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", 
            storage_location = os.path.join(flt_directory, str(years[1]))),
            resources=Resources({"lowercase":1}))
        self.lc2_all.flush_dataset()
        
    def estimate(self, spec_py=None, spec_var=None, spec_file=None):
        t1 = time()
        if spec_py is not None:
            reload(spec_py)
            spec_var = spec_py.specification
        if spec_var is not None:
            self.specification, variables, coefficents, equations, submodels = \
                self.load_specification_from_variable(spec_var)
        elif spec_file is not None:
            self.specification = EquationSpecification(in_storage=self.storage)
            self.specification.load(in_table_name=spec_file)

        self.specification.set_dataset_name_of_variables("land_cover")
        
        self.model_name = "land_cover_change_model"
        choices = range(1,15)
        lccm = LandCoverChangeModel(choices, submodel_string="lct")

        ## 4. select (uncomment) from one the following choices of subsetted sampling files (agents_index)
#        agents_index = where(self.lc1.get_attribute("sall_91_95_0"))[0]
        agents_index = where(self.lc1.get_attribute("sall_95_99_0"))[0]
#        agents_index = where(self.lc1.get_attribute("sall_99_02_0b"))[0]
#        agents_index = where(self.lc1.get_attribute("sa9902_9195_0"))[0]
#        agents_index = where(self.lc1.get_attribute("sa9902_9599_0"))[0]
#        agents_index = where(self.lc1.get_attribute("suburb91_95sample0"))[0]
#        agents_index = where(self.lc1.get_attribute("suburb95_99sample0"))[0]
#        agents_index = where(self.lc1.get_attribute("up91x95_old_samp0"))[0]
#        agents_index = where(self.lc1.get_attribute("urbsamp95_99_0"))[0]

        ## need to include agents_index_all seperate for the calibration portion
        ##    when using the dataset at the full extent, agents_index_all is needed as it is
        ##    created from the lc1_all agents_set and matches the size of the input data

        ## 5. select (uncomment) from one the following choices of sampling files (agents_index) at full spatial extent
#        agents_index_all = where(self.lc1_all.get_attribute("sall_91_95_0"))[0]
        agents_index_all = where(self.lc1_all.get_attribute("sall_95_99_0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("sall_99_02_0b"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("sa9902_9195_0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("sa9902_9599_0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("suburb91_95sample0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("suburb95_99sample0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("up91x95_old_samp0"))[0]
#        agents_index_all = where(self.lc1_all.get_attribute("urbsamp95_99_0"))[0]

        coef, results = lccm.estimate(self.specification, self.lc1, self.lc2, agents_index=agents_index, debuglevel=4)
        new_coef = lccm.calibrate(self.lc1_all, self.lc2_all, agents_index_all)
        specification = lccm.specification

        #save estimation results
#        out_suffix = spec_py.__name__[len(spec_py.__name__) - 11:]
        out_suffix = spec_py.__name__[30:]
        specification.write(out_storage=self.storage, out_table_name='lccm_specification_%sc' % out_suffix)
        new_coef.write(out_storage=self.storage, out_table_name='lccm_coefficients_%sc' % out_suffix)
            
        logger.log_status("Estimation done. %s s" % str(time()-t1))

    def load_specification_from_variable(self, spec_var):
        variables = []
        coefficients = []
        equations = []
        submodels = []
        try:
            for sub_model, submodel_spec in spec_var.items():
                if not isinstance(submodel_spec, dict):
                    raise ValueError, "Wrong specification format"
                if submodel_spec.has_key("equation_ids"):
                    equation_ids = submodel_spec["equation_ids"] ## this retrieves eq_ids from spec.py - they're stored in equations then passed to the equation specifications
                    del submodel_spec["equation_ids"]
                else:
                    equation_ids = None
                for var, coefs in submodel_spec.items():
                    if not equation_ids:
                        equation_ids = range(1, len(coeffs)+1)
                    for i in range(len(coefs)):
                        if coefs[i] != 0:
                            variables.append(var)
                            coefficients.append(coefs[i])
                            equations.append(equation_ids[i])
                            submodels.append(sub_model)
        except:
            raise ValueError, "Wrong specification format for submodel variable."

        specification = EquationSpecification(variables=variables, 
                                              coefficients=coefficients, 
                                              equations = equations,
                                              submodels=submodels)        
        return (specification, variables, coefficients, equations, submodels)

if __name__ == "__main__":
    estimator = LCCMEstimator(save_estimation_results=True, debuglevel=4)
    ## 6. select (uncomment) from one the following choices of model specifications
#    import estimation_lccm_specification_all91to95 as spec_py
#    import estimation_lccm_specification_all95to99 as spec_py
    import estimation_lccm_specification_all95to99_CAOs as spec_py

#    import estimation_lccm_specification_all99to02_minspec as spec_py
#    import estimation_lccm_specification_all99to02_nosmall_v1 as spec_py
#    import estimation_lccm_specification_all99to02_nosmall_v2 as spec_py
#    import estimation_lccm_specification_all99to02_nosmall_v3_from_allspec as spec_py

#    import estimation_lccm_specification_all99to02_all as spec_py
#    import estimation_lccm_specification_all99to02v3 as spec_py
#    import estimation_lccm_specification_all99to02v4_use4predictions as spec_py
#    import estimation_lccm_specification_all99to02v5_from_minspec as spec_py
#    import estimation_lccm_specification_all99to02v5_1_from_minspec as spec_py
#    import estimation_lccm_specification_all99to02v6_from_allspec as spec_py
    estimator.estimate(spec_py)
    