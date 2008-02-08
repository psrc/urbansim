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

from win32com.client import Dispatch
import os

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
  
  def get_range(self, range):
    """
    Returns a range object for the specified range or single cell.
    """
    return self.app.ActiveWorkbook.Sheets(self.sheet).Range(range)
  
  def get_value(self, cell):
    """
    Get the value of 'cell'.
    """
    value = self.get_range(cell).Value
    if isinstance(value, tuple):
      value = [v[0] for v in value]
    return value
  
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
