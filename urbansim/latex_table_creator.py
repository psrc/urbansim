# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


import os
from opus_core.latex_table_creator import LatexTableCreator as CoreLatexTableCreator
from urbansim.model_coordinators.model_system import ModelSystem
from opus_core.storage_factory import StorageFactory
from opus_core.model import prepare_specification_and_coefficients
from opus_core.configuration import Configuration

class LatexTableCreator(CoreLatexTableCreator):
    def create_latex_tables_for_model(self, config, model_name, dir):
        """Write to directory dir a file containing a LaTeX table describing this model's 
        coefficients, and a file containing a LaTeX table describing this model's specification.
        Files will be named named <model_name>_coefficients.tex and <model_name>_specification.tex.
        """
        config = Configuration(config)
        model_system = ModelSystem()
        input_db, output_db = model_system._get_database_connections(config)
        sql_storage = StorageFactory().get_storage('sql_storage', storage_location=input_db)
        #TODO: only do the next stuff if this model has coefficients
        if 'controller' not in config['models_configuration'][model_name]:
            return
        if 'prepare_for_run' not in config['models_configuration'][model_name]['controller']:
            return
        if 'coefficients' not in config['models_configuration'][model_name]['controller']['prepare_for_run']['output']:
            return
        specification_table_name = config['models_configuration'][model_name].get('specification_table', None)
        coefficents_table_name = config['models_configuration'][model_name].get('coefficients_table', None)
        (specification, coefficients) = prepare_specification_and_coefficients(
            specification_storage=sql_storage,
            specification_table=specification_table_name,
            coefficients_storage=sql_storage,
            coefficients_table=coefficents_table_name)

        self.create_latex_table_for_coefficients_for_model(coefficients, model_name, dir)
        self.create_latex_table_for_specifications_for_model(specification, model_name, dir)
        