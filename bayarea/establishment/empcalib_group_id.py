# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from bayarea.datasets.empcalib_group_dataset import EmpcalibGroupDataset, generate_unique_ids

class empcalib_group_id(Variable):
    """ Return the empcalib_group_id of establishment, 
    as defined in the datasets/empcalib_group_dataset.py
    """
    _return_type = "int32"
    
    def dependencies(self):
        return EmpcalibGroupDataset.subgroup_definition

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        variable_names = [VariableName(v) for v in self.dependencies()]
        assert ds.get_dataset_name() == variable_names[0].get_dataset_name()
        short_names = [vn.get_alias() for vn in variable_names]
        return generate_unique_ids(ds, short_names)[0]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

