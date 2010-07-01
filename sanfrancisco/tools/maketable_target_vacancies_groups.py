from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import where, zeros, unique
from urbansim.datasets.target_vacancy_dataset import TargetVacancyDataset
import random
import pyodbc
from adodbapi.adodbapi import Cursor
import math
from compiler.ast import Function
#set up target connection
conn=pyodbc.connect('DRIVER={MySQL ODBC 5.1 Driver};DATABASE=baseyear_2009_scenario_baseline;UID=urbansim;PWD=urbansim')
cursor = conn.cursor()

try:
    cursor.execute("drop table target_vacancies;")
except:
    pass

#create table on mysql server
cursor.execute('CREATE TABLE target_vacancies '
        '( \
        target_vacancy_rate float, \
        year int, \
        total_spaces varchar(50), \
        occupied_spaces varchar(50), \
        building_group_id tinyint)')
        #building_type_id tinyint)')
conn.commit()

us_path=r'C:\opus\data\sanfrancisco\baseyear_2009_scenario_baseline\2009'
storage = StorageFactory().get_storage('flt_storage',storage_location = us_path)

#read classification from local cache
bt = Dataset(in_storage = storage,in_table_name = 'building_types',id_name='building_type_id',dataset_name='building_type')
btclass= Dataset(in_storage = storage,in_table_name = 'building_type_classification',id_name='class_id',dataset_name='building_type_classification')
targetvacancies = Dataset(in_storage = storage,in_table_name = 'target_vacancies',id_name='target_vacancies_id',dataset_name='target_vacancies')

rows = []
for unit_name in unique(btclass.get_attribute('grouping_id')):
    
#===============================================================================
#    y=a*sin(bx+c)+d
# treat vacancy like a sine function. Constants (b, c) are crafted so there are 58 months between each peak
# last peak was late 2007.
# amp (a) denotes the amplitude of each cycle, while the base (d) signifies the center of the Function.
#===============================================================================
    
    for yr in range(2010,2036):
        if unit_name ==3:   #office
            amp=10*.01
            base=.20
        elif unit_name ==2: #inst
            amp=3*.01
            base=.2
        elif unit_name ==1: #comm
            amp=3*.01
            base=.06
        elif unit_name ==4: #res
            amp=4*.01
            base=.05
        elif unit_name ==5: #visit
            amp=10*.01
            base=.3        
        elif unit_name ==6: #mixed
            amp=5*.01
            base=.2        
       
        if  unit_name==4: #res
            rows.append((base+amp*math.sin((1.125346622*yr-2258.125221)),float(yr),"residential_units","number_of_households",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("number_of_households","residential_units",base+amp*math.sin((1.125346622*yr-2258.125221)),unit_name,yr)
            
            #pass
        elif unit_name ==6: #mixed
            rows.append((base+amp*math.sin((1.125346622*yr-2258.125221)),float(yr),"total_mixed_spaces","occupied_mixed_spaces",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("occupied_mixed_spaces","total_mixed_spaces",base+amp*math.sin((1.125346622*yr-2258.125221)),unit_name,yr)
            #pass
        elif unit_name in(1,2,3,5): #nonres
            rows.append((base+amp*math.sin((1.125346622*yr-2258.125221)),float(yr),"non_residential_sqft","occupied_sqft",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("occupied_sqft","non_residential_sqft",base+amp*math.sin((1.125346622*yr-2258.125221)),unit_name,yr)
            #pass
#print rows
#rows.append([.1,2004,'a','b',1])
#rows.append([.08,2006,'ta','db',0])

cursor.executemany('INSERT INTO target_vacancies VALUES (?,?,?,?,?)',rows) 
conn.commit()   