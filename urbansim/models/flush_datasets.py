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

from opus_core.model import Model

class FlushDatasets(Model):
    """Model for flushing given datasets into cache. This is especially useful, when we want 
    to flush dataset only in certain years, not every year, or not after each model 
    (which is done by the model system).
    """
    def run(self, datasets=[]):
        """
        Flush datasets given in the argument 'datasets' into cache.
        """
        for dataset in datasets:
            dataset.flush_dataset()
