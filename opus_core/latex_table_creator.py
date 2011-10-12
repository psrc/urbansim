# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


import os

class LatexTableCreator(object):
        
    def create_latex_table_for_specifications_for_model(self, specification, model_name, dir):
        if specification is None:
            return
        from opus_core.latex import LaTeX
        spec_table = specification.get_table_summary()
        latex = LaTeX()
        # Latex does not like underscores in file names, so use hyphens instead.
        hyphenated_model_name = model_name.replace('_', '-')
        label = 'table:%s-specification' % hyphenated_model_name
        caption = '%s Specification' % model_name.replace('_', ' ').title()
        latex.save_specification_table_to_tex_file(spec_table, os.path.join(dir, hyphenated_model_name + '-specification.tex'),
                                                   label=label, caption=caption                                      )
    
    def create_latex_table_for_coefficients_for_model(self, coefficients, model_name, dir):
        """Write this model's coefficients to a LaTeX table in directory dir.
        Table is named as <model_name>_coefficients.tex.
        """
        if coefficients is None:
            return
        # Latex does not like underscores in file names, so use hyphens instead.
        hyphenated_model_name = model_name.replace('_', '-')
        label = 'table:%s-coefficients' % hyphenated_model_name
        caption = '%s Coefficients' % model_name.replace('_', ' ').title()
        coefficients.make_tex_table(os.path.join(dir, hyphenated_model_name + '-coefficients'),
                                    label=label, caption=caption)