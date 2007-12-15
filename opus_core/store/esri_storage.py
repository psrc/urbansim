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

from opus_core.logger import logger

try:
    import arcgisscripting, types
    from opus_core.store.storage import Storage
    from numpy import empty, append
    from string import count
    from random import randint

except:
    logger.log_warning('Could not load arcgisscripting module. Skipping.')

else:
    class esri_storage(Storage):
        """
        Testing an ESRI storage object
        TODO: needs better error checking throughout
            - check for table existence
            - check for storage_location (workspace) existence
            - deal with feature datasets in geodatabases
             - right now this assumes that all tables/feature classes
             are in the 'root' of the geodb
            - deal with unicode strings from ESRI text columns
              - do these need to be converted to numpy type String?
            - deal with additional field length constraints
             - already doing this for dbf, do the same for geodatabases

        The storage_location can be a string representation of one of the following:
            - a directory path (e.g. 'c:/temp')
            - a path to a personal geodatabase (e.g. 'c:/temp/some_geodb.gdb')
            - a path to an existing ArcSDE database connection (e.g. 'Database Connections/your_db_conn.sde')
        """

        def __init__(self, storage_location):

            # Create ESRI Geoprocessing Object
            self.gp = arcgisscripting.create()
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

        def write_table(self, table_name, table_data):

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
            if dbf == True:
                if table_name.find('.dbf') == -1:
                    table_name = table_name + '.dbf'
                    self.gp.CreateTable(storage_location, table_name)
                else:
                    self.gp.CreateTable(storage_location, table_name)
            else:
                table_name = self.gp.ValidateTableName(table_name)
                self.gp.CreateTable(storage_location, table_name)

            # Get full path to table
            full_table_location = self.get_full_table_location(table_name)

            # Get column names
            column_names = []
            for i in table_data:
                column_names.append(i)
            # Get shortened column names
            short_column_names = []
            for i in column_names:
                if len(i) <= 10:
                    short_column_names.append(i)
                else:
                    short_name = self._get_shortened_column_name(i)
                    short_column_names.append(short_name)
            # Get column types
            numpy_column_types = []
            for i in column_names:
                numpy_column_types.append(table_data[i].dtype.kind)
            # Get ESRI column types
            esri_column_types = []
            for i in numpy_column_types:
                esri_column_types.append(self._get_esri_type_from_numpy_dtype(i))

            # Add fields
            x = 0
            for i in short_column_names:
                self.gp.AddField(full_table_location, i, esri_column_types[x])
                x += 1
            # Delete automatically added field if table of type .dbf
            if dbf == True:
                self.gp.DeleteField(full_table_location, 'Field1')

            # Insert records




        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS):
            """
            TODO:
                - Convert any dates from date fields to strings
                 - at this point this method reads in dates as python objects
                 into the numpy array instead of strings
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

            # Get full path to table
            full_table_name = self.get_full_table_location(table_name)

            # Get columns
            if column_names == '*':
                columns = self.get_column_names(table_name)
            else:
                columns = column_names

            # Get column types
            column_types = self.get_column_types_esri(table_name)
            numpy_column_dtypes = []
            for i in column_types:
                numpy_type = self._get_numpy_dtype_from_esri_dtype(i)
                numpy_column_dtypes.append(numpy_type)

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
            x = 0
            for i in columns:
                table[i] = empty(0, numpy_column_dtypes[x])
                x += 1

            # Populate dictionary with table values
            while row:
                exec exec_stmt
                if type(row_values) != types.TupleType:
                    row_values = (row_values,)
                x = 0
                for i in row_values:
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

            # Create full path to table
            storage_location = self.get_storage_location()
            if storage_location[-1] != '/':
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
                else:
                    column_names.append(str(field.Name))
                field = fields.Next()

            # Set column names to lowercase
            if lowercase:
                column_names = self._lower_case(column_names)

            return column_names

        def get_column_types_esri(self, table_name):
            """
            Returns a list of ESRI column types.  Omits columns of
            type 'OID' and 'Geometry' and those containing '.'
            (e.g. SHAPE.area, SHAPE.len).
            """

            # Create full path to table
            storage_location = self.get_storage_location()
            if storage_location[-1] != '/':
                storage_location = storage_location + '/'
            full_table_name = storage_location + table_name

            # Get the column names
            fields = self.gp.ListFields(full_table_name)
            fields.Reset()
            field = fields.Next()
            esri_column_types = []
            while field:
                if str(field.Type) == 'OID':
                    pass
                elif str(field.Type) == 'Geometry':
                    pass
                elif '.' in field.Name:
                    pass
                else:
                    esri_column_types.append(str(field.Type))
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

            storage_location = self.get_storage_location()

            table_names = []

            # Get table names and add to the list if valid
            tables = self.gp.ListTables()
            tables.Reset()
            table = tables.Next()
            while table:
                if count(str(table), '.') > 1:
                    substitute_table_name = str(table).replace('.dbf', '')
                    if self._validate_table(substitute_table_name) == True:
                        table_names.append(substitute_table_name)
                else:
                    if self._validate_table(table) == True:
                        table_names.append(str(table))
                table = tables.Next()

            # Get feature class or shapefile names and
            # add them to the list if valid
            fcs = self.gp.ListFeatureClasses()
            fcs.Reset()
            fc = fcs.Next()
            while fc:
                if self._validate_table(fc) == True:
                    table_names.append(str(fc))
                fc = fcs.Next()

            return table_names

        def table_exists(self, table_name):
            if self.gp.Exists(table_name) == True:
                return True
            else:
                return False

        def _validate_table(self, table_name):
            """
            This method attempts to get a gp.SearchCursor on the table.  If
            the ESRI Geoprocessor throws an exeption, the table is considered
            to be invalid.
            """

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

        def _get_shortened_column_name(self, column_name):
            #Takes a string, reduces it to 8 characters in
            #length, then adds a random number between 1 and 99
            #to make it somewhat unique
            rand = str(randint(0,99))
            short_name = column_name[0:8] + rand
            return short_name