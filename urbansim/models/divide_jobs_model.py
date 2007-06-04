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

from opus_core.model import Model

class DivideJobsModel(Model):
    def run(self, job_set, index, sectors_hb, sectors_nhbcom, sectors_nhbind, resources=None):
        return job_set.divide_into_hb_nhb_scalable(index, sectors_hb, sectors_nhbcom, sectors_nhbind, 
                                                    resources)
    
    def prepare_for_run(self, storage, comm_spec_table=None, ind_spec_table=None, hb_spec_table=None):
        from opus_core.equation_specification import EquationSpecification
        elcm_com_submodels = None 
        elcm_ind_submodels = None
        elcm_hb_submodels = None 
        elcm_com_specification = None 
        elcm_ind_specification = None
        elcm_hb_specification = None
        if comm_spec_table is not None:
            elcm_com_specification = EquationSpecification(in_storage=storage)
            elcm_com_specification.load(in_table_name=comm_spec_table)
            elcm_com_submodels = elcm_com_specification.get_distinct_submodels()
            
        if ind_spec_table is not None:
            elcm_ind_specification = EquationSpecification(in_storage=storage)
            elcm_ind_specification.load(in_table_name=ind_spec_table)
            elcm_ind_submodels = elcm_com_specification.get_distinct_submodels()

        if hb_spec_table is not None:
            elcm_hb_specification = EquationSpecification(in_storage=storage)
            elcm_hb_specification.load(in_table_name=hb_spec_table)
            elcm_hb_submodels = elcm_hb_specification.get_distinct_submodels()

        return (elcm_com_submodels, elcm_ind_submodels, elcm_hb_submodels, 
                 elcm_com_specification, elcm_ind_specification, elcm_hb_specification)