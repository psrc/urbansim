from opus_core.datasets.dataset_factory import DatasetFactory

#a simple script for creating a view on an indicator table 
#and the dataset spatial table for processing in postgis

def create_view(database, table_to_link_name, dataset_name):
    df = DatasetFactory()
    spatial_table_name = '%s_shp'%df._table_module_class_names_for_dataset(dataset_name)[0]
    spatial_table = database.get_table(spatial_table_name)
    table_to_link = database.get_table(table_to_link_name)
        
    spatial_primary_keys = database.get_primary_keys_for_table(spatial_table)
    table_to_link_primary_keys = database.get_primary_keys_for_table(table_to_link)

    primary_key_error_msg = 'The table %s either has no primary key or has a composite primary key. View creation does not support such tables'
    if spatial_primary_keys == [] or len(spatial_primary_keys) > 1 is not None:
        raise Exception(primary_key_error_msg%(spatial_table_name))
    if table_to_link_primary_keys == [] or len(table_to_link_primary_keys) > 1 is not None:
        raise Exception(primary_key_error_msg%(table_to_link_name))
    

    cols_from_spatial = [c.name for c in spatial_table.c]
    cols_from_linked = [c.name for c in table_to_link.c if c.name not in cols_from_spatial]
    
    cols = ','.join(['s.%s'%c for c in cols_from_spatial] +  ['l.%s'%c for c in cols_from_linked])

    params = {
      'join_col': table_to_link_primary_keys[0].name,
      'to_link':table_to_link,
      'spatial_table':spatial_table_name,
      'cols':cols,
      'spatial_key':spatial_primary_keys[0].name        
    }
    qry = ('''
           CREATE OR REPLACE VIEW %(to_link)s_view 
               AS SELECT %(cols)s from %(to_link)s as l, %(spatial_table)s as s
                    WHERE l.%(join_col)s=s.%(spatial_key)s
               
           '''%params)

    try:
        database.engine.execute(qry)
    except:
        print 'Error, could not create view'
        print qry
        import traceback
        traceback.print_exc()
        
#if __name__ == '__main__':
#    from opus_core.database_management.database_server import DatabaseServer
#    from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
#    
#    config = DatabaseServerConfiguration(protocol='postgres')
#    database_server = DatabaseServer(config)
#    database = database_server.get_database('psrc')
#    create_view(database = database,
#                table_to_link_name = 'zone_indicator_fixed',
#                dataset_name = 'zone')
        