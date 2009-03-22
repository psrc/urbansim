# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from table_creator import TableCreator

class CreateBuildingsTable(TableCreator):
    def create_buildings_table(self, config, db_name):
        table_name = 'buildings'
        
        logger.log_status('Creating table %s.' % table_name)
        
        db = self._get_db(config, db_name)
        self._backup_table(db, table_name)
        self._drop_table(db, table_name)
        self._create_table(db, table_name)
        
    def _create_table(self, db, table_name):
        query = """
            create table buildings 
            select 
                grid_id, 
                year_built, 
                4 as building_type_id,
                residential_units, 
                0 as sqft,
                residential_improvement_value as improvement_value
            from gridcells 
            where
                residential_units > 0;
            
            insert into buildings 
            select 
                grid_id, 
                year_built, 
                1 as building_type_id,
                0 as residential_units, 
                commercial_sqft as sqft,
                commercial_improvement_value as improvement_value
            from gridcells 
            where
                commercial_sqft > 0;
            
            insert into buildings 
            select 
                grid_id, 
                year_built, 
                3 as building_type_id,
                0 as residential_units, 
                industrial_sqft as sqft,
                industrial_improvement_value as improvement_value
            from gridcells 
            where  
                industrial_sqft > 0;
            
            insert into buildings 
            select 
                grid_id, 
                year_built, 
                2 as building_type_id,
                0 as residential_units, 
                governmental_sqft as sqft,
                governmental_improvement_value as improvement_value
            from gridcells 
            where  
                governmental_sqft > 0;
            
            alter table buildings 
                add building_id int auto_increment primary key;
            
        """
        db.DoQuery(query)
