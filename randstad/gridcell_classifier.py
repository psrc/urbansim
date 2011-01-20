# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, arange
from numpy import transpose, argmin, float32, reshape
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.development_type_dataset import DevelopmentTypeDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset

# This class is not tested by all_tests.py, why? The tests fail

class GridcellClassifier:
   """
   This class provides methods to re-classify the development type of gridcells.
   The main entry point is the set_development_type_for_gridcells_in_events method.
   """
   def __init__(self, development_types, sqft_per_unit=1000):
       self._development_types = development_types
       self._development_types.get_id_attribute()
       self._sqft_per_unit = sqft_per_unit

   def _distances(self, gridcells, devtype_id):
       """Returns the square of the distance between each gridcell
       in this array and this development type.  Assumes that the minimum and maximum
       value is identical within each dimension of the development type,
       e.g. min_units = max_units.
       """
       self._sqft_per_unit = 1000.0
       unit_dist = (gridcells.get_attribute('residential_units')
                     - self._development_types.get_attribute_by_id('min_units', [devtype_id]))**2
       commercial_sqft_dist = ((gridcells.get_attribute('commercial_sqft')
                                - self._development_types.get_attribute_by_id('min_commercial_sqft', [devtype_id]))
                               / self._sqft_per_unit)**2
       industrial_sqft_dist = ((gridcells.get_attribute('industrial_sqft')
                                - self._development_types.get_attribute_by_id('min_industrial_sqft', [devtype_id]))
                               / self._sqft_per_unit)**2
       governmental_sqft_dist = ((gridcells.get_attribute('governmental_sqft')
                                  - self._development_types.get_attribute_by_id('min_governmental_sqft', [devtype_id]))
                                 / self._sqft_per_unit)**2
       return (unit_dist
               + commercial_sqft_dist
               + industrial_sqft_dist
               + governmental_sqft_dist)

   def get_closest_development_type(self, gridcells, devtype_ids_to_use=None):
       """Returns the closest development type for each gridcell in
       the array of gridcells.  If two development types are equally close,
       use the development_type with the lowest index.  Only check development
       types in devtype_ids_to_use, if that argument is provided.
       """
       gridcells.get_id_attribute()
       if devtype_ids_to_use == None:
           devtype_ids_to_use = self._development_types.get_id_attribute()
       else:
           devtype_ids_to_use = array(devtype_ids_to_use)
       distances = reshape(arange(devtype_ids_to_use.size * gridcells.size()),
                          (devtype_ids_to_use.size, gridcells.size())).astype(float32)
       i = 0
       for devtype_id in devtype_ids_to_use:
           distances[i] = self._distances(gridcells, devtype_id)
           i += 1
       close_devtype_ids = argmin(transpose(distances))
       i = 0
       for id in close_devtype_ids:
           close_devtype_ids[i] = devtype_ids_to_use[id]
           i += 1
       return close_devtype_ids

   def set_development_type_for_gridcells_in_events(self, gridcells, events,
                                                    devtype_ids_to_use=None):
       """
       For each gridcell in this DevelopmentEvents dataset, set
       its development type to be the closest development type
       from the development_types table, regardless of the 'year'
       of this development event.  The devtype_ids_to_use parameter
       specifies a subset of the development types to consider; if
       not provided, all development types are considered.
       Closeness is defined as the Euclidean distance in the 4-dimensional
       space with axes of residential_units, commercial_sqft, industrial_sqft,
       and governmental_sqft.  When computing the distance, one residentail unit
       is considered to be sqft_per_unit sqft, so that all axes have the same
       "units".  When several development types are equally close, it is
       undefined which one will be choosen, since we cannot guarantee the
       order of the rows in the development types dataset.
       """
       # get ids for gridcells in events
       gc_subset = gridcells.create_subset_window_by_ids(events.get_attribute('grid_id'))
       new_devtypes = self.get_closest_development_type(gc_subset, devtype_ids_to_use)
       gridcells.set_values_of_one_attribute('development_type_id',
                                             new_devtypes,
                                             gc_subset.get_index())

if __name__ == "__main__":
   from opus_core.tests import opus_unittest
   from opus_core.resources import Resources
   from opus_core.storage_factory import StorageFactory
   from numpy import alltrue

   class Tests(opus_unittest.OpusTestCase):

        def test_unit_distance(self):
            storage = StorageFactory().get_storage('dict_storage')

            gridcells_table_name = 'gridcells'
            
            storage.write_table(table_name = gridcells_table_name, 
                table_data = {'grid_id': array([1,2,3]),
                              'residential_units':array([0,8,12]),
                                'commercial_sqft':array([0,0,0]),
                               'industrial_sqft':array([0,0,0]),
                               'governmental_sqft':array([0,0,0])
                             }
                )

            devtypes_table_name = 'devtypes'
            
            storage.write_table(
                    table_name = devtypes_table_name,
                    table_data = {
                        'development_type_id': array([1,2]),
                        'min_units':array([0,10]),
                        'min_commercial_sqft':array([0,0]),
                        'min_industrial_sqft':array([0,0]),
                        'min_governmental_sqft':array([0,0])
                        }
                )

            gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

            devtypes = DevelopmentTypeDataset(
                in_storage = storage,
                in_table_name = devtypes_table_name,
                id_name = 'development_type_id',
                use_groups = False
                )

            classifier = GridcellClassifier(devtypes)
            distance = classifier._distances(gridcells, 1)
            self.assert_(alltrue(distance == array([0,8*8,12*12])))

        def test_closest_devtype_sqft(self):
            storage = StorageFactory().get_storage('dict_storage')
            
            gridcells_table_name = 'gridcells'
            storage.write_table(
                table_name = gridcells_table_name,
                    table_data = {
                        'grid_id': array([1,2,3]),
                        'residential_units':array([0,0,0]),
                        'commercial_sqft':array([300,700,900]),
                        'industrial_sqft':array([0,0,0]),
                        'governmental_sqft':array([0,0,0])
                        }
                )

            devtypes_table_name = 'devtypes'
            storage.write_table(
                table_name = devtypes_table_name,
                    table_data = {
                        'development_type_id': array([1,2]),
                        'min_units':array([0,0]),
                        'min_commercial_sqft':array([500,1000]),
                        'min_industrial_sqft':array([0,0]),
                        'min_governmental_sqft':array([0,0])
                        },
                )

            gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

            devtypes = DevelopmentTypeDataset(
                in_storage = storage,
                in_table_name = devtypes_table_name,
                id_name = 'development_type_id',
                use_groups = False
                )

            classifier = GridcellClassifier(devtypes)
            dts = classifier.get_closest_development_type(gridcells)
            self.assert_(alltrue(dts == array([1,1,2])))

        def test_closest_devtype_units_and_sqft(self):
            storage = StorageFactory().get_storage('dict_storage')


            gridcells_table_name = 'gridcells'
            storage.write_table(
                    table_name = gridcells_table_name,
                    table_data = {
                        'grid_id': array([1,2,3,4]),
                        'residential_units':array([0,0,0,1]),
                        'commercial_sqft':array([300,700,900,900]),
                        'industrial_sqft':array([0,0,0,0]),
                        'governmental_sqft':array([0,0,0,0])
                        },                    
                )

            devtypes_table_name = 'devtypes'
            
            storage.write_table(
                     table_name = devtypes_table_name,
                     table_data = {
                        'development_type_id': array([1,2,3]),
                        'min_units':array([1,0,0]),
                        'min_commercial_sqft':array([500,0,1000]),
                        'min_industrial_sqft':array([0,0,0]),
                        'min_governmental_sqft':array([0,0,0])
                        },
                )

            gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

            devtypes = DevelopmentTypeDataset(
                in_storage = storage,
                in_table_name = devtypes_table_name,
                id_name = 'development_type_id',
                use_groups = False
                )

            classifier = GridcellClassifier(devtypes)
            dts = classifier.get_closest_development_type(gridcells)
            self.assert_(alltrue(dts == array([2,3,3,1])))

        def test_closest_devtype_units(self):
            storage = StorageFactory().get_storage('dict_storage')

            gridcells_table_name = 'gridcells'
            
            storage.write_table(
                    table_name = gridcells_table_name,
                    table_data = {
                        'grid_id': array([1,2,3]),
                        'residential_units':array([0,8,12]),
                        'commercial_sqft':array([0,0,0]),
                        'industrial_sqft':array([0,0,0]),
                        'governmental_sqft':array([0,0,0])
                        }
               )

            devtypes_table_name = 'devtypes'
            storage.write_table(
                    table_name = devtypes_table_name,
                    table_data = {
                        'development_type_id': array([1,2]),
                        'min_units':array([0,10]),
                        'min_commercial_sqft':array([0,0]),
                        'min_industrial_sqft':array([0,0]),
                        'min_governmental_sqft':array([0,0])
                        }
                )

            gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

            devtypes = DevelopmentTypeDataset(
                in_storage = storage,
                in_table_name = devtypes_table_name,
                id_name = 'development_type_id',
                use_groups = False
                )

            classifier = GridcellClassifier(devtypes)
            dts = classifier.get_closest_development_type(gridcells)
            self.assert_(alltrue(dts == array([1,2,2])))

        def test_subset_of_devtypes(self):
            storage = StorageFactory().get_storage('dict_storage')

            gridcells_table_name = 'gridcells'
            storage.write_table(
                    table_name = gridcells_table_name,
                    table_data = {
                        'grid_id': array([1,2,3,4]),
                        'residential_units':array([0,0,0,1]),
                        'commercial_sqft':array([300,700,900,900]),
                        'industrial_sqft':array([0,0,0,0]),
                        'governmental_sqft':array([0,0,0,0])
                        }
              )

            devtypes_table_name = 'devtypes'
            storage.write_table(
                    table_name = devtypes_table_name,
                    table_data = {
                        'development_type_id': array([1,2,3]),
                        'min_units':array([1,0,0]),
                        'min_commercial_sqft':array([500,0,1000]),
                        'min_industrial_sqft':array([0,0,0]),
                        'min_governmental_sqft':array([0,0,0])
                        }
                )

            gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

            devtypes = DevelopmentTypeDataset(
                in_storage = storage,
                in_table_name = devtypes_table_name,
                id_name = 'development_type_id',
                use_groups = False
                )

            classifier = GridcellClassifier(devtypes)
            dts = classifier.get_closest_development_type(gridcells,
                                                      devtype_ids_to_use=[1,3])
            self.assert_(alltrue(dts == array([3,3,3,1])))

   opus_unittest.main()