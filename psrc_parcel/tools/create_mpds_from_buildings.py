from numpy import where, all, unique, array, zeros, logical_not, round
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
        
    def compute_building_variables(self):
        self.input_buildings.compute_variables(["land_use_type_id = building.disaggregate(parcel.land_use_type_id)",
                                                "urbansim_parcel.building.is_residential"], 
                                               dataset_pool=self.dataset_pool)
                                               
    def preprocess_datasets(self):
        self.compute_building_variables()
        # consolidate buildings of the same type on the same parcel
        parcels = self.dataset_pool.get_dataset('parcel')
        number_of_buildings = parcels.compute_variables("number_of_buildings = parcel.number_of_agents(building)", 
                                               dataset_pool=self.dataset_pool)
        multiple_bldg_parcels = where(number_of_buildings > 1)[0]
        bldgs_to_remove = zeros(self.input_buildings.size(), dtype='bool8')
        consolidated = array([0, 0])
        print "Original total: %s buildings" % self.input_buildings.size()
        for i in multiple_bldg_parcels:
            bidx = where(self.input_buildings['parcel_id'] == parcels["parcel_id"][i])[0]
            bts = unique(self.input_buildings["building_type_id"][bidx])         
            if bts.size == 1:
                cons_idx = bidx[0]
                for attr in ["non_residential_sqft", "land_area", "residential_units"]:
                    self.input_buildings[attr][cons_idx] = self.input_buildings[attr][bidx].sum()
                if self.input_buildings["is_residential"][cons_idx]:
                    unitattr = "residential_units"
                else:
                    unitattr = "non_residential_sqft"
                totsqft = self.input_buildings[unitattr][bidx] * self.input_buildings["sqft_per_unit"][bidx]
                self.input_buildings[unitattr][cons_idx] = round(totsqft.sum()/self.input_buildings[unitattr][cons_idx].astype("float32"))
                bldgs_to_remove[bidx[1:]] = True
                consolidated = consolidated + array([1, bidx.size])
                continue
            bldgs_to_remove[bidx] = True
            self.parcels_not_processed = self.parcels_not_processed + [parcels["parcel_id"][i]]
        self.input_buildings.subset_by_index(where(logical_not(bldgs_to_remove))[0])
        
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
    
    