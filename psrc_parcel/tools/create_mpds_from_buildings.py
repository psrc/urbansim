from numpy import where, all, unique, array, zeros, logical_not, logical_and, round, arange
from numpy import in1d, argmin, abs
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
        self.original_templates = None
        
    def compute_building_variables(self):
        self.input_buildings.compute_variables(["land_use_type_id = building.disaggregate(parcel.land_use_type_id)",
                                                "urbansim_parcel.building.is_residential"], 
                                               dataset_pool=self.dataset_pool)
                       
    def get_units(self, idx):
        if self.input_buildings["is_residential"][idx] and self.input_buildings["residential_units"][idx] > 0:
            return "residential_units"
        return "non_residential_sqft"
                      
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
                unitattr = self.get_units(cons_idx)
                totsqft = self.input_buildings[unitattr][bidx] * self.input_buildings["sqft_per_unit"][bidx]
                if self.input_buildings[unitattr][cons_idx] > 0:
                    self.input_buildings["sqft_per_unit"][cons_idx] = round(totsqft.sum()/self.input_buildings[unitattr][cons_idx].astype("float32"))
                bldgs_to_remove[bidx[1:]] = True
                consolidated = consolidated + array([1, bidx.size])
                continue
            bldgs_to_remove[bidx] = True
            self.parcels_not_processed = self.parcels_not_processed + [parcels["parcel_id"][i]]
        self.input_buildings.subset_by_index(where(logical_not(bldgs_to_remove))[0])
        if "template_id" in self.input_buildings.get_known_attribute_names():
            self.original_templates = self.input_buildings["template_id"].copy()
        self.input_buildings.add_attribute(zeros(self.input_buildings.size(), dtype="int32"), name="template_id",
                                           metadata=1)
        print "%s buildings consolidated into %s." % (consolidated[1], consolidated[0])
        print "%s parcels were not processed." % len(self.parcels_not_processed)
        print "Updated total: %s buildings." % self.input_buildings.size()
        
    def run(self, outstorage, output_table=None):
        templates = self.dataset_pool.get_dataset("development_template")
        template_comps = self.dataset_pool.get_dataset("development_template_component")
        templates.compute_variables(["urbansim_parcel.development_template.density_converter", 
                                     "number_of_components = (development_template.number_of_agents(development_template_component)).astype(int32)"],
                                            dataset_pool=self.dataset_pool)
        land_sqft = self.input_buildings["land_area"]
        results = self.input_buildings["template_id"]
        no_template_found = []
        for bidx in arange(self.input_buildings.size()):
            # match by land use type and building type
            #templ_match = templates["land_use_type_id"] == self.input_buildings["land_use_type_id"][bidx]
            templ_match = templates["number_of_components"] == 1
            comp_match = template_comps["building_type_id"] == self.input_buildings["building_type_id"][bidx]
            templ_match = logical_and(templ_match, in1d(templates["template_id"], template_comps["template_id"][where(comp_match)]))
            # match land area            
            templ_match = logical_and(templ_match, 
                                      logical_and(land_sqft[bidx] <= templates["land_sqft_max"],
                                                  land_sqft[bidx] >= templates["land_sqft_min"]))
            templ_idx = where(templ_match)[0]
            if templ_idx.size == 0:
                results[bidx] = -1
                no_template_found = no_template_found + [bidx]
                continue
            units = zeros(templ_idx.size, dtype='float32')
            for i in arange(templ_idx.size):
                units[i] = self.input_buildings["land_area"][bidx]*(1-templates["percent_land_overhead"][templ_idx[i]]/100.0)*templates["density"][templ_idx[i]]*templates["density_converter"][templ_idx[i]]
            unitattr = self.get_units(bidx)
            winner_templ = argmin(abs(units - self.input_buildings[unitattr][bidx]))
            all_winners = units == units[winner_templ]
            if all_winners.sum() > 1: # more than 1 winner
                # choose the one with matching land use type
                lut_match = templates["land_use_type_id"] == self.input_buildings["land_use_type_id"][bidx]
                winners = logical_and(all_winners, lut_match[templ_idx])
                if winners.any():
                    winner_templ = where(winners)[0][0]
            results[bidx] = templates["template_id"][templ_idx[winner_templ]]
        # write results
        if self.original_templates is not None:
            self.input_buildings.add_attribute(self.original_templates, name="original_template_id", metadata=1)
        self.input_buildings.write_dataset(out_storage=outstorage, out_table_name=output_table, attributes=1)
        print "No template found for %s buildings." % len(no_template_found)
            
if __name__ == '__main__':
    ### User's settings:
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_data/2000"
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/MPDs/inverse_templates"
    #input_buildings_table = "buildings1999"
    input_buildings_table = None
    #buildings_filter = None # if input_buildings_table is None, use this to filter out buildings from the input cache 
    buildings_filter = "building.year_built==2025"
    output_cache =  "/Users/hana/workspace/data/psrc_parcel/MPDs/inverse_templates"
    output_buildings_table = "buildings1999out"
    output_buildings_table = "buildings2025out"
    ### End of user's settings
    instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    model = InverseMPDs(instorage, input_buildings_table, buildings_filter)
    model.preprocess_datasets()
    model.run(outstorage, output_table=output_buildings_table)
    #TODO: Compare templates id (2004 buildings)
    