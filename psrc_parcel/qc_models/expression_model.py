import numpy as np
import pandas as pd
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.variables.variable_name import VariableName
from opus_core.opus_error import FileNotFoundError

class ExpressionModel(Model):
    """
    Use this model to check values of various attributes that can be expressed in the Opus expression form.
    Expressions should be written in form of conditions. Alternatively, they can be defined as a tuple, 
    where the first value is a name of a function defined in this class which retuns an array of True and False, 
    and the second value is a list of arguments passed to that function (see the use of "is_element").
    The model results in a summary which counts the number of Trues and Falses of each expression.
    """
    
    default_expressions = {
       1: "job.job_id > 0",
       2: "job.building_id > 0",
       3: "household.household_id > 0",
       4: "household.building_id > 0",
       5: "building.building_id > 0",
       6: "building.parcel_id > 0",
       7: "parcel.parcel_id > 0",
       8: "parcel.zone_id > 0",
       9: "parcel.city_id > 0",
       # check the connection between buildings and parcels
       10: ("is_element", ["building.parcel_id", "parcel.parcel_id"]),
       # do all household's buildings exist or household is unplaced
       11: ("is_element", ["household.building_id", "building.building_id", [-1, 0]]),       
       # check county_id in parcels
       12: ("is_element", ["parcel.county_id", "city.county_id"]),
       # are all parcel.city_id present in the cities table 
       13: ("is_element", ["parcel.city_id", "city.city_id"]),
       # check that there are as many persons as the households attribute persons says
       14: "alldata.aggregate_all(household.persons) == alldata.aggregate_all(person.person_id > 0)",
       # all parcel.plan_type_id present in constraints table
       15: ("is_element", ["parcel.plan_type_id", "development_constraint.plan_type_id"]),
       # job sectors are in range 1-19
       16: ("is_element", ["job.sector_id", None, np.arange(1,20)]),
       # do all job's buildings exist or job is unplaced
       17: ("is_element", ["job.building_id", "building.building_id", [-1, 0]]),       
    }
    
    # non-critical checks (code will throw a warning if there is any False, otherwise an error)
    not_critical = [2,4]
    
    
    def __init__(self, dataset_pool=None):
        self.dataset_pool = dataset_pool

    def run(self, expressions={}, not_critical=[], use_default_expressions=True, which_default_expressions=None, 
             fault_tolerant=False):
        """
        Argument expressions should be a dictionary of "name: condition", or
        "name: (function_name, [args])" (i.e. the same format as default_expressions). 
        The argument "not_critical" is a list of names of expressions that are not critical to throw an error.
        By default the default_expressions above are included in the check. To switch it off, set
        "use_default_expressions" to False. To extract only a subset, which_default_expressions can be set to a list 
        of the expression names (keys in the expression dictionary).
        If the function should end gracefully without failing if some datasets or attributes are missing, 
        or if any of the critical conditions has Falses, set "fault_tolerant" to True.
        """
        exprs = {}
        if use_default_expressions:
            exprs = self.default_expressions.copy()
            if which_default_expressions is not None: # subset default expressions
                exprs = {x: exprs[x] for x in which_default_expressions if x in exprs}
        exprs.update(expressions)
        not_critical = not_critical + self.not_critical
        df = pd.DataFrame(index=exprs.keys(), columns=["condition", "True", "False"])
        warnings = []
        errors = []
        for name, expr in exprs.iteritems():
            values = self.compute_expression(expr, fault_tolerant=fault_tolerant)
            if values is None:
                df.loc[name, 'condition'] = expr
                warnings = warnings + [name]
                continue
            df.loc[name] = [expr, (values <> 0).sum(), (values == 0).sum()]
            if df.loc[name, "False"] > 0:
                if name in not_critical:
                    warnings = warnings + [name]
                else:
                    errors = errors + [name]
        logger.log_status(df)
        if len(warnings) > 0:
            logger.log_warning("False values found in conditions: %s" % warnings)
        if len(errors) > 0:
            logger.log_error("False values found in conditions: %s" % errors)        
            if not fault_tolerant:
                raise ValueError, "QC resutls: Found problems with the data."
        return df

    def compute_expression(self, attribute_name, fault_tolerant=False):
        """Compute any expression and return its values. 
        If fault_tolerant is True, the code does not break if an attribute cannot be computed
        or a dataset is missing.
        """
        if isinstance(attribute_name, tuple): # method of this model
            try:
                func = getattr(self, attribute_name[0])
            except AttributeError:
                print 'Method "%s" not found.' % (attribute_name[0])
            else:
                return func(*attribute_name[1], fault_tolerant=fault_tolerant)            
            
        var_name = VariableName(attribute_name)
        dataset_name = var_name.get_dataset_name()
        try:
            ds = self.dataset_pool.get_dataset(dataset_name)
        except FileNotFoundError:
            if fault_tolerant:
                return None
            raise
        try:
            return ds.compute_variables([var_name], dataset_pool=self.dataset_pool)
        except (LookupError, FileNotFoundError, StandardError):
            if fault_tolerant:
                return np.zeros(ds.size(), dtype="bool8")
            raise
        
    def is_element(self, first, second, additional_values=[], fault_tolerant=False):
        v1 = self.compute_expression(first, fault_tolerant=fault_tolerant)
        if not second is None:
            v2 = self.compute_expression(second, fault_tolerant=fault_tolerant)
        else:
            v2 = []
        return np.logical_or(np.in1d(v1, v2), np.in1d(v1, additional_values))
        
    
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
        res = model.run(fault_tolerant=True)
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
        res = ExpressionModel(dspool).run(which_default_expressions=range(5,11)+[13], fault_tolerant=True)
        self.assertEqual(res.shape[0], 7) # 7 rows
        self.assertEqual(res.loc[10,"False"], 3) # 3 values of building.parcel_id are non-existing
        self.assertEqual(res.loc[6,"False"], 2) # 2 buildings in no parcel
        self.assertEqual(res.loc[9,"False"], 1) # 1 wrong city_id in parcels
        self.assertEqual(res.loc[13,"False"], 2) # 2 non-existing city_id in parcels
        
        
        
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/run_133/2010"
    #storage = storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    #dspool = DatasetPool(["urbansim_parcel"], storage=storage)
    #ExpressionModel(dspool).run()
    opus_unittest.main()