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

except:
    logger.log_warning('Could not load arcgisscripting module. Skipping.')

else:
    class esri_storage(Storage):
        """
        Testing an ESRI storage object
        TODO: needs better error checking throughout
            - check for table existence
            - check for storage_location (workspace) existence

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

        def write_table(self):
            None

        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS):
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

            # Create full path to table
            storage_location = self.get_storage_location()
            if storage_location[-1] != '/':
                storage_location = storage_location + '/'
            full_table_name = storage_location + table_name

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
                        'SmallInteger': 'Int32',
                        'String': 'S',
                        'Double': 'Float64',
                        'Single': 'Float32',
                        'Date': 'S',
                        'Integer': 'Int64'
                      }
            return mapping[esri_type]

        def _get_esri_type_from_numpy_dtype(self, numpy_dtype):
            mapping = {
                       'i':'Integer',
                       'f':'Double',
                       'S':'String',
                       'b':'SmallInteger'
                       }
            return mapping[numpy_dtype]