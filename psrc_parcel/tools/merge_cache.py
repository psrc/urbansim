from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.models.model import Model
from opus_core.logger import logger

class MergeCache(Model):
    """Merge multiple years of one cache directory into a single one that can be used 
    for example for a warm start."""
    def __init__(self, directory):
        self.storage = AttributeCache(directory)
    
    def run(self, year, cleanup_settings={}):
        SimulationState().set_current_time(year)
        tables = self.storage.get_table_names()
        # cleanup
        for table in tables:
            tabdata = self.storage.load_table(table)
            if table in cleanup_settings.keys():
                for attr in cleanup_settings[table]:
                    if attr in tabdata.keys():
                        logger.log_status('Deleting attribute %s in %s.' % (attr, table))
                        del tabdata[attr]
            self.storage.write_table(table, tabdata)
        logger.log_status('Deleting all computed tables.')
        self.storage.delete_computed_tables()
        logger.log_status('Cache directory merged into %s' % year) 
            
        
if __name__ == '__main__':
    # Cache directory to be merged
    dir = '/Users/hana/workspace/data/psrc_parcel/runs/run_106'
    # Which attributes to delete
    attributes_to_delete = ['new_zone_id', 'zone_id', 'faz_id', 'city_id', 'transaction_id', 'refinement_id']
    cleanup_settings = {'households': attributes_to_delete,
                        'jobs': attributes_to_delete}
    # output year into which the merged cache will be stored
    year = 2011
    # Run the model                    
    model = MergeCache(dir)
    model.run(year, cleanup_settings)
    