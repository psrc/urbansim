import numpy as np
import pandas as pd
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.variables.variable_name import VariableName
from opus_core.opus_error import FileNotFoundError

class ExpressionModel(Model):
    """
    Use this model to check values of various attributes that can be expressed in the Opus expression form.
    Expressions should be written in form of conditions. The resulting summary counts the number of Trues and Falses of the expressions.
    """
    
    default_expressions = [
        "job.job_id > 0",
        "household.household_id > 0",
        "household.building_id > 0",
        "building.building_id > 0",
        "building.parcel_id > 0",
        "parcel.parcel_id > 0",
        "parcel.zone_id > 0"
    ]
    
    def __init__(self, dataset_pool=None):
        self.dataset_pool = dataset_pool

    def run(self, expressions=[], use_default_expressions=True, allow_missing=False):
        """
        By default the default_expressions above are included in the check. To switch it off, set
        "use_default_expressions" to False. 
        If the function should end gracefully without failing even if some datasets or attributes are missing,
        set "allow_missing" to True.
        """
        all_expressions = expressions
        if use_default_expressions:
            all_expressions = all_expressions + self.default_expressions
        df = pd.DataFrame(index=np.arange(len(all_expressions)), columns=["condition", "True", "False"])
        for iexpr in np.arange(len(all_expressions)):
            values = self.compute_expression(all_expressions[iexpr], allow_missing=allow_missing)
            if values is None:
                df.loc[iexpr, 'condition'] = all_expressions[iexpr]
                continue
            df.loc[iexpr] = [all_expressions[iexpr], (values <> 0).sum(), (values == 0).sum()]
        logger.log_status(df)
        return df

    def compute_expression(self, attribute_name, allow_missing=False):
        """Compute any expression and return its values. 
        If allow_missing is True, the code does not break if an attribute cannot be computed
        or a dataset is missing.
        """
        var_name = VariableName(attribute_name)
        dataset_name = var_name.get_dataset_name()
        try:
            ds = self.dataset_pool.get_dataset(dataset_name)
        except FileNotFoundError:
            if allow_missing:
                return None
            raise
        try:
            return ds.compute_variables([var_name], dataset_pool=self.dataset_pool)
        except LookupError:
            if allow_missing:
                return np.zeros(ds.size(), dtype="bool8")
            raise
    
import os
from opus_core.tests import opus_unittest
from opus_core.opus_package_info import package
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class TestExpressionModel(opus_unittest.OpusTestCase):
    def get_dataset_pool(self, package_order=["opus_core"]):
        opus_core_path = package().get_opus_core_path()
        cache_dir = os.path.join(opus_core_path, 'data', 'test_cache', '1980')
        storage = StorageFactory().get_storage('flt_storage', storage_location = cache_dir)
        return DatasetPool(package_order, storage=storage)
    
    def test_default_expressions(self):
        dspool = self.get_dataset_pool()
        model = ExpressionModel(dspool)
        res = model.run(allow_missing=True)
        self.assertEqual(res.shape[0], len(model.default_expressions))
        
    def test_users_expressions(self):
        dspool = self.get_dataset_pool(['urbansim'])
        res = ExpressionModel(dspool).run(expressions=["gridcell.aggregate(job.home_based==1) <= gridcell.number_of_agents(job)"], 
                                          use_default_expressions=False)
        self.assertEqual(res.shape[0], 1) # 1 row
        self.assertEqual(res.loc[0,"False"], 0) # all values should be True
        
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/run_133/2010"
    #storage = storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    #dspool = DatasetPool(["urbansim_parcel"], storage=storage)
    #ExpressionModel(dspool).run()
    opus_unittest.main()