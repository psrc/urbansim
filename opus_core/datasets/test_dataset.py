#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from numpy import array
from opus_core.datasets.dataset import Dataset

class TestDataset(Dataset):
    """Dataset for unit tests.
    """
    
    def __init__(self, *args, **kwargs):
        Dataset.__init__(
            self, 
            dataset_name="test",
            id_name="id",
            in_table_name=kwargs.get('in_table_name','tests'),
            in_storage=kwargs['in_storage']
        )
