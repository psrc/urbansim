# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger

try:
    import arcgisscripting, types, pywintypes, os
    from opus_core.store.storage import Storage
    from numpy import empty, append, ma, array
    from string import count, lower as lwr
    from random import randint

except:
    logger.log_warning('Could not load arcgisscripting module. Skipping.')

else:
    class esri_storage(Storage):
        """
        Testing an ESRI storage object
        TODO: needs better error checking throughout
            - deal with feature datasets in geodatabases
             - right now this ignores all tables/feature classes that exist
               in feature datasets unless the feature dataset is specified as
               part of the storage_location path
            - when creating a table, deal with table name length restrictions
            - handle single and double float types better when reading tables

        The storage_location can be a string representation of one of the following:
            - a directory path (e.g. 'c:/temp')
            - a path to a personal geodatabase (e.g. 'c:/temp/some_geodb.gdb')
            - a path to an existing ArcSDE database connection (e.g. 'Database Connections/your_db_conn.sde')
        """

        def __init__(self, storage_location):
            storage_location = os.path.normpath(storage_location)
            # Create ESRI Geoprocessing Object
            self.gp = arcgisscripting.create()
            # Check to see if storage_location exists
            if 'Database Connections' in storage_location:
                db_connection_file = os.path.split(storage_location)[-1]
                full_db_connection_file_path = os.path.join(os.environ['USERPROFILE'], 'Application Data\\ESRI\\ArcCatalog', db_connection_file)
                storage_location_exists = os.path.exists(full_db_connection_file_path)
                if not storage_location_exists:
                    raise IOError, 'The ArcSDE geodatabase connection "%s" does not exist.' % (db_connection_file)
                self.sde = True
            else:
                storage_location_exists = os.path.exists(storage_location)
                if not storage_location_exists:
                    raise IOError, 'The storage location "%s" does not exist.' % (storage_location)
                self.sde = False

            # Set the ESRI workspace parameter
            self.gp.Workspace = storage_location
            self._storage_location = storage_location

        def get_storage_location(self):
            return self._storage_location

        def get_full_table_location(self, table_name):
            storage_location = self.get_storage_location()
            if storage_location[-1] != '/':
                storage_location = storage_location + '/'
            full_table_name = storage_location + table_name
            return full_table_name

        def write_table(self, table_name, table_data, overwrite_existing=True):
            """
            This method writes a dataset (table_data) to the specified table (table_name).
            Set overwrite_existing = True if the table should be overwritten.
            """

            # Replace dashes in the table name with underscores
            table_name = table_name.replace('-', '_')

            # Reset the workspace
            self.gp.Workspace = self._storage_location
            # Get full path to table
            full_table_location = self.get_full_table_location(table_name)
            if overwrite_existing:
                self.gp.OverwriteOutput= 1
                if self.table_exists(table_name):
                    logger.log_note('The table with the name "%s" already exists.' % (table_name))
                    logger.log_note('This table will be overwritten.')
                    self.gp.Delete(full_table_location)
            else:
                self.gp.OverwriteOutput = 0
                if self.table_exists(table_name):
                    logger.log_note('The table with the name "%s" already exists.' % (table_name))
                    logger.log_note('This table will not be overwritten.')
                    return None

            # Determine table type to write
            storage_location = self.get_storage_location()
            if storage_location.find('.sde') > -1:
                dbf = False
            elif storage_location.find('.gdb') > -1:
                dbf = False
            elif storage_location.find('.mdb') > -1:
                dbf = False
            else:
                dbf = True

            # Create table
            if dbf:
                if table_name.find('.dbf') == -1:
                    table_name = table_name + '.dbf'
                    self.gp.CreateTable(storage_location, table_name)
                else:
                    self.gp.CreateTable(storage_location, table_name)
            else:
                table_name = self.gp.ValidateTableName(table_name)
                self.gp.CreateTable(storage_location, table_name)

            # Get column names
            column_names = []
            for i in table_data:
                column_names.append(i)
            # Get shortened column names
            short_column_names = []
            if dbf:
                for i in column_names:
                    if len(i) <= 10:
                        short_column_names.append(i)
                    else:
                        short_name = self._get_shortened_column_name(i, 8)
                        short_column_names.append(short_name)
            else:
                for i in column_names:
                    if len(i) <= 31:
                        short_column_names.append(i)
                    else:
                        short_name = self._get_shortened_column_name(i, 29)
                        short_column_names.append(i)
            # Create column_names to short_column_names mapping
            column_names_mapping = dict(zip(column_names, short_column_names))
            # Get column types
            numpy_column_types = []
            for i in column_names:
                numpy_column_types.append(table_data[i].dtype.kind)
            # Get ESRI column types
            esri_column_types = []
            for i in numpy_column_types:
                esri_column_types.append(self._get_esri_type_from_numpy_dtype(i))

            full_table_location = self.get_full_table_location(table_name)

            # Add columns
            x = 0
            for i in short_column_names:
                self.gp.AddField(full_table_location, i, esri_column_types[x])
                x += 1
            # Delete automatically added field if table of type .dbf
            if dbf:
                self.gp.DeleteField(full_table_location, 'Field1')

            # Insert records
            #
            # Get an ESRI InsertCursor on the table
            rows = self.gp.InsertCursor(full_table_location)
            # Get the number_of_records to insert
            number_of_records = len(table_data[column_names[0]])
            # Do the inserts
            for i in range(0, number_of_records):
                # Get an ESRI NewRow object
                row = rows.NewRow()
                for column_name, column_value in table_data.iteritems():
                    # Check for string value, if yes, insert quotes
                    if column_value[i].dtype.kind == 'S':
                        if "\'" in column_value[i]:
                            column_value[i] = column_value[i].replace("'", "\'")
                            strng = '''"''' + column_value[i] + '''"'''
                            exec_stmt = """row.%s = %s""" % (column_names_mapping[column_name], strng)
                        elif '\"' in column_value[i]:
                            column_value[i] = column_value[i].replace('"', '\"')
                            strng = """'""" + column_value[i] + """'"""
                            exec_stmt = """row.%s = %s""" % (column_names_mapping[column_name], strng)
                        else:
                            strng = """'""" + column_value[i] + """'"""
                            exec_stmt = """row.%s = %s""" % (column_names_mapping[column_name], strng)
                    else:
                        exec_stmt = """row.%s = %s""" % (column_names_mapping[column_name], column_value[i])
                    # Execute the statement built above
                    exec exec_stmt
                # Insert the row
                rows.InsertRow(row)

        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
            """
            The table_name parameter must be one of the following:
                - for Shapefiles: 'your_shapefile.shp'
                - for standalone .dbf tables: 'your_dbf.dbf'
                - for Feature Classes or tables in Geodatabases:
                    - personal gdb: 'your_fc_or_table_name'
                    - ArcSDE gdb in MSSQL Server: 'gdb_name.owner.table' (e.g. 'mygdb.SDE.parcels')

            The column_names parameter must be a Python list of strings
            representing the column names that should be loaded from the
            table.
            """

            # Reset the workspace
            self.gp.Workspace = self._storage_location
            # Check for table existence
            if not self.table_exists(table_name):
                logger.log_warning('Table with name "%s" does not exist.' % (table_name))
                return None

            # Get full path to table
            full_table_name = self.get_full_table_location(table_name)

            # Get columns
            if column_names == '*':
                columns = self.get_column_names(table_name, lowercase)
            else:
                columns = column_names
                if lowercase:
                    columns = [col.lower() for col in columns]

            # Get column types
            column_types = self._get_column_types_esri(table_name)
            numpy_column_dtypes = {}
            for i, j in column_types.iteritems():
                numpy_type = self._get_numpy_dtype_from_esri_dtype(j)
                numpy_column_dtypes[i] = numpy_type

            # Get rows
            rows = self.gp.SearchCursor(full_table_name)
            row = rows.Next()

            # Construct statement to get row values as a tuple (row_values)
            cols = []
            x = 0
            for i in columns:
                cols.append('row.' + columns[x])
                x += 1
            exec_stmt = 'row_values = ' + ', '.join(cols)

            # Create dictionary to populate with table values
            table = {}
            for i in columns:
                table[i] = empty(0, numpy_column_dtypes[i])

            # Populate dictionary with table values while
            # converting unicode and the special 'PyTime'
            # types to strings
            while row:
                exec exec_stmt
                if type(row_values) != types.TupleType:
                    row_values = (row_values,)
                x = 0
                for i in row_values:
                    if type(i) == types.UnicodeType:
                        i = str(i)
                    elif type(i) == pywintypes.TimeType:
                        i = str(i)
                    table[columns[x]] = append(table[columns[x]], i)
                    x += 1
                row = rows.Next()

            return table

        def get_column_names(self, table_name, lowercase=True):
            """
            Returns a list of column names.  Omits columns of type
            'OID' and 'Geometry' and those containing '.' (e.g.
            SHAPE.area, SHAPE.len)
            """

            # Reset the workspace
            self.gp.Workspace = self._storage_location
            # Check for table existence
            if not self.table_exists(table_name):
                logger.log_warning('Table with name "%s" does not exist.' % (table_name))
                return None

            # Create full path to table
            storage_location = self.get_storage_location()
            if not storage_location[-1] == '/':
                storage_location = storage_location + '/'
            full_table_name = storage_location + table_name

            # Get the column names
            fields = self.gp.ListFields(full_table_name)
            fields.Reset()
            field = fields.Next()
            column_names = []
            while field:
                if str(field.Type) == 'OID':
                    pass
                elif str(field.Type) == 'Geometry':
                    pass
                elif '.' in field.Name:
                    pass
                elif 'OBJECTID' in field.Name:
                    pass
                else:
                    column_names.append(str(field.Name))
                field = fields.Next()

            # Set column names to lowercase
            if lowercase:
                column_names = self._lower_case(column_names)

            return column_names

        def _get_column_types_esri(self, table_name):
            """
            Returns a dictionary of ESRI column types.  Omits columns of
            type 'OID' and 'Geometry' and those containing '.'
            (e.g. SHAPE.area, SHAPE.len).
            """

            # Reset the workspace
            self.gp.Workspace = self._storage_location
            # Create full path to table
            storage_location = self.get_storage_location()
            if not storage_location[-1] == '/':
                storage_location = storage_location + '/'
            full_table_name = storage_location + table_name

            # Get the column names
            fields = self.gp.ListFields(full_table_name)
            fields.Reset()
            field = fields.Next()
            #esri_column_types = []
            esri_column_types = {}
            while field:
                if str(field.Type) == 'OID':
                    pass
                elif str(field.Type) == 'Geometry':
                    pass
                elif '.' in field.Name:
                    pass
                elif 'OBJECTID' in field.Name:
                    pass
                else:
                    #esri_column_types.append(str(field.Type))
                    esri_column_types[str(lwr(field.Name))] = str(field.Type)
                field = fields.Next()

            return esri_column_types

        def get_table_names(self):
            """
            Returns a list of VALID table and feature class names in
            the specified storage_location.  If a gp.SearchCursor cannot be
            obtained by the ESRI Geoprocessing object, it is considered to be
            invalid.

            ESRI's Geoprocessor adds a .dbf to the table name string it returns
            if the table is a delimited type.  For instance if the table name
            ends in .txt, .csv, .tab, etc., it will return a .txt.dbf on the end.
            This method strips off the ending .dbf if it exists.
            """
            # Reset the workspace
            self.gp.Workspace = self._storage_location
            storage_location = self.get_storage_location()

            table_names = []

            # Get table names and add to the list if valid
            tables = self.gp.ListTables()
            tables.Reset()
            table = tables.Next()
            while table:
                if count(str(table), '.') > 1:
                    substitute_table_name = str(table).replace('.dbf', '')
                    if self._validate_table(substitute_table_name):
                        table_names.append(substitute_table_name)
                else:
                    if self._validate_table(table):
                        table_names.append(str(table))
                table = tables.Next()

            # Get feature class or shapefile names and
            # add them to the list if valid
            fcs = self.gp.ListFeatureClasses()
            fcs.Reset()
            fc = fcs.Next()
            while fc:
                if self._validate_table(fc):
                    table_names.append(str(fc))
                fc = fcs.Next()
            
            # Loop through table names and strip out any SDE specific naming if needed
            if self.sde:
                table_names_stripped = []
                for i in table_names:
                    x = i.split('.')
                    table_names_stripped.append(x[-1])
                return table_names_stripped
            else:
                return table_names

        def table_exists(self, table_name):
            # Reset the workspace
            self.gp.Workspace = self._storage_location
            if self.gp.Exists(table_name):
                return True
            else:
                return False

        def _validate_table(self, table_name):
            """
            This method attempts to get a gp.SearchCursor on the table.  If
            the ESRI Geoprocessor throws an exeption, the table is considered
            to be invalid.
            """
            # Reset the workspace
            self.gp.Workspace = self._storage_location

            try:
                self.gp.SearchCursor(table_name)
                return True
            except Exception, e:
                return False

        def _get_numpy_dtype_from_esri_dtype(self, esri_type):
            mapping = {
                        'SmallInteger': 'i',
                        'String': 'S',
                        'Double': 'f',
                        'Single': 'f',
                        'Date': 'S',
                        'Integer': 'i'
                      }
            try:
                numpy_dtype = mapping[esri_type]
            except:
                raise ValueError('Unrecognized ESRI type: %s' % esri_type)
            return numpy_dtype

        def _get_esri_type_from_numpy_dtype(self, numpy_dtype):
            mapping = {
                       'i':'LONG',
                       'f':'DOUBLE',
                       'S':'TEXT',
                       'b':'SHORT',
                       'U':'TEXT',
                       'u':'LONG',
                       'c':'DOUBLE',
                       'O':'TEXT',
                       'V':'TEXT'
                       }
            try:
                esri_type = mapping[numpy_dtype]
            except:
                raise ValueError('Unrecognized numpy type: %s' % numpy_dtype)
            return esri_type

        def _get_shortened_column_name(self, column_name, length):
            #Takes a string, reduces it to 'length' characters in
            #length, then adds a random number between 1 and 99
            #to make it somewhat unique
            rand = str(randint(0,99))
            short_name = column_name[0:length] + rand
            # Replace dashes with underscores (dashes are illegal in ESRI column names)
            short_name = short_name.replace('-', '_')
            return short_name


    from opus_core.tests import opus_unittest

    class TestStorage(opus_unittest.OpusTestCase):

        def setUp(self):
            # Get the opus core directory
            opus_core_directory = __import__('opus_core').__path__[0]
            # Set up paths to different data sources
            # TODO: figure out how to do this with SDE Geodatabases
            self.test_data_location_files = os.path.join(opus_core_directory, 'store', 'data', 'esri')
            self.test_data_location_file_geodb = os.path.join(opus_core_directory, 'store', 'data', 'esri', 'test_fgdb.gdb')
            self.test_data_location_personal_geodb = os.path.join(opus_core_directory, 'store', 'data', 'esri', 'test_pgdb.mdb')
            # Create different storage objects
            self.file_path_storage_object = esri_storage(self.test_data_location_files)
            self.file_geodb_storage_object = esri_storage(self.test_data_location_file_geodb)
            self.personal_geodb_storage_object = esri_storage(self.test_data_location_personal_geodb)

        def tearDown(self):
            # Delete schema.ini created by the ESRI geoprocessor:
            full_path_to_schema_ini = os.path.join(self.test_data_location_files, 'schema.ini')
            if os.path.exists(full_path_to_schema_ini):
                os.remove(full_path_to_schema_ini)
            # Delete other tables created by write tests below:
            # .dbf write test cleanup
            full_path_to_test_dbf_table = os.path.join(self.test_data_location_files, 'test_dbf_table.dbf')
            if os.path.exists(full_path_to_test_dbf_table):
                self.file_path_storage_object.gp.Delete(full_path_to_test_dbf_table)
            # file geodb write test cleanup
            full_path_to_test_filegdb_table = os.path.join(self.test_data_location_file_geodb, 'test_filegeodb_table')
            if self.file_geodb_storage_object.table_exists(full_path_to_test_filegdb_table):
                self.file_geodb_storage_object.gp.Delete(full_path_to_test_filegdb_table)
            # personal geodb write test cleanup
            full_path_to_test_personalgeodb_table = os.path.join(self.test_data_location_personal_geodb, 'test_personalgeodb_table')
            if self.personal_geodb_storage_object.table_exists(full_path_to_test_personalgeodb_table):
                self.personal_geodb_storage_object.gp.Delete(full_path_to_test_personalgeodb_table)

        def test_load_test_csv_tbl(self):
            esri_storage_object = self.file_path_storage_object
            loaded_csv_table = esri_storage_object.load_table('test_csv_tbl.csv')
            test_data_table = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_csv_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_tab_tbl(self):
            esri_storage_object = self.file_path_storage_object
            loaded_tab_table = esri_storage_object.load_table('test_tab_tbl.tab')
            test_data_table = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_tab_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_tbl_dbl_quoted_values(self):
            esri_storage_object = self.file_path_storage_object
            loaded_dbl_quoted_values = esri_storage_object.load_table('test_tbl_dbl_quoted_text_values.txt')
            test_data_table = {'fld2': array(['val2', 'val5'], dtype='|S4'),
                               'fld3': array(['val3', 'val6'], dtype='|S4'),
                               'fld1': array(['val1', 'val4'], dtype='|S4')}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_dbl_quoted_values[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_tbl_single_quoted_text_values(self):
            esri_storage_object = self.file_path_storage_object
            loaded_single_quoted_values = esri_storage_object.load_table('test_tbl_single_quoted_text_values.txt')
            test_data_table = {'fld2': array(["'val2'", "'val5'"], dtype='|S6'),
                               'fld3': array(["'val3'", "'val6'"], dtype='|S6'),
                               'fld1': array(["'val1'", "'val4'"], dtype='|S6')}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_single_quoted_values[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_txt_tbl(self):
            esri_storage_object = self.file_path_storage_object
            loaded_txt_table = esri_storage_object.load_table('test_txt_tbl.txt')
            test_data_table = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_txt_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_dbf_tbl(self):
            esri_storage_object = self.file_path_storage_object
            loaded_dbf_table = esri_storage_object.load_table('test_dbf_tbl.dbf')
            test_data_table = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_dbf_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_shapefile(self):
            esri_storage_object = self.file_path_storage_object
            loaded_shapefile_table = esri_storage_object.load_table('test_shapefile.shp')
            test_data_table = esri_storage_object.load_table('test_shapefile.shp')
            #test_data_table = {'date_fld': array(['1/1/2001 12:00:00 AM', '2/2/2002 12:00:00 AM', '3/3/2003 12:00:00 AM'], dtype='|S20'),
            #                   'int': array([1000000, 2000000, 3000000]),
            #                   'small_int': array([1, 2, 3]),
            #                   'single_fld': array([ 1.11110997,  2.22221994,  3.33332992]),
            #                   'string_fld': array(['string 1', 'string 2', 'string 3'], dtype='|S8'),
            #                   'double_fld': array([ 1.11111111,  2.22222222,  2.22222222])}
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_shapefile_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_get_table_names_from_file_path(self):
            esri_storage_object = self.file_path_storage_object
            table_names_in_path = ['test_csv_tbl.csv', 'test_tab_tbl.tab',
                                   'test_tbl_dbl_quoted_text_values.txt',
                                   'test_tbl_single_quoted_text_values.txt',
                                   'test_txt_tbl.txt', 'test_dbf_tbl.dbf',
                                   'test_shapefile.shp']
            test_table_names_in_path = esri_storage_object.get_table_names()
            self.assertEqual(test_table_names_in_path, table_names_in_path)

        def test_get_table_names_from_file_geodb(self):
            esri_storage_object = self.file_geodb_storage_object
            table_names_in_file_geodb = ['test_table', 'test_feature_class']
            test_table_names_in_file_geodb = esri_storage_object.get_table_names()
            self.assertEqual(table_names_in_file_geodb, test_table_names_in_file_geodb)

        def test_get_table_names_from_personal_geodb(self):
            esri_storage_object = self.personal_geodb_storage_object
            table_names_in_personal_geodb = ['test_table', 'test_feature_class']
            test_table_names_in_personal_geodb = esri_storage_object.get_table_names()
            self.assertEqual(table_names_in_personal_geodb, test_table_names_in_personal_geodb)

        def test_load_test_feature_class_from_file_geodb(self):
            esri_storage_object = self.file_geodb_storage_object
            loaded_feature_class = esri_storage_object.load_table('test_feature_class')
            test_data_table = esri_storage_object.load_table('test_feature_class')
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_feature_class[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_table_from_file_geodb(self):
            esri_storage_object = self.file_geodb_storage_object
            loaded_data_table = esri_storage_object.load_table('test_table')
            test_data_table = esri_storage_object.load_table('test_table')
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_data_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_feature_class_from_personal_geodb(self):
            esri_storage_object = self.personal_geodb_storage_object
            loaded_feature_class = esri_storage_object.load_table('test_feature_class')
            test_data_table = esri_storage_object.load_table('test_feature_class')
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_feature_class[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_load_test_table_from_personal_geodb(self):
            esri_storage_object = self.personal_geodb_storage_object
            loaded_data_table = esri_storage_object.load_table('test_table')
            test_data_table = esri_storage_object.load_table('test_table')
            for i in test_data_table:
                passed = False
                if ma.allequal(test_data_table[i], loaded_data_table[i]):
                    passed = True
                self.assertEqual(passed, True)

        def test_write_table_to_file_path(self):
            esri_storage_object = self.file_path_storage_object
            table_data = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            table_name = 'test_dbf_table.dbf'
            esri_storage_object.write_table(table_name, table_data)
            table_exists = esri_storage_object.table_exists(table_name)
            self.assertEqual(table_exists, True)

        def test_write_table_to_file_geodb(self):
            esri_storage_object = self.file_geodb_storage_object
            table_data = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            table_name = 'test_filegeodb_table'
            esri_storage_object.write_table(table_name, table_data)
            table_exists = esri_storage_object.table_exists(table_name)
            self.assertEqual(table_exists, True)

        def test_write_table_to_personal_geodb(self):
            esri_storage_object = self.personal_geodb_storage_object
            table_data = {'fld2': array([2, 5]), 'fld3': array([3, 6]), 'fld1': array([1, 4])}
            table_name = 'test_personalgeodb_table'
            esri_storage_object.write_table(table_name, table_data)
            table_exists = esri_storage_object.table_exists(table_name)
            self.assertEqual(table_exists, True)

    if __name__ == '__main__':
        opus_unittest.main()