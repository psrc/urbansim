# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

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
        building_group_id tinyint)')      #this variable needs to be defined in aliases.py
        #building_type_id tinyint)')
conn.commit()

us_path=r'C:\opus\data\sanfrancisco\baseyear_2009_scenario_baseline\2009'
storage = StorageFactory().get_storage('flt_storage',storage_location = us_path)

#read classification from local cache
bt = Dataset(in_storage = storage,in_table_name = 'building_types',id_name='building_type_id',dataset_name='building_type')
btclass= Dataset(in_storage = storage,in_table_name = 'building_type_classification',id_name='class_id',dataset_name='building_type_classification')
targetvacancies = Dataset(in_storage = storage,in_table_name = 'target_vacancies',id_name='target_vacancies_id',dataset_name='target_vacancies')

    
#===============================================================================
#    y=a*sin(bx+c)+d
# treat vacancy like a sine function. Constants (b, c) are crafted so there are 64 months between each peak
# last peak was late 2007.
# amp (a) denotes the amplitude of each cycle, while the base (d) signifies the center of the Function.
#http://www.nber.org/cycles.html
#===============================================================================

#Solving for c at maximum
# 10 = 10 * sin(phaseshift * peak + c)
#<=> 1=1*sin(phaseshift * peak + c)
#<=> asin(1)= phaseshift * peak + c
#<=> 1.57 = 1.125346622 * 2007 + c
#<=> c = -2258.125221

econcycle=67 #months
peak=2007

#for each cycle (2pi) x economic cycle years pass.
period=(2*math.pi)/(econcycle/12.) 

#use to shift the peak relative to the calendar year
phase=math.asin(1)-(period*peak)

rows = []
for unit_name in unique(btclass.get_attribute('grouping_id')): #needs to be defined in building_type_classification
    for yr in range(2001,2036):
        if unit_name ==3:   #office
            amp=2.5*.01
            base=.06
        elif unit_name ==2: #inst
            amp=3*.01
            base=.15
        elif unit_name ==1: #comm
            amp=3*.01
            base=.06
        elif unit_name ==4: #res
            amp=2*.01
            base=.04
            rows.append((base+amp*math.sin((period*yr-2258.125221)),float(yr),"residential_units","number_of_households",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("number_of_households","residential_units",base+amp*math.sin((period*yr-2258.125221)),unit_name,yr)
        elif unit_name ==5: #visit
            amp=10*.01
            base=.3        
        elif unit_name ==6: #mixed
            amp=5*.01
            base=.2           
            rows.append((base+amp*math.sin((period*yr-phase)),float(yr),"total_mixed_spaces","occupied_mixed_spaces",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("occupied_mixed_spaces","total_mixed_spaces",base+amp*math.sin((period*yr-phase)),unit_name,yr)

        if unit_name in(1,2,3,5): #nonres
            rows.append((base+amp*math.sin((period*yr-phase)),float(yr),"non_residential_sqft","occupied_sqft",float(unit_name)))
            print "%s\t%s\t%f\t%s\t%d" %("occupied_sqft","non_residential_sqft",base+amp*math.sin((period*yr-phase)),unit_name,yr)
            #pass
#print rows
#rows.append([.1,2004,'a','b',1])
#rows.append([.08,2006,'ta','db',0])

cursor.executemany('INSERT INTO target_vacancies VALUES (?,?,?,?,?)',rows) 
conn.commit()   
