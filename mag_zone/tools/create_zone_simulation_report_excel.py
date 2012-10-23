# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from sqlalchemy import create_engine, exc
from datetime import datetime
from easygui import multenterbox, multchoicebox, choicebox
from numpy import array, median, seterr
from time import time
import xlwt, os, sys

class RegionWideReport():
    
    def __init__(self, workbook, years, connection, run_name, base_year, column_counter=0):
        self.column_counter = column_counter
        self.worksheet = workbook.add_sheet('region_wide_report')
        self.years = years
        self.connection = connection
        self.run_name = run_name
        self.base_year = base_year

        self._print_years_to_workbook()
        
    def _print_years_to_workbook(self):
        self.worksheet.write(0,self.column_counter,'year')
        row_counter = 1
        for year in self.years:
            self.worksheet.write(row_counter,self.column_counter,year)
            row_counter += 1
        self.column_counter += 1

    def get_percent_DUs_built(self):
        # get percent of DU capacity built
        self.worksheet.write(0,self.column_counter,'pct_DUs_built')
        row_counter = 1
        for year in self.years:
            print 'Computing percent of DUs built for year %s' % year
            r = self.connection.execute('select SUM(residential_units)/SUM(residential_units_capacity) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_percent_nonres_sqft_built(self):
        # get percent of nonres sqft capacity built
        self.worksheet.write(0,self.column_counter,'pct_nonres_sqft_built')
        row_counter = 1
        for year in self.years:
            print 'Computing percent of nonres sqft built for year %s' % year
            r = self.connection.execute('select SUM(non_residential_sqft)/SUM(non_residential_sqft_capacity) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_DUs_in_active_developments_by_year(self):
        # get total DUs in active developments by year
        self.worksheet.write(0,self.column_counter,'total_ADM_DUs')
        row_counter = 1
        for year in self.years:
            print 'Computing total DUs in Active Developments for year %s' % year
            r = self.connection.execute('select sum(current_built_units) from %s_%s_activeDevelopments where building_type_id in (1,2)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_nonres_sqft_in_active_developments_by_year(self):
        # Get total non-residential sqft in active developments by year
        self.worksheet.write(0,self.column_counter,'total_ADM_nonres_sqft')
        row_counter = 1
        for year in self.years:
            print 'Computing total non-residential sqft in Active Developments for year %s' % year
            r = self.connection.execute('select sum(cast(current_built_units as float)) from %s_%s_activeDevelopments where building_type_id not in (1,2)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_mean_age_of_population_by_year(self):
        # get the average age of the population by year
        self.worksheet.write(0,self.column_counter,'mean_pop_age')
        row_counter = 1
        for year in self.years:
            print 'Computing mean age of population for year %s' % year
            r = self.connection.execute('select ROUND(AVG(CAST(age AS float)),1) from %s_%s_persons' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_median_age_of_population_by_year(self):
        # get the median age of the population by year
        self.worksheet.write(0,self.column_counter,'median_pop_age')
        row_counter = 1
        for year in self.years:
            print 'Computing median age of population for year %s' % year
            r = self.connection.execute('SELECT age from %s_%s_persons' % (self.run_name, year))
            age_list = r.fetchall()
            age_array = array(age_list)
            median_age = round(median(age_array),2)
            self.worksheet.write(row_counter, self.column_counter, median_age)
            row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_population_age_distribution_by_year(self):
        # get population in age brackets <5, 5-9, 10-15, 16-18, 19-24, 25-34, 35-44, 45-54, 55-64, 65+
        self.worksheet.write(0,self.column_counter, 'pop_age_under_5')
        row_counter = 1
        for year in self.years:
            print 'Computing total population under age 5 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 5-9 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 10-14 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_15_17')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 15-17 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 18 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_18_19')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 18-19 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 17 and age < 20 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 20-24 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 25-29 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 30-34 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 35-39 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 40-44 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 45-49 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 50-54 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 55-59 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_60_61')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 60-61 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 62 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_62_64')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 62-64 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 61 and age < 65 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 65-69 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 70-74 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 75-79 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 80-84 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_over_84')
        row_counter = 1
        for year in self.years:
            print 'Computing total population ages 85+ for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_male_population_distribution_by_age_and_year(self):
        # get male population in age brackets <5, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54,
        # 55-59, 60-64, 65-69, 70-74, 75-79, 80-84, 85-89, 90-94, 95-99, 100+
        self.worksheet.write(0,self.column_counter, 'm_pop_age_under_5')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population under age 5 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 5-9 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 10-14 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_15_19')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 15-19 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 20 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 20-24 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 25-29 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 30-34 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 35-39 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 40-44 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 45-49 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 50-54 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 55-59 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_60_64')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 60-64 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 65 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 65-69 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 70-74 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 75-79 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 80-84 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_85_89')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 85-89 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and age < 90 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_90_94')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 90-94 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 89 and age < 95 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_95_99')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 95-99 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 94 and age < 100 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_100up')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population ages 100+ for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 99 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1        

    def get_total_female_population_distribution_by_age_and_year(self):
        # get female population in age brackets <5, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54,
        # 55-59, 60-64, 65-69, 70-74, 75-79, 80-84, 85-89, 90-94, 95-99, 100+
        self.worksheet.write(0,self.column_counter, 'f_pop_age_under_5')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population under age 5 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 5-9 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 10-14 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_15_19')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 15-19 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 20 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 20-24 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 25-29 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 30-34 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 35-39 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 40-44 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 45-49 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 50-54 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 55-59 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_60_64')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 60-64 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 65 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 65-69 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 70-74 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 75-79 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 80-84 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_85_89')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 85-89 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and age < 90 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_90_94')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 90-94 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 89 and age < 95 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_95_99')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 95-99 for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 94 and age < 100 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_100up')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population ages 100+ for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 99 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_by_number_of_children(self):
        # Get the number of households by the number of children in the household
        # categories: 0,1,2,3,4,5,6,7+
        for year in self.years:
            print 'Computing temporary tables for households by number of children for year %s' % year
            query = '''
                    select household_id
                    into #distinct_hhlds%s
                    from %s_%s_households
                    ''' % (year,self.run_name,year)
            r = self.connection.execute(query)
            r.close()
            query = '''
                    select
                        household_id,
                        count(*) num_children
                    into #hh_num_children%s
                    from %s_%s_persons
                    where age < 18
                    group by household_id
                    ''' % (year,self.run_name,year)
            r = self.connection.execute(query)
            r.close()
            query = '''
                    select
                        h.household_id,
                        case
                            when c.num_children is null then 0
                            when c.num_children >=7 then 7
                            else c.num_children
                        end num_children
                    into #hh_with_num_children%s
                    from #distinct_hhlds%s h
                    left join #hh_num_children%s c
                    on c.household_id = h.household_id
                    ''' % (year,year,year)
            r = self.connection.execute(query)
            r.close()
        self.worksheet.write(0,self.column_counter,'hh_0_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 0 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 0' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_1_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 1 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 1' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_2_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 2 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 2' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_3_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 3 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 3' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_4_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 4 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 4' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_5_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 5 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 5' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_6_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 6 children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 6' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_7up_children')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 7+ children for year %s' % year
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 7' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_by_household_size(self):
        # Get the number of households by the household size
        # categories: 1,2,3,4,5,6,7+
        for year in self.years:
            print 'Computing temporary tables for households by household size for year %s' % year
            query = '''
                    select
                        household_id,
                        count(*) num_ppl
                    into #hh_num_ppl%s
                    from %s_%s_persons
                    group by household_id
                    ''' % (year,self.run_name,year)
            r = self.connection.execute(query)
            r.close()
        self.worksheet.write(0,self.column_counter,'hh_size_1')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 1 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 1' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_2')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 2 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 2' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_3')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 3 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 3' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_4')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 4 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 4' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_5')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 5 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 5' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_6')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 6 for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 6' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_7up')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with household size 7+ for year %s' % year
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 7' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_by_number_of_vehicles(self):
        # Get total households by number of workers
        self.worksheet.write(0,self.column_counter,'hh_0_vehicles')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 0 vehicles for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles < 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_1_vehicle')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 1 vehicle for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_2_vehicles')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 2 vehicles for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_3_vehicles')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 3 vehicles for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 3' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_4up_vehicles')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 4+ vehicles for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles > 3' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1

    def get_total_households_by_number_of_workers(self):
        # Get total households by number of workers
        self.worksheet.write(0,self.column_counter,'hh_0_workers')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 0 workers for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers < 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_1_worker')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 1 worker for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_2_workers')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 2 workers for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_3_workers')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 3 workers for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 3' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_4up_workers')
        row_counter = 1
        for year in self.years:
            print 'Computing total households with 4+ workers for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers > 3' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1

    def get_total_workers_in_households(self):
        # Get total workers in households
        self.worksheet.write(0,self.column_counter,'workers_in_hh')
        row_counter = 1
        for year in self.years:
            print 'Computing total workers in households for year %s' % year
            r = self.connection.execute('select sum(workers) from %s_%s_households' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1

    def get_total_population_by_sex_and_year(self):
        # Get total population by sex and year
        self.worksheet.write(0,self.column_counter,'total_male_pop')
        row_counter = 1
        for year in self.years:
            print 'Computing total male population for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where sex = 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'total_female_pop')
        row_counter = 1
        for year in self.years:
            print 'Computing total female population for year %s' % year
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where sex = 2 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
    
    def get_total_DUs_by_year(self):
        # Get total residential units by year
        self.worksheet.write(0,self.column_counter,'total_DUs')
        row_counter = 1
        for year in self.years:
            print 'Computing total residential DUs for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_nonres_sqft_by_year(self):
        # Get total non-residential sqft by year
        self.worksheet.write(0,self.column_counter,'total_nonres_sqft')
        row_counter = 1
        for year in self.years:
            print 'Computing total non-residential sqft for year %s' % year
            r = self.connection.execute('select sum(cast(non_residential_sqft as float)) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_nonres_sqft_by_type_and_year(self):
        # Get total nonres sqft by type and year
        query = 'select building_type_id, building_type_name from %s_%s_buildingTypes where is_residential = 0' % (self.run_name, self.years[0])
        r = self.connection.execute(query)
        nonres_types = []
        nonres_names = []
        for row in r:
            nonres_types.append(row[0])
            nonres_names.append(row[1])
        r.close()
        # Get totals
        column_counter = self.column_counter
        for building_type in nonres_types:
            row_counter = 1
            self.worksheet.write(0,column_counter,'nonres_sqft_type_%s' % building_type)
            for year in self.years:
                print 'Computing non-residential sqft for year %s and building type %s' % (year, building_type)
                query = 'select SUM(CAST(non_residential_sqft AS FLOAT)) from %s_%s_buildings where building_type_id = %s' % (self.run_name, year, building_type)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(nonres_types)

    def get_total_DUs_SF_by_year(self):
        # Get total single family residential units by year
        self.worksheet.write(0,self.column_counter,'total_SF_DUs')
        row_counter = 1
        for year in self.years:
            print 'Computing total SF residential DUs for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings where building_type_id = 1' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_DUs_MF_by_year(self):
        # Get total multi family residential units by year
        self.worksheet.write(0,self.column_counter,'total_MF_DUs')
        row_counter = 1
        for year in self.years:
            print 'Computing total MF residential DUs for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings where building_type_id = 2' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_hh')
        row_counter = 1
        for year in self.years:
            print 'Computing total households for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_mean_household_income_by_year(self):
        self.worksheet.write(0,self.column_counter,'mean_hh_income')
        row_counter = 1
        for year in self.years:
            print 'Computing mean household income for year %s' % year
            r = self.connection.execute('SELECT ROUND(AVG(CAST(income as FLOAT)),2) from %s_%s_households' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_mean_persons_per_household_by_year(self):
        self.worksheet.write(0,self.column_counter,'mean_pp_per_hh')
        row_counter = 1
        for year in self.years:
            print 'Computing mean persons per household for year %s' % year
            r = self.connection.execute('select household_id, count(*) num_pphh into #pp_hh%s from %s_%s_persons group by household_id' % (year, self.run_name, year))
            r = self.connection.execute('SELECT ROUND(AVG(CAST(num_pphh as FLOAT)),2) from #pp_hh%s' % (year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_median_household_income_by_year(self):
        self.worksheet.write(0,self.column_counter,'median_hh_income')
        row_counter = 1
        for year in self.years:
            print 'Computing median household income for year %s' % year
            r = self.connection.execute('SELECT income from %s_%s_households' % (self.run_name, year))
            income_list = r.fetchall()
            income_array = array(income_list)
            median_income = round(median(income_array),2)
            self.worksheet.write(row_counter, self.column_counter, median_income)
            row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_in_SFR_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_hh_SFR')
        row_counter = 1
        for year in self.years:
            print 'Computing total households in SFR for year %s' % year
            query = '''
                    select
                        count(*)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 1
                    ''' % (self.run_name, year, self.run_name, year)
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_in_MFR_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_hh_MFR')
        row_counter = 1
        for year in self.years:
            print 'Computing total households in MFR for year %s' % year
            query = '''
                    select
                        count(*)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 2
                    ''' % (self.run_name, year, self.run_name, year)
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_population_in_SFR_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_pop_SFR')
        row_counter = 1
        for year in self.years:
            print 'Computing total population in SFR for year %s' % year
            query = '''
                    select
                        sum(persons)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 1
                    ''' % (self.run_name, year, self.run_name, year)
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_population_in_MFR_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_pop_MFR')
        row_counter = 1
        for year in self.years:
            print 'Computing total population in MFR for year %s' % year
            query = '''
                    select
                        sum(persons)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 2
                    ''' % (self.run_name, year, self.run_name, year)
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_population_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_pop')
        row_counter = 1
        for year in self.years:
            print 'Computing total population for year %s' % year
            try:
                r = self.connection.execute('select sum(persons) from %s_%s_households where is_seasonal = 0' % (self.run_name, year))
            except:
                r = self.connection.execute('select count(*) from %s_%s_persons where is_seasonal = 0' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_jobs_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_jobs')
        row_counter = 1
        for year in self.years:
            print 'Computing total jobs for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_jobs' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_households_by_year_and_income_category(self):
        # Get household totals by household income category
        # households under 50k
        self.worksheet.write(0,self.column_counter,'total_hh_income_0')
        row_counter = 1
        for year in self.years:
            print 'Computing households <50k income for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where income < 50001' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        # households between 50k and 100k
        self.worksheet.write(0,self.column_counter + 1,'total_hh_income_1')
        row_counter = 1
        for year in self.years:
            print 'Computing households >50k income <100k for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where income > 50000 and income <100001' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 1,row[0])
                row_counter += 1
            r.close()
        # households over 100k
        self.worksheet.write(0,self.column_counter + 2,'total_hh_income_2')
        row_counter = 1
        for year in self.years:
            print 'Computing households >100k income for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where income > 100000' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 2,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 3

    def get_houehold_control_totals_by_year(self):
        self.worksheet.write(0,self.column_counter,'household_ct')
        row_counter = 1
        print 'Computing household control totals'
        r = self.connection.execute('select year, sum(total_number_of_households) from %s_%s_annualHouseholdControlTotals group by year order by year' % (self.run_name, self.base_year))
        for row in r:
            if row[0] == (self.base_year + 1):
                self.worksheet.write(row_counter,self.column_counter,0)
                row_counter += 1
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
            else:
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
        r.close()
        self.column_counter += 1

    def get_job_control_totals_by_year(self):
        self.worksheet.write(0,self.column_counter,'job_ct')
        row_counter = 1
        print 'Computing job control totals'
        r = self.connection.execute('select year, sum(total_number_of_jobs) from %s_%s_annualEmploymentControlTotals group by year order by year' % (self.run_name, self.base_year))
        for row in r:
            if row[0] == (self.base_year + 1):
                self.worksheet.write(row_counter,self.column_counter,0)
                row_counter += 1
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
            else:
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
        r.close()
        self.column_counter += 1

    def get_total_unplaced_development_projects_by_year(self):
        # Get unplaced development projects by year
        self.worksheet.write(0,self.column_counter,'unplaced_projects')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced development projects for year %s' % year
            if year == self.base_year:
                # there is no developmentProjects dataset for the base year
                self.worksheet.write(row_counter,self.column_counter,0)
                row_counter += 1
            else:
                r = self.connection.execute('select count(*) from %s_%s_developmentProjects where building_id < 1' % (self.run_name,year))
                for row in r:
                    self.worksheet.write(row_counter,self.column_counter,row[0])
                    row_counter += 1
                r.close()
        self.column_counter += 1

    def get_total_unplaced_households_by_year(self):
        # Get unplaced household totals by year
        self.worksheet.write(0,self.column_counter,'unplaced_hh')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced households for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_unplaced_households_by_income_categories(self):
        # Get unplaced household totals by household income category
        # unplaced households under 50k
        self.worksheet.write(0,self.column_counter,'unpl_hh_0_50k')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced households <50k income for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income < 50001)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        # unplaced households between 50k and 100k
        self.worksheet.write(0,self.column_counter + 1,'unpl_hh_50_100k')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced households >50k income <100k for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income > 50000 and income <100001)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 1,row[0])
                row_counter += 1
            r.close()
        # unplaced households over 100k
        self.worksheet.write(0,self.column_counter + 2,'unpl_hh_100k_up')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced households >100k income for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income > 100000)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 2,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 3

    def get_total_unplaced_jobs_by_year(self):
        # Get unplaced job totals by year
        self.worksheet.write(0,self.column_counter,'unplaced_jobs')
        row_counter = 1
        for year in self.years:
            print 'Computing unplaced jobs for year %s' % year
            r = self.connection.execute('select count(*) from %s_%s_jobs where building_id < 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_unplaced_jobs_by_sector_and_year(self):
        # Get unplaced job totals by sector and year
        # Get sectors
        r = self.connection.execute('select sector_id from %s_%s_employmentSectors order by sector_id' % (self.run_name, self.base_year))
        sectors = []
        for row in r:
            sectors.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter # was 14
        for sector in sectors:
            row_counter = 1
            self.worksheet.write(0,column_counter,'unpl_job_sec%s' % sector)
            for year in self.years:
                print 'Computing unplaced jobs for year %s and sector %s' % (year, sector)
                query = 'select count(*) from %s_%s_jobs where building_id < 1 and sector_id = %s' % (self.run_name, year, sector)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(sectors)

    def get_total_jobs_by_sector_and_year(self):
        # Get job totals by sector and year
        # Get sectors
        r = self.connection.execute('select sector_id from %s_%s_employmentSectors order by sector_id' % (self.run_name, self.base_year))
        sectors = []
        for row in r:
            sectors.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter # was 14
        for sector in sectors:
            row_counter = 1
            self.worksheet.write(0,column_counter,'job_sec%s' % sector)
            for year in self.years:
                print 'Computing jobs for year %s and sector %s' % (year, sector)
                query = 'select count(*) from %s_%s_jobs where sector_id = %s' % (self.run_name, year, sector)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(sectors)

    def get_total_population_by_race_and_year(self):
        # Get total population by race and year
        # Get races
        r = self.connection.execute('select distinct(race) from %s_%s_persons order by race' % (self.run_name, self.base_year))
        races = []
        for row in r:
            races.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter
        for race in races:
            row_counter = 1
            self.worksheet.write(0,column_counter,'pop_race%s' % race)
            for year in self.years:
                print 'Computing total population for year %s and race %s' % (year, race)
                query = 'select count(*) from %s_%s_persons where race = %s' % (self.run_name, year, race)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(races)

    def get_mean_persons_per_household_by_race_of_hh_head_and_year(self):
        # Get mean persons per by race and year
        # Get races
        r = self.connection.execute('select distinct(race) from %s_%s_persons order by race' % (self.run_name, self.base_year))
        races = []
        for row in r:
            races.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter
        temp_tables_years = []
        for race in races:
            row_counter = 1
            self.worksheet.write(0,column_counter,'pphh_race%s' % race)
            for year in self.years:
                print 'Computing mean persons per household for year %s and race %s' % (year, race)
                if year not in temp_tables_years:
                    r = self.connection.execute('select household_id, count(*) as num_pp_in_hh into tmp_p_hh%s from %s_%s_persons group by household_id' % (year, self.run_name, year))
                    r.close()
                    r = self.connection.execute('select household_id, race into tmp_head_race%s from %s_%s_persons where head_of_hh = 1' % (year, self.run_name, year))
                    r.close()
                    r = self.connection.execute('select p.*, h.race into tmp_pp_hh_race%s from tmp_p_hh%s p join tmp_head_race%s h on p.household_id = h.household_id' % (year, year, year))
                    r.close()
                    temp_tables_years.append(year)
                query = 'select ROUND(AVG(CAST(num_pp_in_hh AS FLOAT)),2) from tmp_pp_hh_race%s where race = %s' % (year, race)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(races)

    def get_mean_age_by_race_and_year(self):
        # Get mean age by race and year
        # Get races
        r = self.connection.execute('select distinct(race) from %s_%s_persons order by race' % (self.run_name, self.base_year))
        races = []
        for row in r:
            races.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter
        for race in races:
            row_counter = 1
            self.worksheet.write(0,column_counter,'mean_age_race%s' % race)
            for year in self.years:
                print 'Computing mean age for year %s and race %s' % (year, race)
                query = 'select ROUND(AVG(CAST(age as FLOAT)),1) from %s_%s_persons where race = %s' % (self.run_name, year, race)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(races)

    def get_total_job_spaces_by_year(self):
        # Get total job spaces by year
        self.worksheet.write(0,self.column_counter,'total_job_spaces')
        row_counter = 1           
        for year in self.years:
            print 'Computing total job spaces for year %s' % year
            # delete previous temp table
            r = self.connection.execute("IF OBJECT_ID('tempdb..#temp_bldgs_non_res_sqft','local') IS NOT NULL DROP TABLE #temp_bldgs_non_res_sqft")
            r.close()
            query = '''
                        select
                            b1.non_residential_sqft,
                            b1.zone_id,
                            b1.building_type_id
                        into
                            #temp_bldgs_non_res_sqft
                        from
                            %s_%s_buildings b1          
                    ''' % (self.run_name, year)
            r = self.connection.execute(query)
            r.close()
            query = '''
                        select
                            sum(b1.non_residential_sqft/b2.building_sqft_per_job) job_spaces
                        from
                            #temp_bldgs_non_res_sqft b1
                        left join
                            %s_%s_buildingSqftPerJob b2
                        on
                            b1.building_type_id = b2.building_type_id and b1.zone_id = b2.zone_id            
                    ''' % (self.run_name, year)
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

def get_total_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total jobs by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numjobs
                    into #numjobs_%s
                    from %s_%s_jobs h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numjobs IS NULL THEN 0
                                    ELSE u.numjobs
                            END
                        from #distinct_%s r
                        left join #numjobs_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_households_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total households by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('hh_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total households by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numhh
                    into #numhh_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numhh IS NULL THEN 0
                                    ELSE u.numhh
                            END
                        from #distinct_%s r
                        left join #numhh_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_households_by_income_quintile_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    for quintile in range(1,6):
        # Get total households by income quintiles by subarea in a separate sheet
        # write column headings (years)
        worksheet = workbook.add_sheet('hh_inc_quint_%s_by_%s' % (quintile, subarea))
        worksheet.write(0,0,'%s_id' % (subarea))
        
        # TODO: if subarea is mpa, write mpa_name
    #    if subarea == 'mpa':
    #        blah blah blah
        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'y'+str(year)+'q'+str(quintile))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        
        # TODO: if subarea is mpa, write mpa_name
    #    if subarea == 'mpa':
    #        blah blah blah
        
        # get values and fill in table
        column_counter = 1
        for year in years:
            print 'Computing total households for income quintile %s by %s for year %s' % (quintile, subarea, year)
            row_counter = 1
            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
            r.close()
            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
            r.close()
            query = '''select z.%s_id, count(*) as numhh
                        into #numhh_%s_%s
                        from %s_%s_households h
                        left join %s_%s_buildings b
                        on b.building_id = h.building_id
                        left join %s_%s_zones z
                        on b.zone_id = z.zone_id
                        where h.income_quintiles = %s
                        group by z.%s_id
                        order by z.%s_id''' % (subarea, year, quintile, run_name, year, run_name, year, run_name, year, quintile, subarea, subarea)
            r = connection.execute(query)
            r.close()
            r = connection.execute('''select
                                CASE 
                                        WHEN u.numhh IS NULL THEN 0
                                        ELSE u.numhh
                                END
                            from #distinct_%s r
                            left join #numhh_%s_%s u
                            on r.%s_id = u.%s_id
                            order by r.%s_id''' % (subarea, year, quintile, subarea, subarea, subarea))
            for row in r:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            r.close()

def get_persons_per_household_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get persons per household by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('pphh_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing persons per household by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select
                        p.household_id,
                        count(*) num_people,
                        z.%s_id
                    into #hh_num_people_%s
                    from %s_%s_persons p
                    left join %s_%s_households h
                    on p.household_id = h.household_id
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by p.household_id, z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, run_name, year, subarea)
        r = connection.execute(query)
        r.close()
        query = '''select
                    %s_id,
                    round(avg(cast(num_people as float)),3) pphh
                    into #pphh_%s%s
                    from #hh_num_people_%s
                    group by %s_id
                    order by %s_id
                ''' % (subarea, subarea, year, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    when h.pphh IS null then 0
                                    else h.pphh
                            END
                        from #distinct_%s u
                        left join #pphh_%s%s h
                        on h.%s_id = u.%s_id
                        order by u.%s_id''' % (subarea, subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()
        
def get_mean_household_income_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get mean household income by subarea in a separate sheet
    # write column headings
    function_begin = time()
    worksheet = workbook.add_sheet('mean_hh_income_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        t0 = time()
        print '\nComputing mean household income by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, round(AVG(cast(income as float)),2) as avghhinc
                    into #avghhinc_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.avghhinc IS NULL THEN 0
                                    ELSE u.avghhinc
                            END
                        from #distinct_%s r
                        left join #avghhinc_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        t1 = time() - t0
        print 'Query took %s seconds' % t1
        t0 = time()
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        t1 = time() - t0
        print 'Writing to Excel took %s seconds' % t1
        r.close()
    function_end = time() - function_begin
    print '---------------'
    print 'Old style queries took %s seconds' % function_end
    print '---------------'

def get_mean_household_income_by_year_and_subarea2(subarea, years, workbook, run_name, base_year, connection):
    # Get mean household income by subarea in a separate sheet
    # write column headings
    function_begin = time()
    worksheet = workbook.add_sheet('mean_hh_income_by_%s2' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        t0 = time()
        print '\nComputing mean household income by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute('''  SELECT
                                          CASE 
                                                WHEN u.avghhinc IS NULL THEN 0
                                                ELSE u.avghhinc
                                          END
                                    FROM
                                    (
                                    SELECT DISTINCT(%s_id)
                                    FROM %s_%s_zones
                                    ) r
                                    LEFT JOIN 
                                    (
                                    SELECT z.%s_id, ROUND(AVG(CAST(income AS FLOAT)),2) AS avghhinc
                                    FROM %s_%s_households h
                                    LEFT JOIN %s_%s_buildings b
                                    ON b.building_id = h.building_id
                                    LEFT JOIN %s_%s_zones z
                                    ON b.zone_id = z.zone_id
                                    GROUP BY z.%s_id
                                    ) u
                                    ON r.%s_id = u.%s_id
                                    ORDER BY r.%s_id
                               ''' % (subarea, run_name, year, subarea, run_name, year, run_name, year, run_name, year, subarea, subarea, subarea, subarea))
        t1 = time() - t0
        print 'Query took %s seconds' % t1
        t0 = time()
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        t1 = time() - t0
        print 'Writing to Excel took %s seconds' % t1
        r.close()
    function_end = time() - function_begin
    print '---------------'
    print 'New style queries took %s seconds' % function_end
    print '---------------'

def get_median_household_income_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get median household income by subarea in a separate sheet
    # write column headings
    seterr(invalid='ignore')
    worksheet = workbook.add_sheet('median_hh_income_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    distinct_subareas = []
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        distinct_subareas.append(row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing median household income by %s for year %s' % (subarea, year)
        row_counter = 1
        for sub in distinct_subareas:
            query = '''select
                            income
                        from %s_%s_households h
                        left join %s_%s_buildings b
                        on h.building_id = b.building_id
                        left join %s_%s_zones z
                        on b.zone_id = z.zone_id
                        where z.%s_id = %s''' % (run_name, year, run_name, year, run_name, year, subarea, sub)
            r = connection.execute(query)
            income_list = r.fetchall()
            median_income = median(array(income_list))
            if str(median_income) == 'nan':
                median_income = 'Null'
            worksheet.write(row_counter, column_counter, median_income)
            row_counter += 1
        column_counter += 1

def get_total_households_in_SFR_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total households in SFR by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('SFR_hh_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total SFR households by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numSFRhh
                    into #numSFRhh_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id = 1
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numSFRhh IS NULL THEN 0
                                    ELSE u.numSFRhh
                            END
                        from #distinct_%s r
                        left join #numSFRhh_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_households_in_MFR_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total households in MFR by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('MFR_hh_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total MFR households by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numMFRhh
                    into #numMFRhh_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id = 2
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numMFRhh IS NULL THEN 0
                                    ELSE u.numMFRhh
                            END
                        from #distinct_%s r
                        left join #numMFRhh_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_population_in_SFR_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total population in SFR by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('SFR_pop_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total SFR population by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numSFRpop
                    into #numSFRpop_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id = 1
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numSFRpop IS NULL THEN 0
                                    ELSE u.numSFRpop
                            END
                        from #distinct_%s r
                        left join #numSFRpop_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_population_in_MFR_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total population in MFR by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('MFR_pop_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total MFR population by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numMFRpop
                    into #numMFRpop_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id = 2
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numMFRpop IS NULL THEN 0
                                    ELSE u.numMFRpop
                            END
                        from #distinct_%s r
                        left join #numMFRpop_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total population by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('pop_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total population by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numhh
                    into #numpp_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numhh IS NULL THEN 0
                                    ELSE u.numhh
                            END
                        from #distinct_%s r
                        left join #numpp_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()
        

def get_total_population_by_year_and_subarea_stacked(subarea, years, workbook, run_name, base_year, connection):
    # Get total population by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('pop_by_%s_and_year_stacked' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    worksheet.write(0,1,'population')
    worksheet.write(0,2,'year')
    # write distinct subareas
    row_counter = 1
    for year in years:
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
    # get values and fill in table
    column_counter = 1
    row_counter = 1
    for year in years:
        print 'Computing total population by %s for year %s' % (subarea, year)
        #row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numhh
                    into #numpp_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numhh IS NULL THEN 0
                                    ELSE u.numhh
                            END
                        from #distinct_%s r
                        left join #numpp_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            worksheet.write(row_counter,column_counter+1,year)
            row_counter += 1
        r.close()



def get_total_DUs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total residential units by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('res_DUs_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total residential DUs by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        if year == base_year:
            query = '''select p.%s_id, sum(b.residential_units) as sum_res_units
                        into #res_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.residential_units) as sum_res_units
                        into #res_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sum_res_units IS NULL THEN 0
                                    ELSE u.sum_res_units
                            END
                        from #distinct_%s r
                        left join #res_units_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()
        
def get_total_DUs_SF_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total SF residential units by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('sf_DUs_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total SFR residential DUs by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        if year == base_year:
            query = '''select p.%s_id, sum(b.residential_units) as sum_SF_res_units
                        into #sfres_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        where b.building_type_id = 1
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.residential_units) as sum_SF_res_units
                        into #sfres_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        where b.building_type_id = 1
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sum_SF_res_units IS NULL THEN 0
                                    ELSE u.sum_SF_res_units
                            END
                        from #distinct_%s r
                        left join #sfres_units_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_DUs_MF_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total MF residential units by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('mf_DUs_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total MFR residential DUs by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        if year == base_year:
            query = '''select p.%s_id, sum(b.residential_units) as sum_MF_res_units
                        into #mfres_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        where b.building_type_id = 2
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.residential_units) as sum_MF_res_units
                        into #mfres_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        where b.building_type_id = 2
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sum_MF_res_units IS NULL THEN 0
                                    ELSE u.sum_MF_res_units
                            END
                        from #distinct_%s r
                        left join #mfres_units_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_nonres_sqft_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total non-residential sqft by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('nonres_sqft_by_%s_and_year' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # get distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing total non-residential sqft by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        if year == base_year:
            query = '''select p.%s_id, sum(b.non_residential_sqft) as sum_non_res_sqft
                        into #non_res_sqft_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.non_residential_sqft) as sum_non_res_sqft
                        into #non_res_sqft_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sum_non_res_sqft IS NULL THEN 0
                                    ELSE u.sum_non_res_sqft
                            END
                        from #distinct_%s r
                        left join #non_res_sqft_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def save_excel_workbook(run_name, excel_output_path, workbook):
    # check for existence of excel workbook, append date/time stamp if it exists
    try:
        excel_output_workbook_name = run_name + '.xls'
        if os.path.exists(os.path.join(excel_output_path,excel_output_workbook_name)):
            now = datetime.now()
            now = [str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second)]
            now = '-'.join(now)
            spl = excel_output_workbook_name.split('.')
            spl[0] = spl[0] + '_' + now
            excel_output_workbook_name = spl[0] + '.' + spl[1]
            print 'Excel workbook already exists, appending datetime stamp to filename'
            print 'Saving to workbook to: %s' % str(os.path.join(excel_output_path,excel_output_workbook_name))
            
            workbook.save(os.path.join(excel_output_path,excel_output_workbook_name))
        else:
            print 'Saving to workbook to: %s' % str(os.path.join(excel_output_path,excel_output_workbook_name))
            workbook.save(os.path.join(excel_output_path,excel_output_workbook_name))
    except:
        print 'No worksheets have been created, workbook not saved.'

def get_projects_runs_available_years(connection):
    
    # run query to get all tables
    query = 'select TABLE_NAME from INFORMATION_SCHEMA.TABLES'
    r = connection.execute(query)
    
    # get all opus tables
    all_opus_tables = []
    for row in r:
        result = row[0]
        if result[0:4] == 'opus':
            all_opus_tables.append(str(row[0]))
    r.close()
    
    # get all opus runs
    all_opus_runs = []
    for table in all_opus_tables:
        if '_runs_' in table:
            all_opus_runs.append(table)
    
    # get unique projects and runs
    all_opus_runs_split = []
    for table in all_opus_runs:
        all_opus_runs_split.append(table.split('_'))
    unique_runs = []
    unique_projects = []
    for table in all_opus_runs_split:
        this_project, this_run = table[1], table[3]
        if not this_project in unique_projects:
            unique_projects.append(this_project)
        if not this_run in unique_runs:
            unique_runs.append(this_run)

    #build nested dictionary of available projects, runs, years
    projects_runs_years = {}
    for project in unique_projects:
        projects_runs_years[project] = {}
        for i in all_opus_runs_split:
            if i[1] == project:
                if i[3] not in projects_runs_years[project]:
                    projects_runs_years[project][i[3]] = []
    for proj in projects_runs_years:
        for run in projects_runs_years[proj]:
            for i in all_opus_runs_split:
                if i[3] == run:
                    if i[4] not in projects_runs_years[proj][run]:
                        projects_runs_years[proj][run].append(i[4])
    
    return unique_projects, projects_runs_years

def get_available_subareas(connection, run_name, lowest_year):
    # run query to get all columns
    query = "select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '%s_%s_zones'" % (run_name, lowest_year)
    r = connection.execute(query)
    # sort through columns for subarea id columns
    available_subareas = []
    for row in r:
        if '_id' in row[0]:
             available_subareas.append(row[0].replace('_id',''))
    r.close()
    return available_subareas

def main():
    # choose project
    chosen_project = choicebox('Choose a project:','Available Projects',unique_projects)
    if not chosen_project:
        print 'User cancelled, ending script.'
        return 
    print 'chosen_project = %s' % chosen_project
    
    #given project, get available runs
    available_runs = []
    for run in projects_runs_years[chosen_project]:
        available_runs.append(run)
    
    # choose run
    chosen_run = choicebox('Choose a simulation run:','Available simulation runs',available_runs)
    if not chosen_run:
        print 'User cancelled, ending script.'
        return
    print 'chosen_run = %s' % chosen_run
    
    # given project and run, get available years
    available_years = projects_runs_years[chosen_project][chosen_run]
    available_years.sort()
    
    # choose years
    chosen_years_str = multchoicebox('Choose simulation years:','Available simulation years',available_years)
    chosen_years = []
    for i in chosen_years_str:
        chosen_years.append(int(i))
    chosen_years.sort()
    lowest_year = chosen_years[0]
    if not chosen_years:
        print 'User cancelled, ending script.'
        return
    print 'chosen_years = %s' % chosen_years

    # construct full run name
    run_name = 'opus_' + chosen_project + '_runs_' + chosen_run
    
    # given project and full run name, get available subareas
    available_subareas = get_available_subareas(connection, run_name, lowest_year)
    # choose subarea
    if available_subareas <> []:
        chosen_subarea = choicebox('Choose a subarea:','Available subareas',available_subareas)
        if not chosen_subarea:
            chosen_subarea = ''
            print 'No chosen subarea.'
        else:
            print 'chosen_subarea = %s' % chosen_subarea
    else:
        chosen_subarea = ''
    
    # other setup variables
    query_fields = ['Base Year','Years','Run Name','Excel Output Path','Subarea']
    query_default_values = ['2010',chosen_years,run_name,'c:/working/excel_outputs',chosen_subarea]
    query_variables = multenterbox('Confirm and/or update values','Report setup values',query_fields,query_default_values)
    if not query_variables:
        print 'User cancelled, ending script.'
        return
    run_name = query_variables[2]
    excel_output_path = query_variables[3]
    subarea = query_variables[4]
    base_year = int(query_variables[0])
    years = eval(query_variables[1])

    # create Excel workbook
    workbook = xlwt.Workbook()
    
    while True:
        report_list = \
                        [ 'get_total_population_by_year'
                        , 'get_total_households_by_year'
                        , 'get_total_households_by_number_of_children'
                        , 'get_total_households_by_household_size'
                        , 'get_total_households_by_number_of_workers'
                        , 'get_total_workers_in_households'
                        , 'get_total_jobs_by_year'
                        , 'get_total_DUs_by_year'
                        , 'get_percent_DUs_built'
                        , 'get_total_nonres_sqft_by_year'
                        , 'get_percent_nonres_sqft_built'
                        , 'get_total_DUs_SF_by_year'
                        , 'get_total_DUs_MF_by_year'
                        , 'get_total_households_by_year_and_income_category'
                        , 'get_total_unplaced_households_by_year'
                        , 'get_total_unplaced_households_by_income_categories'
                        , 'get_total_unplaced_jobs_by_year'
                        , 'get_total_unplaced_jobs_by_sector_and_year'
                        , 'get_total_jobs_by_sector_and_year'
                        , 'get_job_control_totals_by_year'
                        , 'get_houehold_control_totals_by_year'
                        , 'get_total_job_spaces_by_year'
                        , 'get_total_households_in_SFR_by_year'
                        , 'get_total_households_in_MFR_by_year'
                        , 'get_total_population_in_SFR_by_year'
                        , 'get_total_population_in_MFR_by_year'
                        , 'get_total_population_age_distribution_by_year'
                        , 'get_total_male_population_distribution_by_age_and_year'
                        , 'get_total_female_population_distribution_by_age_and_year'
                        , 'get_total_population_by_sex_and_year'
                        , 'get_mean_household_income_by_year'
                        , 'get_mean_age_of_population_by_year'
                        , 'get_median_household_income_by_year (CAUTION:VERY SLOW!)'
                        , 'get_median_age_of_population_by_year (CAUTION:VERY SLOW!)'
                        , 'get_total_nonres_sqft_by_type_and_year'
                        , 'get_total_DUs_in_active_developments_by_year'
                        , 'get_total_nonres_sqft_in_active_developments_by_year'
                        , 'get_total_unplaced_development_projects_by_year'
                        , 'get_total_population_by_race_and_year'
                        , 'get_mean_age_by_race_and_year'
                        , 'get_mean_persons_per_household_by_year'
                        , 'get_mean_persons_per_household_by_race_of_hh_head_and_year'
                        , 'get_total_households_by_number_of_vehicles'
                        ]
        
        # Add subarea query choices if subarea was specified
        if subarea <> '':
            report_list.extend(
                        [ 'get_total_jobs_by_year_and_subarea'
                        , 'get_total_households_by_year_and_subarea'
                        , 'get_total_population_by_year_and_subarea'
                        , 'get_total_DUs_by_year_and_subarea'
                        , 'get_total_nonres_sqft_by_year_and_subarea'
                        , 'get_total_DUs_MF_by_year_and_subarea'
                        , 'get_total_DUs_SF_by_year_and_subarea'
                        , 'get_total_households_in_SFR_by_year_and_subarea'
                        , 'get_total_households_in_MFR_by_year_and_subarea'
                        , 'get_total_population_in_SFR_by_year_and_subarea'
                        , 'get_total_population_in_MFR_by_year_and_subarea'
                        , 'get_mean_household_income_by_year_and_subarea'
                        , 'get_median_household_income_by_year_and_subarea (CAUTION:VERY SLOW!)'
                        , 'get_persons_per_household_by_year_and_subarea'
                        , 'get_households_by_income_quintile_by_year_and_subarea'
                        , 'get_total_population_by_year_and_subarea_stacked'
                        ]
                               )
        report_list.sort()
        
        # Open GUI
        text = 'Chosen project: %s\nChosen simulation run: %s\n\nChoose queries to run:' % (chosen_project, chosen_run)
        choices = multchoicebox(text,'Run Queries',report_list)
        if not choices:
            print 'User cancelled, ending script.'
            return
        
        # create report object:
        region_wide_report = RegionWideReport(workbook, years, connection, run_name, base_year)
        
        # Organize chosen queries into two lists
        region_wide_choices = []
        subarea_choices = []
        for choice in choices:
            if 'CAUTION' in choice:
                choice = choice.split()[0]
            if 'subarea' in choice:
                subarea_choices.append(choice)
            else:
                region_wide_choices.append(choice)
        
        # start timer
        t0 = time()
        
        # Run region wide queries
        for region_wide_choice in region_wide_choices:
            try:
                q = 'region_wide_report.%s()' % region_wide_choice
                exec(q)
            except exc.ProgrammingError, e:
                print '\nERROR when calling the following region-wide report method: \n%s' % q
                print '\nThere was a SQL error: \n%s\n' % (e)
        # Run subarea queries
        for subarea_choice in subarea_choices:
            try:
                q = '%s(subarea, years, workbook, run_name, base_year, connection)' % subarea_choice
                exec(q)
            except exc.ProgrammingError, e:
                print '\nERROR when calling the following subarea report function: \n%s' % q
                print '\nThere was a SQL error: \n%s\n' % (e)
        
        # print time of execution
        t1 = time() - t0
        print 'The queries took %s seconds' % (t1)
        
        # Save excel workbook
        print 'Report successful'
        save_excel_workbook(run_name, excel_output_path, workbook)
        return

if __name__ == "__main__":
    print 'Starting: Create Zone Simulation Report in Excel'
    # database connection variables   
    # get values from gui
    db_connection_fields = ['Username','Password','Server Name','Database Name']
    db_connection_default_values = ['AZSMARTExport','thebigone','MAG1113','AZSMART_V4_zone']
    db_connection_values = multenterbox('Enter SQL connection values:','SQL Connection',db_connection_fields,db_connection_default_values)
    if not db_connection_values:
        print 'User cancelled, ending script.'
        exit()
    # create the engine and connection
    try:
        engine = create_engine('mssql://%s:%s@%s/%s' % (db_connection_values[0], db_connection_values[1], db_connection_values[2], db_connection_values[3]))
        connection = engine.connect()
    except:
        print 'Connection to %s failed, ending script.' % db_connection_values[2]
        exit()
    print 'SQL connection to %s successful.' % db_connection_values[2]
    unique_projects, projects_runs_years = get_projects_runs_available_years(connection)
    main()

#############################
########### NOTES ###########
#############################
    
# TODO:
# add a drop table if exists function
# some of these queries were designed to be run w/ a full simulation uploaded to SQL (every year) instead of
#      a partial run (e.g. 2005,2010,2015).  Generalization of the code to handle these cases would be good

# - correct get_total_households_in_SFR_by_year (pop and MFR/SFR) not adding up to total

# queries TODO:
# - avg age by subarea
# - total MH dus (MF+SF dont add up to total)
# - 
# - hh by hh size by subarea
# - pp per hh by subarea




