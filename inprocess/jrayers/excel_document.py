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

# TODO:expand this class into a full excel storage object

from opus_core.logger import logger
from numpy import empty, append, ma, array

try:
    from win32com.client import Dispatch
    import os

except:
    logger.log_warning('Could not load win32com.client module. Skipping.')

else:
    class ExcelDocument(object):
        """
        A class for accessing data in an Excel document.
        """
        def __init__(self, visible=False):
            self.app = Dispatch("Excel.Application")
            self.app.Visible = visible
            self.sheet = 1
        
        def open(self, filename):
            """
            Open an existing Excel workbook.
            """
            self.app.Workbooks.Open(filename)
        
        def set_sheet(self, sheet):
            """
            Set the active worksheet.
            """
            self.sheet = sheet
        
        def get_range_values(self, excel_range):
            """
            Gets a range object for the specified range or single cell.
            The variable 'excel_range' should be specified as a string, e.g. 'D10:F22'
            """
            return self.app.ActiveWorkbook.Sheets(self.sheet).Range(excel_range)
          
        def get_cell_value(self, cell):
            """
            Get the value of 'cell'.
            The variable 'cell' should be specified as a string, e.g. 'A1'
            """
            value = self.get_range_values(cell).Value
            if isinstance(value, tuple):
                value = [v[0] for v in value]
            return value
        
        def get_range_values_as_dict(self, excel_range):
            """
            Get the values of a range as a dictionary compatible with OPUS
            storage objects.  Assumes that the top row of a range contains names
            suitable for use as column names and remaining rows are made up of integers
            or floats.
            """
            
            # Put range values in a list
            range_values = self.get_range_values(excel_range)
            range_list = []
            for i in range_values:
                range_list.append(i.value)
            
            # Get number of columns and list of column names
            column_names = []
            number_of_columns = 0
            for i in range_list:
                if isinstance(i, unicode):
                    number_of_columns += 1
                    column_names.append(str(i))
            
            # Get number of data rows
            number_data_rows = len(range_list)/number_of_columns - 1
            
            # Get rows as list of lists
            new_num_cols = 0
            lst = []
            for i in range(number_data_rows):
                new_num_cols = new_num_cols + number_of_columns
                temp_list = range_list[new_num_cols:new_num_cols + number_of_columns]
                lst.append(temp_list)
            
            # Create dictionary of columns to populate with values
            table = {}
            x = 0
            for i in range(0,number_of_columns):
                col_name = str(range_list[i])
                table[col_name] = empty(0, 'f')
                       
            # Populate dictionary with values
            for i in lst:
                index_counter = 0
                for j in i:
                    column_name = column_names[index_counter]
                    table[column_name] = append(table[column_name], j)
                    index_counter += 1

            return table
            
        def close(self):
            """
            Close the active workbook.
            """
            self.app.ActiveWorkbook.Close()
          
        def quit(self):
            """
            Quit Excel.
            """
            return self.app.Quit()
