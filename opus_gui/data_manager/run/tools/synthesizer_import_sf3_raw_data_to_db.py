# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.items():
        param_dict[str(key)] = str(val)
    
    # get parameter values
    raw_sf3_file_path = param_dict['raw_sf3_file_path']
    database_server_connection = param_dict['database_server_connection']
    database_name = param_dict['database_name']
    
    # set up database server configuration
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)   

    # Main application routine:

    opus_db.execute("""
            CREATE TABLE raw_sf3_data (
              GEO_ID text,
              P006001 int,P006002 int,P006003 int,P006004 int,
              P006005 int,P006006 int,P006007 int,P006008 int,
              P008001 int,P008002 int,P008003 int,P008004 int,
              P008005 int,P008006 int,P008007 int,P008008 int,
              P008009 int,P008010 int,P008011 int,P008012 int,
              P008013 int,P008014 int,P008015 int,P008016 int,
              P008017 int,P008018 int,P008019 int,P008020 int,
              P008021 int,P008022 int,P008023 int,P008024 int,
              P008025 int,P008026 int,P008027 int,P008028 int,
              P008029 int,P008030 int,P008031 int,P008032 int,
              P008033 int,P008034 int,P008035 int,P008036 int,
              P008037 int,P008038 int,P008039 int,P008040 int,
              P008041 int,P008042 int,P008043 int,P008044 int,
              P008045 int,P008046 int,P008047 int,P008048 int,
              P008049 int,P008050 int,P008051 int,P008052 int,
              P008053 int,P008054 int,P008055 int,P008056 int,
              P008057 int,P008058 int,P008059 int,P008060 int,
              P008061 int,P008062 int,P008063 int,P008064 int,
              P008065 int,P008066 int,P008067 int,P008068 int,
              P008069 int,P008070 int,P008071 int,P008072 int,
              P008073 int,P008074 int,P008075 int,P008076 int,
              P008077 int,P008078 int,P008079 int,P009001 int,
              P009002 int,P009003 int,P009004 int,P009005 int,
              P009006 int,P009007 int,P009008 int,P009009 int,
              P009010 int,P009011 int,P009012 int,P009013 int,
              P009014 int,P009015 int,P009016 int,P009017 int,
              P009018 int,P009019 int,P009020 int,P009021 int,
              P009022 int,P009023 int,P009024 int,P009025 int,
              P009026 int,P009027 int,P010001 int,P010002 int,
              P010003 int,P010004 int,P010005 int,P010006 int,
              P010007 int,P010008 int,P010009 int,P010010 int,
              P010011 int,P010012 int,P010013 int,P010014 int,
              P010015 int,P010016 int,P010017 int,P010018 int,
              P010019 int,P014001 int,P014002 int,P014003 int,
              P014004 int,P014005 int,P014006 int,P014007 int,
              P014008 int,P014009 int,P014010 int,P014011 int,
              P014012 int,P014013 int,P014014 int,P014015 int,
              P014016 int,P043001 int,P043002 int,P043003 int,
              P043004 int,P043005 int,P043006 int,P043007 int,
              P043008 int,P043009 int,P043010 int,P043011 int,
              P043012 int,P043013 int,P043014 int,P043015 int,
              P052001 int,P052002 int,P052003 int,P052004 int,
              P052005 int,P052006 int,P052007 int,P052008 int,
              P052009 int,P052010 int,P052011 int,P052012 int,
              P052013 int,P052014 int,P052015 int,P052016 int,
              P052017 int);              
            """)
    
    opus_db.execute("""
            LOAD DATA LOCAL INFILE '%s' INTO TABLE raw_sf3_data
            FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
            """ % (raw_sf3_file_path))
    
    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)
    
def opusHelp():
    help = 'This tool will import the raw Census SF3 data necessary\n' \
           'to create the marginals for the synthesizer algorithm.\n' \
           '\n' \
           'You will need to download the following tables for each county you wish to synthesize from the \n' \
           'factfinder download center at http://factfinder.census.gov/servlet/DownloadDatasetServlet?_lang=en \n' \
           '\n' \
           'P6, P8, P9, P10, P14, and P43\n' \
           'Once you have downloaded those detailed tables for each county, you will need to eliminate.\n' \
           'some fields from the file: GEO_ID2, SUMLEVEL, and GEO_NAME\n' \
           'You will also need to delete the first two lines of the file (no field names in the file) and \n' \
           'turn the file into a comma delimited file rather than pipe delimited.  The easiest way to do this \n' \
           'is to use a spreadsheet application like Microsoft Excel.  You may also need to concatenate \n' \
           'each county together into the csv file.\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - download SF3 data from factfinder.census.gov and follow the directions above\n' \
           '\n'
    return help    