#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from baseline import Baseline

class BaselineMultipleRuns(Baseline):
    
    multiple_runs = True
    
    def __init__(self):
        config = Baseline()
        if self.multiple_runs:
            config.sample_inputs()
        config['years'] = (2001, 2005)
        config['number_of_runs'] = 50
        config['seed'] = 1
        config['description'] = 'baseline multiple runs'     
        self.merge(config)

    
if __name__ == "__main__":
    config = BaselineMultipleRuns()
