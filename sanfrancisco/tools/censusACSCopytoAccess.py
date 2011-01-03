#===============================================================================
# Script packages American Community Survey release and dumps into database and 
# creates ARCGIS layer files for each sequence (1 thru 114). Needs the following
# files from the Census web site to run: 
# http://www2.census.gov/acs2009_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls
# http://www2.census.gov/acs2009_5yr/summaryfile/2005-2009_ACSSF_By_State_All_Tables/California_Tracts_Block_Groups_Only.zip
# http://www2.census.gov/acs2009_5yr/summaryfile/UserTools/2005-2009_SummaryFileXLS.zip
#
# The ACS contains of 114 sequences, where each sequence is a collection of thema-
# tically related data at a given geographic level of detail (tracts, block 
# groups, etc). Each sequence may in turn contain any number of columns from 1
# to 255. There is an excel file for each sequence containing column headers, as
# well as a data (.txt) file. The script parses through the excel file direc-
# tory, opens each sequence, stores column headers, and opens the relevant data
# file. It then connects to a database through pyODBC, creates a data definition
# statement to create the target table, and subsequently inserts the data from
# the text file to the newly created table. Lastly, the script creates ArcGIS 
# layer files using the ArcGIS 9.3 geoprocessor object.
#===============================================================================

import csv
import arcgisscripting
import sys
import string
import re
import win32com.client as win32
#xlApp = win32.Dispatch("Excel.Application")
#xlApp.Visible = True
import xlrd
import os
import time
import pyodbc


def readExcelFiles(geographyType="tract",valueType="estimate"):
       
    #Looks up a geographic correspondence between STFID and LOGRECNO to be able to link to tract shapefile
    geoFileName=r'I:\Citywide\Core Data\Census\American Community Survey\ACS_5_Year_2005_2009\%s.csv' %(geographyType)
    geoReader = csv.reader(open(geoFileName,'rb'))
    geoDict={}
    for row in geoReader:
        geoDict[row[1]]=row[0]
    #data file contains records for all of California--constrain what is kept to San Francisco.
    if geographyType=='tract':
        sfLogrecnoLo=18790      #this is selected to be the first tract
        sfLogrecnoHi=18966      #this is selected to be the last tract +1
    else:
        sfLogrecnoLo=37423      #this is selected to be the first blkgrp
        sfLogrecnoHi=37998      #this is selected to be the last blkgrp +1
        
    #folder for excel sequence tables (seq1.xls etc)
    fPathTemplate=r'I:\Citywide\Core Data\Census\American Community Survey\ACS_5_Year_2005_2009\2005-2009_SummaryFileXLS'
    
    #folder for extracted data files
    fPathData=r'I:\Citywide\Core Data\Census\American Community Survey\ACS_5_Year_2005_2009\data'
    
    timestring=str(time.strftime("%Y%m%d_%H%M", time.localtime()))
    logfile=open(os.path.join(fPathData,timestring+"_logfile.txt"),"w")
    
    #location for target (in this case MS Access--must be created in advance) database
    dataBasePath=r'I:\Citywide\Core Data\Census\American Community Survey\ACS_5_Year_2005_2009\ACS2005-2009.mdb'
    connString="DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" %(dataBasePath)
    conn = pyodbc.connect(connString)
    cursor = conn.cursor()
    for root, dirs, files in os.walk(fPathTemplate):
        for name in files:
            #create geoprocessor object
            gp = arcgisscripting.create()
            gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
            
            #get data file
            fSeq=name[3:len(name)-4] #get sequence from excel name template
            dataFileName="%s20095ca%s000.txt" %(valueType,fSeq.rjust(4,'0'))
            dataFile=open(os.path.join(root,fPathData,dataFileName))
            dataFileSize=os.path.getsize(os.path.join(fPathData,dataFileName))
            column_count=len(dataFile.readline().split(','))
            
            #get excel file and column headers
            xlFilename = os.path.join(root, name)
            xlSize=os.path.getsize(xlFilename)
            xlWb = xlrd.open_workbook(xlFilename)
            column_names=xlWb.sheet_by_index(0).row_values(0)

            #create data container for appending
            data_append = []
            
            #1. only look at text files with data in them
            if dataFileSize>0:
                for line in dataFile:
                    # only include San Francisco geographies from data file 
                    if long(line[25:32]) in range(sfLogrecnoLo,sfLogrecnoHi):
                        # remove periods if they represent numbers (NOT decimal points)
                        #patt = re.compile(r'(?<![0-9])[.](?![0-9])')
                        #dataPeriodRemovedA=re.sub(patt,None,line)
                        out=[]
                        
                        # remove last line break and split into list and replace .'s and 0-length strings 
                        data = line.replace("\n","").split(",")
                        for item in data:
                            if item.strip() in ["","."]:
                                out.append(None)
                            else:
                                out.append(item)
                        
                        # insert tract ID from dictionary using LOGRECNO at index 5
                        out.insert(0,geoDict[data[5]])
                        # convert each line to a tuple and append to global list for INSERT statement
                        datarow =  tuple(item for item in out)
                        data_append.append(datarow)

                #go to access and make a list of field names followed by "double" 
                if len(data_append)>0:
                    col_list=[o+" double," for o in column_names]
                
                    #convert list to string and exclude last comma
                    column_string=''.join(col_list)         
                    column_string_fix=column_string[92:len(column_string)-1]
                    table_name="%s_%s_seq%s" %(valueType,geographyType,fSeq.rjust(4,'0'))
                
                    #create the tabledef statement with the fields defined by column_string_fix
                    tabledef=('CREATE TABLE %s (STFID varchar(12),FILEID varchar(5),FILETYPE varchar(9),STUSAB varchar(2)\
                    ,CHARITER varchar(1),SEQUENCE varchar(1),LOGRECNO varchar(7) PRIMARY KEY, %s)') %(table_name,column_string_fix)
                    logline="%s\t%d" %(table_name,column_count)
                    logfile.write(logline)
                    logfile.flush()
                    print logline
                    cursor.execute(tabledef)
                    conn.commit()
                    
                    # prepare "?"-paramater placeholder string for INSERT statement
                    q_marks="(%s" %("?,"*(column_count+1))
                    q_marksformat=q_marks[0:len(q_marks)-1]+")"
                    update_str="INSERT INTO %s VALUES %s" %(table_name,q_marksformat)
                    
                    #define GIS output layer file
                    sourceGeo = "I:\\GIS\\Citywide\\base_maps\\san_francisco\\%s.shp" %geographyType
                    dataToJoin = "%s\\%s" %(dataBasePath,table_name)
                    outLayer = "%s2000_Layer" %geographyType
                    GeoFeatureLayerToJoin =  "%s2000_Layer" %geographyType
                    FinalOut = r"I:\Citywide\Core Data\Census\American Community Survey\ACS_5_Year_2005_2009\layers\%s.lyr" %table_name 
                    
                    # Process: Make Feature Layer; add join and save
                    gp.MakeFeatureLayer_management(sourceGeo, GeoFeatureLayerToJoin, "", "", "OBJECTID OBJECTID VISIBLE NONE;ID ID VISIBLE NONE;FIPSSTCO FIPSSTCO VISIBLE NONE;TRT2000 TRT2000 VISIBLE NONE;STFID STFID VISIBLE NONE;TRACT_ID TRACT_ID VISIBLE NONE;PLANNING_D PLANNING_D VISIBLE NONE;TractID TractID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;X X VISIBLE NONE;Y Y VISIBLE NONE;PlanningDi PlanningDi VISIBLE NONE")
                    gp.AddJoin_management(GeoFeatureLayerToJoin, "STFID", dataToJoin, "STFID", "KEEP_ALL")
                    gp.SaveToLayerFile_management(outLayer, FinalOut)
                    gp=None
                try:
                    cursor.executemany(update_str,data_append)
                    conn.commit()
                    logfile.write("\tsuccessfully created table %s\n" %(table_name))
                except:
                    logfile.write("\terror encountered in %s\n" %(table_name))
                    dumpName="%s_%sDump" %(timestring,table_name)
                    logfileDump=open(os.path.join(fPathData,dumpName),"w")
                    logfileDump.write("\terror encountered in %s\n" %(data_append))
                    logfileDump.close()
            
    logfile.close()
    dataFile.close()
    conn.close()
    
if __name__ == '__main__':
    #run all four in turn (for tracts and block groups, both margin of error and value estimate tables
    readExcelFiles("tract","e")
    readExcelFiles("blkgrp","e")
    readExcelFiles("tract","m")
    readExcelFiles("blkgrp","m")