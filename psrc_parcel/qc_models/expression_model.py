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
    
    default_expressions = {
       1: "job.job_id > 0",
       2: "household.household_id > 0",
       3: "household.building_id > 0",
       4: "building.building_id > 0",
       5: "building.parcel_id > 0",
       6: "parcel.parcel_id > 0",
       7: "parcel.zone_id > 0",
       # check the connection between buildings and parcels
       8: "(building.disaggregate(parcel.parcel_id) > 0)*(building.disaggregate(parcel.parcel_id) == building.parcel_id)",
       # do all household buildings exist
       9: "(household.disaggregate(building.building_id) > 0)*(household.disaggregate(building.building_id) == household.building_id)",
       10: "parcel.city_id > 0",
       11: "(parcel.disaggregate(city.county_id) > 0)*(parcel.disaggregate(city.county_id) == parcel.county_id)",
       12: ("is_element", ["parcel.city_id", "city.city_id"])
    }
    
    
    
    def __init__(self, dataset_pool=None):
        self.dataset_pool = dataset_pool

    def run(self, expressions={}, use_default_expressions=True, which_default_expressions=None, allow_missing=False):
        """
        Argument expressions should be dictionary of "name: condition" (same format as default_expressions). 
        By default the default_expressions above are included in the check. To switch it off, set
        "use_default_expressions" to False. To extract only a subset, which_default_expressions can be set to a list 
        of the expression names (keys in the expression dictionary).
        If the function should end gracefully without failing even if some datasets or attributes are missing,
        set "allow_missing" to True.
        """
        exprs = {}
        if use_default_expressions:
            exprs = self.default_expressions.copy()
            if which_default_expressions is not None: # subset default expressions
                exprs = {x: exprs[x] for x in which_default_expressions if x in exprs}
        exprs.update(expressions)
        df = pd.DataFrame(index=exprs.keys(), columns=["condition", "True", "False"])
        for name, expr in exprs.iteritems():
            values = self.compute_expression(expr, allow_missing=allow_missing)
            if values is None:
                df.loc[name, 'condition'] = expr
                continue
            df.loc[name] = [expr, (values <> 0).sum(), (values == 0).sum()]
        logger.log_status(df)
        return df

    def compute_expression(self, attribute_name, allow_missing=False):
        """Compute any expression and return its values. 
        If allow_missing is True, the code does not break if an attribute cannot be computed
        or a dataset is missing.
        """
        if isinstance(attribute_name, tuple): # method of this model
            try:
                func = getattr(self, attribute_name[0])
            except AttributeError:
                print 'Method "%s" not found.' % (attribute_name[0])
            else:
                return func(*attribute_name[1], allow_missing=allow_missing)            
            
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
        except (LookupError, FileNotFoundError, StandardError):
            if allow_missing:
                return np.zeros(ds.size(), dtype="bool8")
            raise
        
    def is_element(self, first, second, allow_missing=False):
        v1 = self.compute_expression(first, allow_missing=allow_missing)
        v2 = self.compute_expression(second, allow_missing=allow_missing)
        return np.in1d(v1, v2)
        
    
import os
from numpy import arange, array
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
        dspool = self.get_dataset_pool(['urbansim'])
        model = ExpressionModel(dspool)
        res = model.run(allow_missing=True)
        self.assertEqual(res.shape[0], len(model.default_expressions))
        
    def test_users_expressions(self):
        dspool = self.get_dataset_pool(['urbansim'])
        res = ExpressionModel(dspool).run(expressions={1:"gridcell.aggregate(job.home_based==1) <= gridcell.number_of_agents(job)"}, 
                                          use_default_expressions=False)
        self.assertEqual(res.shape[0], 1) # 1 row
        self.assertEqual(res.loc[1,"False"], 0) # all values should be True
        
    def test_my_inputs(self):
        parcels_data = {
            "parcel_id": arange(7)+1,
            "city_id": array([5, 0, 1, 1, 1, 2, 2])
        }
        buildings_data = {
            "building_id": arange(7)+1,
            "parcel_id": array([0,4,6,10,-1,3,1]),
                }
        cities_data = {
            "city_id": array([1,2,3])
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='parcels', table_data=parcels_data) 
        storage.write_table(table_name='buildings', table_data=buildings_data) 
        storage.write_table(table_name='cities', table_data=cities_data) 
        dspool = DatasetPool(['urbansim_parcel', 'urbansim'], storage=storage)
        res = ExpressionModel(dspool).run(which_default_expressions=range(4,9), allow_missing=True)
        self.assertEqual(res.shape[0], 5) # 5 rows
        self.assertEqual(res.loc[8,"False"], 3) # 3 values of building.parcel_id are non-existing

        
        
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/run_133/2010"
    #storage = storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    #dspool = DatasetPool(["urbansim_parcel"], storage=storage)
    #ExpressionModel(dspool).run()
    opus_unittest.main()