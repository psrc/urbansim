#from win32com.client import Dispatch
#import win32com.client, sys

#Arc = win32com.client.Dispatch('esriArcmap.ArcMapEx')

#os.system('start R:/Projects/PSRC/Estimation/Results/Arcmap/taz_map/units_added_taz.mxd')

##################################################
import os

os.startfile('C:/Program Files/ArcGIS/Bin/arcmap.exe')
#################################################
## Open calculator program ##

#import os
#os.system('start calc.exe')
#################################################
## Open MS Word ##
#import win32com.client

#w=win32com.client.Dispatch("Word.Application")
#w.Visible=1
#w.Documents.Add()

##################################################
## Open MS Excel and key in values in two cells ##
# this example starts Excel, creates a new workbook, 
# puts some text in the first and second cell
# closes the workbook without saving the changes
# and closes Excel.  This happens really fast, so
# you may want to comment out some lines and add them
# back in one at a time ... or do the commands interactively

#from win32com.client import Dispatch

#xlApp = Dispatch("Excel.Application")
#xlApp.Visible = 1
#xlApp.Workbooks.Add()
#xlApp.ActiveSheet.Cells(1,1).Value = 'Python Rules!'
#xlApp.ActiveWorkbook.ActiveSheet.Cells(1,2).Value = 'Python Rules 2!'
#xlApp.ActiveWorkbook.Close(SaveChanges=0)
#xlApp.Quit()
#del xlApp