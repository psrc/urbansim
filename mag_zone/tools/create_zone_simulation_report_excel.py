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

    def get_total_DUs_in_active_developments_by_year(self):
        # get total DUs in active developments by year
        self.worksheet.write(0,self.column_counter,'total_ADM_DUs')
        row_counter = 1
        for year in self.years:
            print('Computing total DUs in Active Developments for year %s' % year)
            r = self.connection.execute('select sum(current_built_units) from %s_%s_activeDevelopments where building_type_id in (1,2,3)' % (self.run_name,year))
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
            print('Computing total non-residential sqft in Active Developments for year %s' % year)
            r = self.connection.execute('select sum(cast(current_built_units as float)) from %s_%s_activeDevelopments where building_type_id not in (1,2)' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_group_quarters_households(self):
        # get total group quarters households by year
        self.worksheet.write(0,self.column_counter,'gq_hh')
        row_counter = 1
        for year in self.years:
            print('Computing total group quarters households for year %s' % year)
            r = self.connection.execute('''
                                SELECT
                                    sum(b.gq_households_in_dorms) + 
                                    sum(b.gq_households_in_juvenile_prisons) + 
                                    sum(b.gq_households_in_military) + 
                                    sum(b.gq_households_in_nursing_homes) + 
                                    sum(b.gq_households_in_other_inst) + 
                                    sum(b.gq_households_in_other_noninst) + 
                                    sum(b.gq_households_in_prisons) sumgq
                                FROM %s_%s_buildings b
                                left join %s_%s_zones z
                                on b.zone_id = z.zone_id
             ''' % (self.run_name,year,self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_total_group_quarters_population(self):
        # get total group quarters population by year
        self.worksheet.write(0,self.column_counter,'gq_pop')
        row_counter = 1
        for year in self.years:
            print('Computing total group quarters population for year %s' % year)
            r = self.connection.execute('''
                                SELECT
                                    sum(b.gq_pop_in_dorms) + 
                                    sum(b.gq_pop_in_juvenile_prisons) + 
                                    sum(b.gq_pop_in_military) + 
                                    sum(b.gq_pop_in_nursing_homes) + 
                                    sum(b.gq_pop_in_other_inst) + 
                                    sum(b.gq_pop_in_other_noninst) + 
                                    sum(b.gq_pop_in_prisons) sumgq
                                FROM %s_%s_buildings b
                                left join %s_%s_zones z
                                on b.zone_id = z.zone_id
             ''' % (self.run_name,year,self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_total_transient_population(self):
        # get total transient population by year
        self.worksheet.write(0,self.column_counter,'transient_pop')
        row_counter = 1
        for year in self.years:
            print('Computing total transient population for year %s' % year)
            r = self.connection.execute('''
                                SELECT
                                    sum(b.transient_pop_in_hotels + b.transient_pop_in_households) thhlds
                                FROM %s_%s_buildings b
                                left join %s_%s_zones z
                                on b.zone_id = z.zone_id
             ''' % (self.run_name,year,self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_total_transient_households(self):
        # get total transient households by year
        self.worksheet.write(0,self.column_counter,'transient_hh')
        row_counter = 1
        for year in self.years:
            print('Computing total transient households for year %s' % year)
            r = self.connection.execute('''
                                SELECT
                                    sum(b.transient_households_in_hotels + b.transient_households_in_households) thhlds
                                FROM %s_%s_buildings b
                                left join %s_%s_zones z
                                on b.zone_id = z.zone_id
             ''' % (self.run_name,year,self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_total_construction_jobs(self):
        # get the average age of the population by year
        self.worksheet.write(0,self.column_counter,'const_jobs')
        row_counter = 1
        for year in self.years:
            print('Computing total construction jobs for year %s' % year)
            r = self.connection.execute('select sum(construction_jobs) from %s_%s_zones' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1
        
    def get_total_non_site_based_jobs(self):
        # get the average age of the population by year
        self.worksheet.write(0,self.column_counter,'nsb_jobs')
        row_counter = 1
        for year in self.years:
            print('Computing total non site based jobs for year %s' % year)
            r = self.connection.execute('select sum(non_site_jobs) from %s_%s_zones' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_mean_age_of_population_by_year(self):
        # get the average age of the population by year
        self.worksheet.write(0,self.column_counter,'mean_pop_age')
        row_counter = 1
        for year in self.years:
            print('Computing mean age of population for year %s' % year)
            r = self.connection.execute('select ROUND(AVG(CAST(age AS float)),2) from %s_%s_persons where is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
        self.column_counter += 1

    def get_median_age_of_population_by_year(self):
        # get the median age of the population by year
        self.worksheet.write(0,self.column_counter,'median_pop_age')
        row_counter = 1
        for year in self.years:
            print('Computing median age of population for year %s' % year)
            r = self.connection.execute('SELECT age from %s_%s_persons where is_seasonal = 0' % (self.run_name, year))
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
            print('Computing total population under age 5 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 5-9 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 10-14 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_15_17')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 15-17 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 18 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_18_19')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 18-19 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 17 and age < 20 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 20-24 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 25-29 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 30-34 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 35-39 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 40-44 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 45-49 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 50-54 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 55-59 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_60_61')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 60-61 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 62 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_62_64')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 62-64 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 61 and age < 65 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 65-69 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 70-74 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 75-79 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 80-84 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'pop_age_over_84')
        row_counter = 1
        for year in self.years:
            print('Computing total population ages 85+ for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1


    def get_total_population_age_male_distribution_by_age_and_year(self):
        # get population in age brackets <5, 5-9, 10-15, 16-18, 19-24, 25-34, 35-44, 45-54, 55-64, 65+
        self.worksheet.write(0,self.column_counter, 'm_pop_age_under_5')
        row_counter = 1
        for year in self.years:
            print('Computing total male population under age 5 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 5-9 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 10-14 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_15_17')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 15-17 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 18 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_18_19')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 18-19 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 17 and age < 20 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 20-24 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 25-29 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 30-34 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 35-39 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 40-44 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 45-49 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 50-54 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 55-59 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_60_61')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 60-61 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 62 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_62_64')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 62-64 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 61 and age < 65 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 65-69 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 70-74 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 75-79 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 80-84 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'm_pop_age_over_84')
        row_counter = 1
        for year in self.years:
            print('Computing total male population ages 85+ for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and is_seasonal = 0 and sex = 1' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1


    def get_total_population_age_female_distribution_by_age_and_year(self):
        # get population in age brackets <5, 5-9, 10-15, 16-18, 19-24, 25-34, 35-44, 45-54, 55-64, 65+
        self.worksheet.write(0,self.column_counter, 'f_pop_age_under_5')
        row_counter = 1
        for year in self.years:
            print('Computing total female population under age 5 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age < 5 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_5_9')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 5-9 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 4 and age < 10 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_10_14')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 10-14 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 9 and age < 15 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_15_17')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 15-17 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 14 and age < 18 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_18_19')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 18-19 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 17 and age < 20 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_20_24')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 20-24 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 19 and age < 25 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_25_29')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 25-29 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 24 and age < 30 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_30_34')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 30-34 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 29 and age < 35 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_35_39')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 35-39 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 34 and age < 40 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_40_44')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 40-44 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 39 and age < 45 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_45_49')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 45-49 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 44 and age < 50 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_50_54')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 50-54 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 49 and age < 55 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_55_59')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 55-59 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 54 and age < 60 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_60_61')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 60-61 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 59 and age < 62 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_62_64')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 62-64 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 61 and age < 65 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_65_69')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 65-69 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 64 and age < 70 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_70_74')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 70-74 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 69 and age < 75 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_75_79')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 75-79 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 74 and age < 80 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_80_84')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 80-84 for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 79 and age < 85 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter, 'f_pop_age_over_84')
        row_counter = 1
        for year in self.years:
            print('Computing total female population ages 85+ for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where age > 84 and is_seasonal = 0 and sex = 2' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1


    def get_total_households_by_number_of_children(self):
        # Get the number of households by the number of children in the household
        # categories: 0,1,2,3,4,5,6,7+
        for year in self.years:
            print('Computing temporary tables for households by number of children for year %s' % year)
            query = '''
                    select household_id
                    into #distinct_hhlds%s
                    from %s_%s_households
                    where is_seasonal = 0
                    ''' % (year,self.run_name,year)
            r = self.connection.execute(query)
            r.close()
            query = '''
                    select
                        household_id,
                        count(*) num_children
                    into #hh_num_children%s
                    from %s_%s_persons
                    where age < 18 and is_seasonal = 0
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
            print('Computing total households with 0 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 0' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_1_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 1 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 1' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_2_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 2 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 2' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_3_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 3 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 3' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_4_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 4 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 4' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_5_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 5 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 5' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_6_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 6 children for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_with_num_children%s where num_children = 6' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_7up_children')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 7+ children for year %s' % year)
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
            print('Computing temporary tables for households by household size for year %s' % year)
            query = '''
                    select
                        household_id,
                        count(*) num_ppl
                    into #hh_num_ppl%s
                    from %s_%s_persons
                    where is_seasonal = 0
                    group by household_id
                    ''' % (year,self.run_name,year)
            r = self.connection.execute(query)
            r.close()
        self.worksheet.write(0,self.column_counter,'hh_size_1')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 1 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 1' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_2')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 2 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 2' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_3')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 3 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 3' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_4')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 4 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 4' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_5')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 5 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 5' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_6')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 6 for year %s' % year)
            r = self.connection.execute('select count(*) from #hh_num_ppl%s where num_ppl = 6' % (year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        self.worksheet.write(0,self.column_counter,'hh_size_7up')
        row_counter = 1
        for year in self.years:
            print('Computing total households with household size 7+ for year %s' % year)
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
            print('Computing total households with 0 vehicles for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles < 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_1_vehicle')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 1 vehicle for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_2_vehicles')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 2 vehicles for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 2 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_3_vehicles')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 3 vehicles for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles = 3 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_4up_vehicles')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 4+ vehicles for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where number_of_vehicles > 3 and is_seasonal = 0' % (self.run_name,year))
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
            print('Computing total households with 0 workers for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers < 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_1_worker')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 1 worker for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_2_workers')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 2 workers for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 2 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_3_workers')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 3 workers for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers = 3 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'hh_4up_workers')
        row_counter = 1
        for year in self.years:
            print('Computing total households with 4+ workers for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_households where workers > 3 and is_seasonal = 0' % (self.run_name,year))
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
            print('Computing total workers in households for year %s' % year)
            r = self.connection.execute('select sum(workers) from %s_%s_households where is_seasonal = 0' % (self.run_name,year))
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
            print('Computing total male population for year %s' % year)
            r = self.connection.execute('select COUNT(*) from %s_%s_persons where sex = 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter +=1
        self.worksheet.write(0,self.column_counter,'total_female_pop')
        row_counter = 1
        for year in self.years:
            print('Computing total female population for year %s' % year)
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
            print('Computing total residential DUs for year %s' % year)
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
            print('Computing total non-residential sqft for year %s' % year)
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
                print('Computing non-residential sqft for year %s and building type %s' % (year, building_type))
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
            print('Computing total SF residential DUs for year %s' % year)
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings where building_type_id in (1,3)' % (self.run_name, year))
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
            print('Computing total MF residential DUs for year %s' % year)
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
            print('Computing total households for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where is_seasonal = 0' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_seasonal_households_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_seas_hh')
        row_counter = 1
        for year in self.years:
            print('Computing total seasonal households for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where is_seasonal = 1' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_mean_household_income_by_year(self):
        self.worksheet.write(0,self.column_counter,'mean_hh_income')
        row_counter = 1
        for year in self.years:
            print('Computing mean household income for year %s' % year)
            r = self.connection.execute('SELECT ROUND(AVG(CAST(income as FLOAT)),2) from %s_%s_households where is_seasonal = 0' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_mean_persons_per_household_by_year(self):
        self.worksheet.write(0,self.column_counter,'mean_pp_per_hh')
        row_counter = 1
        for year in self.years:
            print('Computing mean persons per household for year %s' % year)
            r = self.connection.execute('select household_id, count(*) num_pphh into #pp_hh%s from %s_%s_persons where is_seasonal = 0 group by household_id' % (year, self.run_name, year))
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
            print('Computing median household income for year %s' % year)
            r = self.connection.execute('SELECT income from %s_%s_households where is_seasonal = 0' % (self.run_name, year))
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
            print('Computing total households in SFR for year %s' % year)
            query = '''
                    select
                        count(*)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id in (1,3) and h.is_seasonal = 0
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
            print('Computing total households in MFR for year %s' % year)
            query = '''
                    select
                        count(*)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 2 and h.is_seasonal = 0
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
            print('Computing total population in SFR for year %s' % year)
            query = '''
                    select
                        sum(persons)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id in (1,3) and h.is_seasonal = 0
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
            print('Computing total population in MFR for year %s' % year)
            query = '''
                    select
                        sum(persons)
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    where b.building_type_id = 2 and h.is_seasonal = 0
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
            print('Computing total population for year %s' % year)
            try:
                r = self.connection.execute('select sum(persons) from %s_%s_households where is_seasonal = 0' % (self.run_name, year))
            except:
                r = self.connection.execute('select count(*) from %s_%s_persons where is_seasonal = 0' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_seasonal_population_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_seas_pop')
        row_counter = 1
        for year in self.years:
            print('Computing total seasonal population for year %s' % year)
            try:
                r = self.connection.execute('select sum(persons) from %s_%s_households where is_seasonal = 1' % (self.run_name, year))
            except:
                r = self.connection.execute('select count(*) from %s_%s_persons where is_seasonal = 1' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_jobs_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_jobs')
        row_counter = 1
        for year in self.years:
            print('Computing total jobs for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_jobs' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_hb_jobs_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_hb_jobs')
        row_counter = 1
        for year in self.years:
            print('Computing total home based jobs for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_jobsWithSchools2 j join %s_%s_buildings b on j.building_id = b.building_id where b.building_type_id < 4' % (self.run_name, year, self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter, self.column_counter, row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_nhb_jobs_by_year(self):
        self.worksheet.write(0,self.column_counter,'total_nhb_jobs')
        row_counter = 1
        for year in self.years:
            print('Computing total non home based jobs for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_jobs j join %s_%s_buildings b on j.building_id = b.building_id where b.building_type_id > 3' % (self.run_name, year))
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
            print('Computing households <50k income for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where income < 50001 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        # households between 50k and 100k
        self.worksheet.write(0,self.column_counter + 1,'total_hh_income_1')
        row_counter = 1
        for year in self.years:
            print('Computing households >50k income <100k for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where income > 50000 and income <100001 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 1,row[0])
                row_counter += 1
            r.close()
        # households over 100k
        self.worksheet.write(0,self.column_counter + 2,'total_hh_income_2')
        row_counter = 1
        for year in self.years:
            print('Computing households >100k income for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where income > 100000 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 2,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 3

    def get_annual_population_control_totals_by_year(self):
        self.worksheet.write(0,self.column_counter,'population_ct')
        row_counter = 1
        print('Computing population control totals')
        r = self.connection.execute('select year, sum(total_population) from %s_%s_annualHouseholdControlTotals where is_seasonal = 0 group by year order by year' % (self.run_name, self.base_year))
        for row in r:
            if row_counter == 1 and row[0] == (self.base_year + 1):
                self.worksheet.write(row_counter,self.column_counter,0)
                row_counter += 1
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
            else:
                self.worksheet.write(row_counter,self.column_counter,row[1])
                row_counter += 1
        r.close()
        self.column_counter += 1

    def get_annual_employment_control_totals_by_year(self):
        self.worksheet.write(0,self.column_counter,'employment_ct')
        row_counter = 1
        print('Computing employment control totals')
        r = self.connection.execute('select year, sum(total_number_of_jobs) from %s_%s_annualEmploymentControlTotals group by year order by year' % (self.run_name, self.base_year))
        for row in r:
            if row_counter == 1 and row[0] == (self.base_year + 1):
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
            print('Computing unplaced development projects for year %s' % year)
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
            print('Computing unplaced households for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1
        
    def get_total_unplaced_population_by_year(self):
        # Get unplaced household totals by year
        self.worksheet.write(0,self.column_counter,'unplaced_pp')
        row_counter = 1
        for year in self.years:
            print('Computing unplaced population for year %s' % year)
            r = self.connection.execute('select sum(persons) from %s_%s_households where building_id < 1 and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                if row[0]:
                    self.worksheet.write(row_counter,self.column_counter,row[0])
                    row_counter += 1
                else:
                    self.worksheet.write(row_counter,self.column_counter,0)
                    row_counter += 1                    
            r.close()
        self.column_counter += 1

    def get_total_unplaced_households_by_income_categories(self):
        # Get unplaced household totals by household income category
        # unplaced households under 50k
        self.worksheet.write(0,self.column_counter,'unpl_hh_0_50k')
        row_counter = 1
        for year in self.years:
            print('Computing unplaced households <50k income for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income < 50001) and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        # unplaced households between 50k and 100k
        self.worksheet.write(0,self.column_counter + 1,'unpl_hh_50_100k')
        row_counter = 1
        for year in self.years:
            print('Computing unplaced households >50k income <100k for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income > 50000 and income <100001) and is_seasonal = 0' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter + 1,row[0])
                row_counter += 1
            r.close()
        # unplaced households over 100k
        self.worksheet.write(0,self.column_counter + 2,'unpl_hh_100k_up')
        row_counter = 1
        for year in self.years:
            print('Computing unplaced households >100k income for year %s' % year)
            r = self.connection.execute('select count(*) from %s_%s_households where building_id < 1 and (income > 100000) and is_seasonal = 0' % (self.run_name,year))
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
            print('Computing unplaced jobs for year %s' % year)
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
                print('Computing unplaced jobs for year %s and sector %s' % (year, sector))
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
                print('Computing jobs for year %s and sector %s' % (year, sector))
                query = 'select count(*) from %s_%s_jobs where sector_id = %s' % (self.run_name, year, sector)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(sectors)
        
    def get_total_jobs_by_land_use_sector_and_year(self):
        # Get job totals by sector and year
        # Get sectors
        r = self.connection.execute('select distinct(report_sector_id) from basedata_zaReference_buildingTypes order by report_sector_id')
        sectors = []
        for row in r:
            sectors.append(row[0])
        r.close()
        # Get totals
        column_counter = self.column_counter # was 14
        for sector in sectors:
            row_counter = 1
            if sector == 2:
                label = 'RET'
            elif sector == 3:
                label = 'IND'
            elif sector == 4:
                label = 'OFF'
            elif sector == 5:
                label = 'OTH'
            elif sector == 6:
                label = 'PUB'
            elif sector == 1:
                label = 'WAH'
            self.worksheet.write(0,column_counter,'jobs_lu%s' % label)
            for year in self.years:
                print('Computing jobs for year %s and land use sector %s' % (year, sector))
                query = '''
                            select
                                count(*)
                            from
                                %s_%s_jobs j
                            left join %s_%s_buildings b
                            on j.building_id = b.building_id
                            left join basedata_zaReference_buildingTypes bt
                            on b.building_type_id = bt.building_type_id
                            where bt.report_sector_id = %s          
                        ''' % (self.run_name, year, self.run_name, year, sector)                       
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(sectors)

    def get_total_hb_jobs_by_sector_and_year(self):
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
            self.worksheet.write(0,column_counter,'job_hb_sec%s' % sector)
            for year in self.years:
                print('Computing home based jobs for year %s and sector %s' % (year, sector))
                query = 'select count(*) from %s_%s_jobsWithSchools2 where sector_id = %s and home_based_status = 1' % (self.run_name, year, sector)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(sectors)

    def get_total_nhb_jobs_by_sector_and_year(self):
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
            self.worksheet.write(0,column_counter,'job_nhb_sec%s' % sector)
            for year in self.years:
                print('Computing non home based jobs for year %s and sector %s' % (year, sector))
                query = 'select count(*) from %s_%s_jobsWithSchools2 where sector_id = %s and home_based_status = 0' % (self.run_name, year, sector)
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
        r = self.connection.execute('select distinct(race) from %s_%s_persons where is_seasonal = 0 order by race' % (self.run_name, self.base_year))
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
                print('Computing total population for year %s and race %s' % (year, race))
                query = 'select count(*) from %s_%s_persons where race = %s and is_seasonal = 0' % (self.run_name, year, race)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(races)


    def get_total_households_by_income_quintile_and_year(self):
        # Get total households by income quintile and year
        
        # compute temp tables
        for year in self.years:
            print('Computing temp tables for household quintiles for year %s' % (year))
            query = '''
                        SELECT
                            NTILE(5) OVER(ORDER BY h.income) AS qtile
                        into #hhquintsregion%s
                        FROM %s_%s_households h
                        where h.is_seasonal = 0                        
                    ''' % (year, self.run_name, year)
            r = self.connection.execute(query)
            r.close()
        
        # compute totals and put into worksheet
        income_quintiles = [1,2,3,4,5]
        column_counter = self.column_counter
        for q in income_quintiles:
            row_counter = 1
            self.worksheet.write(0,column_counter,'hh_quint0%s' % q)
            for year in self.years:
                print('Computing total households for year %s and income quintile %s' % (year, q))                
                query = '''
                        SELECT
                            COUNT(*)
                        FROM #hhquintsregion%s
                        WHERE qtile = %s    
                        ''' % (year, q)
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,column_counter,row[0])
                r.close()
                row_counter += 1
            column_counter += 1
        self.column_counter += len(income_quintiles)


    def get_mean_persons_per_household_by_race_of_hh_head_and_year(self):
        # Get mean persons per by race and year
        # Get races
        r = self.connection.execute('select distinct(race) from %s_%s_persons where is_seasonal = 0 order by race' % (self.run_name, self.base_year))
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
                print('Computing mean persons per household for year %s and race %s' % (year, race))
                if year not in temp_tables_years:
                    r = self.connection.execute('select household_id, count(*) as num_pp_in_hh into tmp_p_hh%s from %s_%s_persons where is_seasonal = 0 group by household_id' % (year, self.run_name, year))
                    r.close()
                    r = self.connection.execute('select household_id, race into tmp_head_race%s from %s_%s_persons where head_of_hh = 1 and is_seasonal = 0' % (year, self.run_name, year))
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
        r = self.connection.execute('select distinct(race) from %s_%s_persons where is_seasonal = 0 order by race' % (self.run_name, self.base_year))
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
                print('Computing mean age for year %s and race %s' % (year, race))
                query = 'select ROUND(AVG(CAST(age as FLOAT)),1) from %s_%s_persons where race = %s and is_seasonal = 0' % (self.run_name, year, race)
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
            print('Computing total job spaces for year %s' % year)
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



def get_total_unplaced_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total unplaced jobs by subarea in a separate sheet
    # write column headings
    subarea = 'super_raz'
    worksheet = workbook.add_sheet('unpl_jobs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'unpl_emp_y'+str(year))
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
        print('Computing total unplaced jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select h.%s_id, count(*) as numjobs
                    into #numunpljobs_%s
                    from %s_%s_jobs h
                    where h.building_id < 1
                    group by h.%s_id
                    order by h.%s_id''' % (subarea, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numjobs IS NULL THEN 0
                                    ELSE u.numjobs
                            END
                        from #distinct_%s r
                        left join #numunpljobs_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_emp_y'+str(year))
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
        print('Computing total jobs by %s for year %s' % (subarea, year))
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

def get_total_transient_households_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total transient households by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('transhh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'trans_hh_y'+str(year))
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
        print('Computing total transient households by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        z.%s_id,
                        sum(b.transient_households_in_hotels + b.transient_households_in_households) thhlds
                    INTO #numtranhh_%s
                    FROM %s_%s_buildings b
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id
                ''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.thhlds IS NULL THEN 0
                                    ELSE u.thhlds
                            END
                        from #distinct_%s r
                        left join #numtranhh_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_transient_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total transient population by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('transpop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'trans_pop_y'+str(year))
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
        print('Computing total transient population by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        z.%s_id,
                        sum(b.transient_pop_in_hotels + b.transient_pop_in_households) thhlds
                    INTO #numtranpp_%s
                    FROM %s_%s_buildings b
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id
                ''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.thhlds IS NULL THEN 0
                                    ELSE u.thhlds
                            END
                        from #distinct_%s r
                        left join #numtranpp_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()



def get_total_group_quarters_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total group quarters population by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('gqpop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'gq_pop_y'+str(year))
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
        print('Computing total group quarters population by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        z.%s_id,
                        sum(b.gq_pop_in_dorms) + 
                        sum(b.gq_pop_in_juvenile_prisons) + 
                        sum(b.gq_pop_in_military) + 
                        sum(b.gq_pop_in_nursing_homes) + 
                        sum(b.gq_pop_in_other_inst) + 
                        sum(b.gq_pop_in_other_noninst) + 
                        sum(b.gq_pop_in_prisons) sumgq
                    INTO #numgqpop_%s
                    FROM %s_%s_buildings b
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id
                ''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sumgq IS NULL THEN 0
                                    ELSE u.sumgq
                            END
                        from #distinct_%s r
                        left join #numgqpop_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_group_quarters_households_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total group quarters households by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('gqhh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'gq_hh_y'+str(year))
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
        print('Computing total group quarters households by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        z.%s_id,
                        sum(b.gq_households_in_dorms) + 
                        sum(b.gq_households_in_juvenile_prisons) + 
                        sum(b.gq_households_in_military) + 
                        sum(b.gq_households_in_nursing_homes) + 
                        sum(b.gq_households_in_other_inst) + 
                        sum(b.gq_households_in_other_noninst) + 
                        sum(b.gq_households_in_prisons) sumgq
                    INTO #numgqhh_%s
                    FROM %s_%s_buildings b
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    group by z.%s_id
                    order by z.%s_id
                ''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.sumgq IS NULL THEN 0
                                    ELSE u.sumgq
                            END
                        from #distinct_%s r
                        left join #numgqhh_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_construction_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total construction jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('const_jobs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_const_emp_y'+str(year))
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
        print('Computing total construction jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        %s_id,
                        sum(construction_jobs) numjobs
                    INTO #numcnstjobs_%s
                    FROM %s_%s_zones
                    group by %s_id
                    order by %s_id
                    ''' % (subarea, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numjobs IS NULL THEN 0
                                    ELSE u.numjobs
                            END
                        from #distinct_%s r
                        left join #numcnstjobs_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_non_site_based_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total construction jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('nonsite_jobs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_nsb_emp_y'+str(year))
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
        print('Computing total construction jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''
                    SELECT
                        %s_id,
                        sum(non_site_jobs) numjobs
                    INTO #numnsbjobs_%s
                    FROM %s_%s_zones
                    group by %s_id
                    order by %s_id
                    ''' % (subarea, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numjobs IS NULL THEN 0
                                    ELSE u.numjobs
                            END
                        from #distinct_%s r
                        left join #numnsbjobs_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_jobs_nhb_by_sector_and_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_nhb_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_nhb_emp_y'+str(year))
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
        print('Computing total home based jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numjobs
                    into #numjobsnhb_%s
                    from %s_%s_jobs h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id > 3
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
                        left join #numjobsnhb_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_jobs_hb_by_sector_and_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_hb_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_hb_emp_y'+str(year))
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
        print('Computing total home based jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numjobs
                    into #numjobshb_%s
                    from %s_%s_jobs h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id < 4
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
                        left join #numjobshb_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_nhb_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_nhb_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_nhb_emp_y'+str(year))
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
        print('Computing total non-home based jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numjobs
                    into #numjobsnhb_%s
                    from %s_%s_jobs h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id > 3
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
                        left join #numjobsnhb_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_hb_jobs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total home based jobs by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('jobs_hb_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_hb_emp_y'+str(year))
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
        print('Computing total home based jobs by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numjobs
                    into #numjobshb_%s
                    from %s_%s_jobs h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where b.building_type_id < 4
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
                        left join #numjobshb_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()


def get_total_unplaced_households_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total unplaced households by subarea in a separate sheet
    # write column headings
    subarea = 'super_raz'
    worksheet = workbook.add_sheet('unpl_hh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'unpl_hh_y'+str(year))
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
        print('Computing total unplaced households by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select h.%s_id, count(*) as numhh
                    into #numunplhh_%s
                    from %s_%s_households h
                    where h.is_seasonal = 0 and h.building_id < 1
                    group by h.%s_id
                    order by h.%s_id''' % (subarea, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numhh IS NULL THEN 0
                                    ELSE u.numhh
                            END
                        from #distinct_%s r
                        left join #numunplhh_%s u
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
    worksheet = workbook.add_sheet('hh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_hh_y'+str(year))
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
        print('Computing total households by %s for year %s' % (subarea, year))
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
                    where h.is_seasonal = 0
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

def get_total_seasonal_households_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total households by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('hh_seas_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_seas_hh_y'+str(year))
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
        print('Computing total seasonal households by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, count(*) as numhh
                    into #numhhse_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where h.is_seasonal = 1
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
                        left join #numhhse_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

def get_total_jobs_by_land_use_sector_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    for sector in range(1,7):
        # Get total jobs by income sectors by subarea in a separate sheet
        # write column headings (years)
        
        if sector == 2:
            label = 'RET'
        elif sector == 3:
            label = 'IND'
        elif sector == 4:
            label = 'OFF'
        elif sector == 5:
            label = 'OTH'
        elif sector == 6:
            label = 'PUB'
        elif sector == 1:
            label = 'WAH'
        
        worksheet = workbook.add_sheet('jobs_by_%s' % (label))
        worksheet.write(0,0,'%s_id' % (subarea))
        
        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'tot_emp_%s_y%s' % (str(label),str(year)))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        
        # get values and fill in table
        column_counter = 1
        for year in years:
            print('Computing total households for income sector %s by %s for year %s' % (sector, subarea, year))
            row_counter = 1
            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
            r.close()
            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
            r.close()
            query = '''
                        select
                            z.%s_id,
                            count(*) as numjobs
                        into #numjlus_%s_%s
                        from %s_%s_jobs j
                        left join %s_%s_buildings b
                        on j.building_id = b.building_id
                        left join basedata_zaReference_buildingTypes bt
                        on b.building_type_id = bt.building_type_id
                        left join %s_%s_zones z
                        on b.zone_id = z.zone_id
                        where bt.report_sector_id = %s
                        group by z.%s_id
                        order by z.%s_id
                    ''' % (subarea, year, sector, run_name, year, run_name, year, run_name, year, sector, subarea, subarea)
            r = connection.execute(query)
            r.close()
            r = connection.execute('''select
                                CASE 
                                        WHEN u.numjobs IS NULL THEN 0
                                        ELSE u.numjobs
                                END
                            from #distinct_%s r
                            left join #numjlus_%s_%s u
                            on r.%s_id = u.%s_id
                            order by r.%s_id''' % (subarea, year, sector, subarea, subarea, subarea))
            for row in r:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            r.close()


def get_total_nhb_jobs_by_sector_and_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by employment sectors by subarea in separate sheets    
    # get sectors
    r = connection.execute('select sector_id from %s_%s_employmentSectors order by sector_id' % (run_name, base_year))
    sectors = []
    for row in r:
        sectors.append(row[0])
    r.close()    
    
    for sector in sectors:
        # write column headings (years)
        worksheet = workbook.add_sheet('jobs_nhb_empsec_%s' % (sector))
        worksheet.write(0,0,'%s_id' % (subarea))
        
        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'tot_nhb_emp_%s_y%s' % (str(sector),str(year)))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        
        # get values and fill in table
        column_counter = 1
        for year in years:
            print('Computing total nhb jobs by sector %s by %s for year %s' % (sector, subarea, year))
            row_counter = 1
            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
            r.close()
            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
            r.close()
            r = connection.execute(
                            '''
                                SELECT
                                    CASE
                                        WHEN j.num_jobs is null THEN 0
                                        ELSE j.num_jobs
                                    END
                                FROM #distinct_%s r
                                left join (
                                    SELECT
                                        z.%s_id,
                                        count(*) num_jobs
                                    FROM %s_%s_jobs j
                                    left join %s_%s_buildings b
                                    on b.building_id = j.building_id
                                    left join %s_%s_zones z
                                    on b.zone_id = z.zone_id
                                    where j.sector_id = %s and b.building_type_id > 3
                                    group by z.%s_id
                                    ) j
                                on r.%s_id = j.%s_id
                                order by r.%s_id
                            ''' % (subarea, subarea, run_name, year, run_name, year, run_name, year, sector, subarea, subarea, subarea, subarea))
            for row in r:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            r.close()


def get_total_hb_jobs_by_sector_and_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by employment sectors by subarea in separate sheets    
    # get sectors
    r = connection.execute('select sector_id from %s_%s_employmentSectors order by sector_id' % (run_name, base_year))
    sectors = []
    for row in r:
        sectors.append(row[0])
    r.close()    
    
    for sector in sectors:
        # write column headings (years)
        worksheet = workbook.add_sheet('jobs_hb_empsec_%s' % (sector))
        worksheet.write(0,0,'%s_id' % (subarea))
        
        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'tot_hb_emp_%s_y%s' % (str(sector),str(year)))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        
        # get values and fill in table
        column_counter = 1
        for year in years:
            print('Computing total hb jobs by sector %s by %s for year %s' % (sector, subarea, year))
            row_counter = 1
            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
            r.close()
            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
            r.close()
            r = connection.execute(
                            '''
                                SELECT
                                    CASE
                                        WHEN j.num_jobs is null THEN 0
                                        ELSE j.num_jobs
                                    END
                                FROM #distinct_%s r
                                left join (
                                    SELECT
                                        z.%s_id,
                                        count(*) num_jobs
                                    FROM %s_%s_jobs j
                                    left join %s_%s_buildings b
                                    on b.building_id = j.building_id
                                    left join %s_%s_zones z
                                    on b.zone_id = z.zone_id
                                    where j.sector_id = %s and b.building_type_id < 4
                                    group by z.%s_id
                                    ) j
                                on r.%s_id = j.%s_id
                                order by r.%s_id
                            ''' % (subarea, subarea, run_name, year, run_name, year, run_name, year, sector, subarea, subarea, subarea, subarea))
            for row in r:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            r.close()

def get_total_jobs_by_sector_and_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total jobs by employment sectors by subarea in separate sheets    
    # get sectors
    r = connection.execute('select sector_id from %s_%s_employmentSectors order by sector_id' % (run_name, base_year))
    sectors = []
    for row in r:
        sectors.append(row[0])
    r.close()    
    
    for sector in sectors:
        # write column headings (years)
        worksheet = workbook.add_sheet('jobs_empsec_%s' % (sector))
        worksheet.write(0,0,'%s_id' % (subarea))
        
        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'tot_emp_%s_y%s' % (str(sector),str(year)))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        
        # get values and fill in table
        column_counter = 1
        for year in years:
            print('Computing total jobs by sector %s by %s for year %s' % (sector, subarea, year))
            row_counter = 1
            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
            r.close()
            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
            r.close()
            r = connection.execute(
                            '''
                                SELECT
                                    CASE
                                        WHEN j.num_jobs is null THEN 0
                                        ELSE j.num_jobs
                                    END
                                FROM #distinct_%s r
                                left join (
                                    SELECT
                                        z.%s_id,
                                        count(*) num_jobs
                                    FROM %s_%s_jobs j
                                    left join %s_%s_buildings b
                                    on b.building_id = j.building_id
                                    left join %s_%s_zones z
                                    on b.zone_id = z.zone_id
                                    where j.sector_id = %s
                                    group by z.%s_id
                                    ) j
                                on r.%s_id = j.%s_id
                                order by r.%s_id
                            ''' % (subarea, subarea, run_name, year, run_name, year, run_name, year, sector, subarea, subarea, subarea, subarea))
            for row in r:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            r.close()


def get_total_households_by_income_quintile_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):

    # create temp tables:
    # create distinct subareas
    r = connection.execute('select distinct(%s_id) into #distinct1_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
    r.close()
    # create distinct quintiles
    query = '''
                SELECT 1 as quint into #quints;
                INSERT INTO #quints
                VALUES(2);
                INSERT INTO #quints
                VALUES(3);
                INSERT INTO #quints
                VALUES(4);
                INSERT INTO #quints
                VALUES(5);                
            '''
    r = connection.execute(query)
    r.close()
    # cross join for unique combinations
    query = '''
                SELECT * 
                INTO #distinct1_%s_quints
                FROM #distinct1_%s
                cross join #quints
                order by %s_id, quint                
            ''' % (subarea, subarea, subarea)
    r = connection.execute(query)
    r.close()
    
    # create temporary tables for each year
    for year in years:
        # get quints on households
        print('Computing temp tables for total households for income quintiles for year %s' % (year))
        query = '''
                    SELECT
                        h.*,
                        NTILE(5) OVER (ORDER BY h.income) as 'income_quints'
                    into #hhquints%s
                    FROM %s_%s_households h
                    WHERE h.is_seasonal = 0
                ''' % (year, run_name, year)
        r = connection.execute(query)
        r.close()
        # group up all hh w/quints by subarea
        query = '''
                    SELECT
                        z.%s_id,
                        h.income_quints,
                        count(*) num_hh
                    INTO #hhquints_by_%s_%s
                    FROM #hhquints%s h
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    left join %s_%s_zones z
                    on z.zone_id = b.zone_id
                    group by z.%s_id, h.income_quints
                    order by z.%s_id, h.income_quints
                ''' % (subarea, subarea, year, year, run_name, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close() 
        # join hh w/quints to unique quint/subarea combination
        query = '''
                    SELECT
                        d.%s_id,
                        d.quint as quintile,
                        CASE
                            WHEN h.num_hh is null THEN 0
                            ELSE h.num_hh
                        END num_hh
                    INTO #hh_by_quint_by_%s_%s
                    FROM #distinct1_%s_quints d
                    left join #hhquints_by_%s_%s h
                    on d.%s_id = h.%s_id and d.quint = h.income_quints
                    order by d.%s_id, h.income_quints            
                ''' % (subarea, subarea, year, subarea, subarea, year, subarea, subarea, subarea)
        r = connection.execute(query)
        r.close()

    # actually start putting the stuff into worksheets
    for quintile in range(1,6):
        # Get total households by income quintiles by subarea in a separate sheet
        # write column headings (years)
        worksheet = workbook.add_sheet('hh_inc_quint_%s_by_%s' % (quintile, subarea))
        worksheet.write(0,0,'%s_id' % (subarea))

        # write column labels:
        column_counter = 1
        for year in years:
            worksheet.write(0,column_counter,'y'+str(year)+'hhq'+str(quintile))
            column_counter += 1
        # get distinct subareas and write to 1st column as IDs
        row_counter = 1
        r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
        for row in r:
            worksheet.write(row_counter,0,row[0])
            row_counter += 1
        r.close()

        # get values and fill in table
        column_counter = 1
        for year in years:
            print('Computing total households for income quintile %s by %s for year %s' % (quintile, subarea, year))
            row_counter = 1
#            r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
#            r.close()
#            r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
#            r.close()
            query = '''
                        SELECT
                            num_hh
                        FROM #hh_by_quint_by_%s_%s
                        where quintile = %s
                        order by %s_id
                    ''' % (subarea, year, quintile, subarea)
            results = connection.execute(query)
            for row in results:
                worksheet.write(row_counter,column_counter,row[0])
                row_counter += 1
            column_counter += 1
            results.close()

def get_mean_persons_per_household_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get persons per household by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('pphh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'pph_y'+str(year))
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
        print('Computing persons per household by %s for year %s' % (subarea, year))
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
                    where p.is_seasonal = 0
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


def get_mean_age_of_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get persons per household by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('avg_age_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'avg_age_y'+str(year))
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
        print('Computing mean population age by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select
                        z.%s_id,
                        round(avg(cast(p.age as float)),2) avg_age
                    into #avg_age_%s
                    from %s_%s_persons p
                    left join %s_%s_households h
                    on p.household_id = h.household_id
                    left join %s_%s_buildings b
                    on h.building_id = b.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where p.is_seasonal = 0 and h.building_id > 0
                    group by z.%s_id''' % (subarea, year, run_name, year, run_name, year, run_name, year, run_name, year, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    when h.avg_age IS null then 0
                                    else h.avg_age
                            END
                        from #distinct_%s u
                        left join #avg_age_%s h
                        on h.%s_id = u.%s_id
                        order by u.%s_id''' % (subarea, year, subarea, subarea, subarea))
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
        worksheet.write(0,column_counter,'avg_inc_y'+str(year))
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
        print('\nComputing mean household income by %s for year %s' % (subarea, year))
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
                    where h.is_seasonal = 0
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
        print('Query took %s seconds' % t1)
        t0 = time()
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        t1 = time() - t0
        print('Writing to Excel took %s seconds' % t1)
        r.close()
    function_end = time() - function_begin
    print('---------------')
    print('Old style queries took %s seconds' % function_end)
    print('---------------')

def get_mean_household_income_by_year_and_subarea2(subarea, years, workbook, run_name, base_year, connection):
    # Get mean household income by subarea in a separate sheet
    # write column headings
    function_begin = time()
    worksheet = workbook.add_sheet('mean_hh_income_by_%s2' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'avg_inc_y'+str(year))
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
        print('\nComputing mean household income by %s for year %s' % (subarea, year))
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
                                    WHERE h.is_seasonal = 0
                                    GROUP BY z.%s_id
                                    ) u
                                    ON r.%s_id = u.%s_id
                                    ORDER BY r.%s_id
                               ''' % (subarea, run_name, year, subarea, run_name, year, run_name, year, run_name, year, subarea, subarea, subarea, subarea))
        t1 = time() - t0
        print('Query took %s seconds' % t1)
        t0 = time()
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        t1 = time() - t0
        print('Writing to Excel took %s seconds' % t1)
        r.close()
    function_end = time() - function_begin
    print('---------------')
    print('New style queries took %s seconds' % function_end)
    print('---------------')

def get_median_household_income_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get median household income by subarea in a separate sheet
    # write column headings
    seterr(invalid='ignore')
    worksheet = workbook.add_sheet('median_hh_income_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'med_inc_y'+str(year))
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
        print('Computing median household income by %s for year %s' % (subarea, year))
        row_counter = 1
        for sub in distinct_subareas:
            query = '''select
                            income
                        from %s_%s_households h
                        left join %s_%s_buildings b
                        on h.building_id = b.building_id
                        left join %s_%s_zones z
                        on b.zone_id = z.zone_id
                        where z.%s_id = %s and h.is_seasonal = 0''' % (run_name, year, run_name, year, run_name, year, subarea, sub)
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
    worksheet = workbook.add_sheet('SFR_hh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_sfr_hh_y'+str(year))
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
        print('Computing total SFR households by %s for year %s' % (subarea, year))
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
                    where b.building_type_id in (1,3) and h.is_seasonal = 0
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
    worksheet = workbook.add_sheet('MFR_hh_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_mfr_hh_y'+str(year))
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
        print('Computing total MFR households by %s for year %s' % (subarea, year))
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
                    where b.building_type_id = 2 and h.is_seasonal = 0
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
    worksheet = workbook.add_sheet('SFR_pop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_sfr_pop_y'+str(year))
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
        print('Computing total SFR population by %s for year %s' % (subarea, year))
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
                    where b.building_type_id in (1,3) and h.is_seasonal = 0
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
    worksheet = workbook.add_sheet('MFR_pop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_mfr_pop_y'+str(year))
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
        print('Computing total MFR population by %s for year %s' % (subarea, year))
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
                    where b.building_type_id = 2 and h.is_seasonal = 0
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
    worksheet = workbook.add_sheet('pop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_pop_y'+str(year))
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
        print('Computing total population by %s for year %s' % (subarea, year))
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
                    where h.is_seasonal = 0
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
        
        
def get_total_unplaced_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total unplaced population by subarea in a separate sheet
    # write column headings
    subarea = 'super_raz'
    worksheet = workbook.add_sheet('unpl_pop_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'unpl_pop_y'+str(year))
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
        print('Computing total unplaced population by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select h.%s_id, sum(h.persons) as numhh
                    into #numunplpp_%s
                    from %s_%s_households h
                    where h.is_seasonal = 0 and h.building_id < 1
                    group by h.%s_id
                    order by h.%s_id''' % (subarea, year, run_name, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        r = connection.execute('''select
                            CASE 
                                    WHEN u.numhh IS NULL THEN 0
                                    ELSE u.numhh
                            END
                        from #distinct_%s r
                        left join #numunplpp_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()
        
        
def get_total_seasonal_population_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total population by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('pop_seas_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_seas_pop_y'+str(year))
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
        print('Computing total seasonal population by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numhh
                    into #numppseas_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where h.is_seasonal = 1
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
                        left join #numppseas_%s u
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
    worksheet = workbook.add_sheet('pop_by_%s_stacked' % (subarea))
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
        print('Computing total population by %s for year %s' % (subarea, year))
        #row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        query = '''select z.%s_id, sum(persons) as numhh
                    into #numpp1_%s
                    from %s_%s_households h
                    left join %s_%s_buildings b
                    on b.building_id = h.building_id
                    left join %s_%s_zones z
                    on b.zone_id = z.zone_id
                    where h.is_seasonal= 0
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
                        left join #numpp1_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            worksheet.write(row_counter,column_counter+1,year)
            row_counter += 1
        r.close()


def get_total_DU_capacity_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total residential unit capacity by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('res_DUcap_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_du_cap_y'+str(year))
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
        print('Computing total residential DU capacity by %s for year %s' % (subarea, year))
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        if year == base_year:
            query = '''select p.%s_id, sum(b.residential_units_capacity) as sum_res_units
                        into #res_unitscap_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.residential_units_capacity) as sum_res_units
                        into #res_unitscap_%s
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
                        left join #res_unitscap_%s u
                        on r.%s_id = u.%s_id
                        order by r.%s_id''' % (subarea, year, subarea, subarea, subarea))
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()



def get_total_DUs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total residential units by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('res_DUs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_du_y'+str(year))
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
        print('Computing total residential DUs by %s for year %s' % (subarea, year))
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
    worksheet = workbook.add_sheet('sf_DUs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_sfr_du_y'+str(year))
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
        print('Computing total SFR residential DUs by %s for year %s' % (subarea, year))
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
                        where b.building_type_id in (1,3)
                        group by p.%s_id
                        order by p.%s_id''' % (subarea, year, run_name, year, run_name, year, subarea, subarea)
        else:
            query = '''select p.%s_id, sum(b.residential_units) as sum_SF_res_units
                        into #sfres_units_%s
                        from %s_%s_buildings b
                        left join %s_%s_zones p
                        on b.zone_id = p.zone_id
                        where b.building_type_id in (1,3)
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
    worksheet = workbook.add_sheet('mf_DUs_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_mfr_du_y'+str(year))
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
        print('Computing total MFR residential DUs by %s for year %s' % (subarea, year))
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
    worksheet = workbook.add_sheet('nonres_sqft_by_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'tot_nonres_sqft_y'+str(year))
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
        print('Computing total non-residential sqft by %s for year %s' % (subarea, year))
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
            print('Excel workbook already exists, appending datetime stamp to filename')
            print('Saving to workbook to: %s' % str(os.path.join(excel_output_path,excel_output_workbook_name)))
            
            workbook.save(os.path.join(excel_output_path,excel_output_workbook_name))
        else:
            print('Saving to workbook to: %s' % str(os.path.join(excel_output_path,excel_output_workbook_name)))
            workbook.save(os.path.join(excel_output_path,excel_output_workbook_name))
    except:
        print('No worksheets have been created, workbook not saved.')

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
                        try:
                            yr = int(i[4])
                            projects_runs_years[proj][run].append(i[4])
                        except:
                            pass
    
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
        print('User cancelled, ending script.')
        return 
    print('chosen_project = %s' % chosen_project)
    
    #given project, get available runs
    available_runs = []
    for run in projects_runs_years[chosen_project]:
        available_runs.append(run)
    
    # choose run
    chosen_run = choicebox('Choose a simulation run:','Available simulation runs',available_runs)
    if not chosen_run:
        print('User cancelled, ending script.')
        return
    print('chosen_run = %s' % chosen_run)
    
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
        print('User cancelled, ending script.')
        return
    print('chosen_years = %s' % chosen_years)

    # construct full run name
    run_name = 'opus_' + chosen_project + '_runs_' + chosen_run
    
    # given project and full run name, get available subareas
    available_subareas = get_available_subareas(connection, run_name, lowest_year)
    # choose subarea
    if available_subareas != []:
        chosen_subarea = choicebox('Choose a subarea:','Available subareas',available_subareas)
        if not chosen_subarea:
            chosen_subarea = ''
            print('No chosen subarea.')
        else:
            print('chosen_subarea = %s' % chosen_subarea)
    else:
        chosen_subarea = ''
    
    # other setup variables
    query_fields = ['Base Year','Years','Run Name','Excel Output Path','Subarea']
    query_default_values = ['2010',chosen_years,run_name,'c:/working/excel_outputs',chosen_subarea]
    query_variables = multenterbox('Confirm and/or update values','Report setup values',query_fields,query_default_values)
    if not query_variables:
        print('User cancelled, ending script.')
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
                        , 'get_total_hb_jobs_by_year'
                        #, 'get_total_nhb_jobs_by_year'
                        , 'get_total_DUs_by_year'
                        #, 'get_total_nonres_sqft_by_year'
                        , 'get_total_DUs_SF_by_year'
                        , 'get_total_DUs_MF_by_year'
                        #, 'get_total_households_by_year_and_income_category'
                        , 'get_total_unplaced_households_by_year'
                        , 'get_total_unplaced_population_by_year'
                        #, 'get_total_unplaced_households_by_income_categories'
                        , 'get_total_unplaced_jobs_by_year'
                        #, 'get_total_unplaced_jobs_by_sector_and_year'
                        , 'get_total_jobs_by_sector_and_year'
                        , 'get_total_hb_jobs_by_sector_and_year'
                        , 'get_total_nhb_jobs_by_sector_and_year'
                        , 'get_annual_employment_control_totals_by_year'
                        , 'get_annual_population_control_totals_by_year'
                        #, 'get_total_job_spaces_by_year'
                        , 'get_total_households_in_SFR_by_year'
                        , 'get_total_households_in_MFR_by_year'
                        , 'get_total_population_in_SFR_by_year'
                        , 'get_total_population_in_MFR_by_year'
                        , 'get_total_population_age_distribution_by_year'
                        , 'get_total_population_age_male_distribution_by_age_and_year'
                        , 'get_total_population_age_female_distribution_by_age_and_year'
                        , 'get_total_population_by_sex_and_year'
                        , 'get_mean_household_income_by_year'
                        , 'get_mean_age_of_population_by_year'
                        #, 'get_median_household_income_by_year (CAUTION:VERY SLOW!)'
                        #, 'get_median_age_of_population_by_year (CAUTION:VERY SLOW!)'
                        #, 'get_total_nonres_sqft_by_type_and_year'
                        #, 'get_total_DUs_in_active_developments_by_year'
                        #, 'get_total_nonres_sqft_in_active_developments_by_year'
                        #, 'get_total_unplaced_development_projects_by_year'
                        , 'get_total_population_by_race_and_year'
                        #, 'get_mean_age_by_race_and_year'
                        , 'get_mean_persons_per_household_by_year'
                        #, 'get_mean_persons_per_household_by_race_of_hh_head_and_year'
                        , 'get_total_households_by_number_of_vehicles'
                        , 'get_total_seasonal_population_by_year'
                        , 'get_total_seasonal_households_by_year'
                        , 'get_total_jobs_by_land_use_sector_and_year'
                        , 'get_total_households_by_income_quintile_and_year'
                        , 'get_total_construction_jobs'
                        , 'get_total_non_site_based_jobs'
                        , 'get_total_transient_households'
                        , 'get_total_transient_population'
                        #, 'get_total_group_quarters_households'
                        , 'get_total_group_quarters_population'
                        ]
        
        # Add subarea query choices if subarea was specified
        if subarea != '':
            report_list.extend(
                        [ 'get_total_jobs_by_year_and_subarea'
                        , 'get_total_hb_jobs_by_year_and_subarea'
                        #, 'get_total_nhb_jobs_by_year_and_subarea'
                        , 'get_total_households_by_year_and_subarea'
                        , 'get_total_population_by_year_and_subarea'
                        , 'get_total_DUs_by_year_and_subarea'
                        , 'get_total_DU_capacity_by_year_and_subarea'
                        #, 'get_total_nonres_sqft_by_year_and_subarea'
                        , 'get_total_DUs_MF_by_year_and_subarea'
                        , 'get_total_DUs_SF_by_year_and_subarea'
                        , 'get_total_households_in_SFR_by_year_and_subarea'
                        , 'get_total_households_in_MFR_by_year_and_subarea'
                        , 'get_total_population_in_SFR_by_year_and_subarea'
                        , 'get_total_population_in_MFR_by_year_and_subarea'
                        , 'get_mean_household_income_by_year_and_subarea'
                        #, 'get_mean_household_income_by_year_and_subarea2'
                        #, 'get_median_household_income_by_year_and_subarea (CAUTION:VERY SLOW!)'
                        , 'get_mean_persons_per_household_by_year_and_subarea'
                        , 'get_total_households_by_income_quintile_by_year_and_subarea'
                        #, 'get_total_population_by_year_and_subarea_stacked'
                        , 'get_total_seasonal_households_by_year_and_subarea'
                        , 'get_total_seasonal_population_by_year_and_subarea'
                        , 'get_total_jobs_by_land_use_sector_by_year_and_subarea'
                        , 'get_mean_age_of_population_by_year_and_subarea'
                        , 'get_total_jobs_by_sector_and_year_and_subarea'
                        , 'get_total_jobs_hb_by_sector_and_year_and_subarea'
                        , 'get_total_jobs_nhb_by_sector_and_year_and_subarea'
                        , 'get_total_construction_jobs_by_year_and_subarea'
                        , 'get_total_non_site_based_jobs_by_year_and_subarea'
                        , 'get_total_transient_households_by_year_and_subarea'
                        , 'get_total_unplaced_households_by_year_and_subarea'
                        , 'get_total_unplaced_population_by_year_and_subarea'
                        , 'get_total_unplaced_jobs_by_year_and_subarea'
                        #, 'get_total_group_quarters_households_by_year_and_subarea'
                        , 'get_total_group_quarters_population_by_year_and_subarea'
                        , 'get_total_transient_population_by_year_and_subarea'
                        , 'get_total_hb_jobs_by_sector_and_year_and_subarea'
                        , 'get_total_nhb_jobs_by_sector_and_year_and_subarea'
                        ]
                               )
        report_list.sort()
        
        # Open GUI
        text = 'Chosen project: %s\nChosen simulation run: %s\n\nChoose queries to run:' % (chosen_project, chosen_run)
        choices = multchoicebox(text,'Run Queries',report_list)
        if not choices:
            print('User cancelled, ending script.')
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
            except exc.ProgrammingError as e:
                print('\nERROR when calling the following region-wide report method: \n%s' % q)
                print('\nThere was a SQL error: \n%s\n' % (e))
        # Run subarea queries
        for subarea_choice in subarea_choices:
            try:
                q = '%s(subarea, years, workbook, run_name, base_year, connection)' % subarea_choice
                exec(q)
            except exc.ProgrammingError as e:
                print('\nERROR when calling the following subarea report function: \n%s' % q)
                print('\nThere was a SQL error: \n%s\n' % (e))
        
        # print time of execution
        t1 = time() - t0
        print('The queries took %s seconds' % (t1))
        
        # Save excel workbook
        print('Report successful')
        save_excel_workbook(run_name, excel_output_path, workbook)
        return

if __name__ == "__main__":
    print('Starting: Create Zone Simulation Report in Excel')
    # database connection variables   
    # get values from gui
    db_connection_fields = ['Username','Password','Server Name','Database Name']
    db_connection_default_values = ['AZSMARTExport','thebigone','SQL\AZSMART','AZSMART_V5_zone']
    db_connection_values = multenterbox('Enter SQL connection values:','SQL Connection',db_connection_fields,db_connection_default_values)
    if not db_connection_values:
        print('User cancelled, ending script.')
        exit()
    # create the engine and connection
    try:
        engine = create_engine('mssql://%s:%s@%s/%s' % (db_connection_values[0], db_connection_values[1], db_connection_values[2], db_connection_values[3]))
        connection = engine.connect()
    except:
        print('Connection to %s failed, ending script.' % db_connection_values[2])
        exit()
    print('SQL connection to %s successful.' % db_connection_values[2])
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


# - subarea NAICS sector based emp

# TODO: REMOVE HARD CODING OF LAND USE BASED EMPLOYMENT SECTOR TABLE

## OLD Queries to redo or save
#    def get_percent_DUs_built(self):
#        # get percent of DU capacity built
#        self.worksheet.write(0,self.column_counter,'pct_DUs_built')
#        row_counter = 1
#        for year in self.years:
#            print 'Computing percent of DUs built for year %s' % year
#            r = self.connection.execute('select SUM(residential_units)/SUM(residential_units_capacity) from %s_%s_buildings' % (self.run_name,year))
#            for row in r:
#                self.worksheet.write(row_counter,self.column_counter,row[0])
#                row_counter += 1
#            r.close()
#        self.column_counter += 1
#
#    def get_percent_nonres_sqft_built(self):
#        # get percent of nonres sqft capacity built
#        self.worksheet.write(0,self.column_counter,'pct_nonres_sqft_built')
#        row_counter = 1
#        for year in self.years:
#            print 'Computing percent of nonres sqft built for year %s' % year
#            r = self.connection.execute('select SUM(non_residential_sqft)/SUM(non_residential_sqft_capacity) from %s_%s_buildings' % (self.run_name,year))
#            for row in r:
#                self.worksheet.write(row_counter,self.column_counter,row[0])
#                row_counter += 1
#            r.close()
#        self.column_counter += 1

