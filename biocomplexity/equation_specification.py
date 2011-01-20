# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.equation_specification import EquationSpecification as CoreEquationSpecification


class EquationSpecification(CoreEquationSpecification):
    # Names of attributes for specification data on storage
    field_submodel_id = 'from_id'
    field_equation_id = 'to_id'
    field_coefficient_name = 'coefficient_name'
    field_variable_name = 'variable_name'
