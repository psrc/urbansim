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

from inprocess.jrayers.excel_document import ExcelDocument
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.allocation_model import AllocationModel
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.store.file_flt_storage import file_flt_storage

print "geting excel document data"
excel_doc = ExcelDocument()
excel_doc.open('c:\\tmp\\TransientModel.xls')

list_of_column_names = ['year', 'persons']
list_of_ranges = ['d22:d32', 'k22:k32']
control_total_data = excel_doc.get_dict_table_from_column_names_and_ranges(list_of_column_names, list_of_ranges)

#print control_total_data

print "getting dict storage"
dict_storage = StorageFactory().get_storage('dict_storage')
dict_storage.write_table(table_name = 'control_totals', table_data = control_total_data)

print "getting esri storage"
esri_storage = StorageFactory().get_storage('esri_storage', storage_location='c:\\tmp\\tmp.gdb')

print "getting control total data as 'dataset'"
ct_data = Dataset(in_storage = dict_storage, in_table_name = 'control_totals', id_name='year')

print "getting hotel data as 'dataset'"
hotel_data = Dataset(in_storage=esri_storage, in_table_name='hotels', id_name='hotelid')

print "creating dataset pool"
dataset_pool = DatasetPool(storage=dict_storage, package_order=['urbansim_parcel', 'urbansim'])
dataset_pool._add_dataset('hotel_data', hotel_data)
dataset_pool._add_dataset('ct_data', ct_data)

print "creating allocation model"
model = AllocationModel()

model.run(hotel_data, outcome_attribute='persons', weight_attribute='rooms', control_totals=ct_data, current_year=2050, dataset_pool=dataset_pool)
result = hotel_data.get_attribute('persons')

#print "writing to cache"
#cache = file_flt_storage('c:\\tmp\\test_cache')
#hotel_data.write_dataset(out_storage=cache, out_table_name='hotels_with_persons')

excel_doc.close()
excel_doc.quit()
del excel_doc
