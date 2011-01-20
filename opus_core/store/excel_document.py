# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# TODO:expand this class into a full excel storage object
# This is not a full storage object, it only reads data from excel

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
        
        def get_range_values_as_list(self, excel_range):
            """
            Gets a range object for the specified range or single cell.
            Returns this range as a Python list.
            """
            range_values = self.get_range_values(excel_range)
            range_list = []
            for i in range_values:
                range_list.append(i.value)
            return range_list
          
        def get_cell_value(self, cell):
            """
            Get the value of 'cell'.
            The variable 'cell' should be specified as a string, e.g. 'A1'
            """
            value = self.get_range_values(cell).Value
            if isinstance(value, tuple):
                value = [v[0] for v in value]
            return value
        
        def get_dict_table_from_column_names_and_ranges(self, column_names_and_ranges):
            """
            Returs a dictionary with column names as keys and numpy arrays as values.
            list_of_column_names should be a python list containing the column names.
            list_of_ranges should be a python list containing strings of excel ranges.
            """
            #if len(list_of_column_names) != len(list_of_ranges):
            #    print 'The are a different number of column names and ranges'
            #    return
            
            dic = {}
            #for i in range(0,len(list_of_column_names)):
            #    dic[list_of_column_names[i]] = array(self.get_range_values_as_list(list_of_ranges[i]))
            
            
            for column_name, data_range in column_names_and_ranges.iteritems():
                dic[column_name] = array(self.get_range_values_as_list(data_range))
            return dic
        
        def close(self):
            """
            Close the active workbook without saving.
            """
            self.app.ActiveWorkbook.Close(SaveChanges=0)
          
        def quit(self):
            """
            Quit Excel.
            """
            self.app.Quit()
