from numpy import where, arange, all, unique, concatenate, array
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool


class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
class InverseMPDs:
    def __init__(self, storage, input_table=None, filter=None):
        self.dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        if input_table is not None:
            self.input_buildings = self.dataset_pool.get_dataset('building', 
                                                dataset_arguments={"in_table_name":input_table})
        elif filter is not None:
            self.input_buildings = self.dataset_pool.get_dataset('building')
            ind = self.input_buildings.compute_variables(filter, dataset_pool=self.dataset_pool)
            self.input_buildings.subset_by_index(where(ind > 0)[0])
        else:
            raise InputError, "Either input_table or filter must be given."
        self.parcels_not_processed = []
        
    def compute_land_use_type(self):
        self.input_buildings.compute_variables("land_use_type_id = building.disaggregate(parcel.land_use_type_id)", 
                                               dataset_pool=self.dataset_pool)
                                               
    def preprocess_datasets(self):
        print "Original total: %s buildings" % self.input_buildings.size()
        self.compute_land_use_type()
        # consolidate buildings of the same type on the same parcel
        parcels = self.dataset_pool.get_dataset('parcel')
        number_of_buildings = parcels.compute_variables("number_of_buildings = parcel.number_of_agents(building)", 
                                               dataset_pool=self.dataset_pool)
        multiple_bldg_parcels = where(number_of_buildings > 1)[0]
        bldgs_to_remove = array([], dtype='int32')
        consolidated = array([0, 0])
        for i in multiple_bldg_parcels:
            bidx = where(self.input_buildings['parcel_id'] == parcels["parcel_id"][i])[0]
            bts = unique(self.input_buildings["building_type_id"][bidx])         
            if bts.size == 1:
                cons_idx = bidx[0]
                for attr in ["non_residential_sqft", "land_area", "residential_units"]:
                    self.input_buildings[attr][cons_idx] = self.input_buildings[attr][bidx].sum()
                #TODO: ? sqft_per_unit
                bldgs_to_remove = concatenate((bldgs_to_remove, bidx[1:]))
                consolidated = consolidated + array([1, bidx.size])
                continue
            self.parcels_not_processed = self.parcels_not_processed + [parcels["parcel_id"][i]]
        self.input_buildings.subset_by_index(bldgs_to_remove)
        
        print "%s buildings consolidated into %s." % (consolidated[1], consolidated[0])
        print "%s parcels were not processed." % len(self.parcels_not_processed)
        print "Updated total: %s buildings." % self.input_buildings.size()
        
    def run(self):
        pass
        
if __name__ == '__main__':
    ### User's settings:
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_data/2000"
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/MPDs/inverse_templates"
    output_dir =  "/Users/hana/workspace/data/psrc_parcel/MPDs/inverse_templates"
    input_buildings_table = "buildings1999"
    buildings_filter = None # if input_buildings_table is None, use this to filter out buildings from the input cache 
    ### End of user's settings
    instorage = FltStorage().get(input_cache)
    model = InverseMPDs(instorage, input_buildings_table, buildings_filter)
    model.preprocess_datasets()
    model.run()
    
    