#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

class Visualizer:

    def visualize(self, indicators, *args, **kwargs):
        raise 'visualize not implemented'
    
    




    def test__output_types(self):
        from inprocess.travis.opus_core.indicator_framework.visualizers.table import Table
        
        output_types = ['csv','tab']
        try:        
            import dbfpy
        except ImportError:
            pass
        else:
            output_types.append('dbf')
            
        for output_type in output_types:
            table = Table(
                source_data = self.cross_scenario_source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                output_type = output_type)
            
            table.create(False)
            path = table.get_file_path()
            self.assertEqual(os.path.exists(path), True)