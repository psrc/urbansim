# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from sqlalchemy import create_engine
from datetime import datetime
from easygui import multenterbox, multchoicebox
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

    def get_total_DUs_by_year(self):
        # Get total residential units by year
        self.worksheet.write(0,self.column_counter,'total_units')
        row_counter = 1
        for year in self.years:
            print 'Computing total residential units for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_nonres_sqft_by_year(self):
        # Get total residential units by year
        self.worksheet.write(0,self.column_counter,'total_nonres_sqft')
        row_counter = 1
        for year in self.years:
            print 'Computing total non residential sqft for year %s' % year
            r = self.connection.execute('select sum(cast(non_residential_sqft as float)) from %s_%s_buildings' % (self.run_name,year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_DUs_SF_by_year(self):
        # Get total single family residential units by year
        self.worksheet.write(0,self.column_counter,'total_SF_units')
        row_counter = 1
        for year in self.years:
            print 'Computing total SF residential units for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings where building_type_id = 1' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_DUs_MF_by_year(self):
        # Get total multi family residential units by year
        self.worksheet.write(0,self.column_counter,'total_MF_units')
        row_counter = 1
        for year in self.years:
            print 'Computing total MF residential units for year %s' % year
            r = self.connection.execute('select sum(residential_units) from %s_%s_buildings where building_type_id = 2' % (self.run_name, year))
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
                row_counter += 1
            r.close()
        self.column_counter += 1

    def get_total_vacant_DUs_by_year(self):
        # Get total vacant residential units by year
        self.worksheet.write(0,self.column_counter,'vacant_res_units')
        row_counter = 1
        for year in self.years:
            print 'Computing vacant residential units for year %s' % year
            r = self.connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units','local') IS NOT NULL DROP TABLE #bldg_res_units")
            r.close()
            query = '''
                    select building_id, residential_units
                    into #bldg_res_units
                    from %s_%s_buildings
                    ''' % (self.run_name, year)
            r = self.connection.execute(query)
            r.close()
            r = self.connection.execute("IF OBJECT_ID('tempdb..#hh_by_building','local') IS NOT NULL DROP TABLE #hh_by_building")
            r.close()
            query = '''
                    select building_id, count(*) as total_hh
                    into #hh_by_building
                    from %s_%s_households
                    group by building_id
                    ''' % (self.run_name, year)
            r = self.connection.execute(query)
            r.close()
            r = self.connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units_hh','local') IS NOT NULL DROP TABLE #bldg_res_units_hh")
            r.close()
            query = '''
                    select
                            b.building_id,
                            b.residential_units,
                            case
                                    when h.total_hh is null then 0
                                    else h.total_hh
                            end as num_hh
                    into #bldg_res_units_hh
                    from #bldg_res_units b
                    left join #hh_by_building h
                    on b.building_id = h.building_id
                    '''
            r = self.connection.execute(query)
            r.close()
            r = self.connection.execute("IF OBJECT_ID('tempdb..#vac_res_units','local') IS NOT NULL DROP TABLE #vac_res_units")
            r.close()
            query = '''
                    select
                            building_id,
                            residential_units,
                            num_hh,
                            residential_units - num_hh as vacant_res_units
                    into #vac_res_units
                    from #bldg_res_units_hh
                    '''
            r = self.connection.execute(query)
            r.close()
            query = '''
                    select sum(vacant_res_units) from #vac_res_units where vacant_res_units > 0
                    '''
            r = self.connection.execute(query)
            for row in r:
                self.worksheet.write(row_counter,self.column_counter,row[0])
            r.close
            row_counter += 1
        self.column_counter += 1

    def get_total_vacant_DUs_by_type_and_year(self):
        # Get vacant residential units by type and year
        r = self.connection.execute('select building_type_id, building_type_name from %s_%s_buildingTypes where is_residential = 1 order by building_type_id' % (self.run_name, self.base_year))
        building_types = []
        building_type_names = []
        for row in r:
            building_types.append(str(row[0]).strip())
            building_type_names.append(str(row[1]).strip())
        r.close()
        for (indx, btype) in enumerate(building_types):
            row_counter = 1
            self.worksheet.write(0,self.column_counter,'vacant_%s' % building_type_names[indx])
            for year in self.years:
                print 'Computing vacant %s units for year %s' % (building_type_names[indx], year)
                r = self.connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units','local') IS NOT NULL DROP TABLE #bldg_res_units")
                r.close()
                query = '''
                        select building_id, residential_units
                        into #bldg_res_units
                        from %s_%s_buildings
                        where building_type_id = %s
                        ''' % (self.run_name, year, btype)
                r = self.connection.execute(query)
                r.close()
                r = self.connection.execute("IF OBJECT_ID('tempdb..#hh_by_building','local') IS NOT NULL DROP TABLE #hh_by_building")
                r.close()
                query = '''
                        select building_id, count(*) as total_hh
                        into #hh_by_building
                        from %s_%s_households
                        group by building_id
                        ''' % (self.run_name, year)
                r = self.connection.execute(query)
                r.close()
                r = self.connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units_hh','local') IS NOT NULL DROP TABLE #bldg_res_units_hh")
                r.close()
                query = '''
                        select
                                b.building_id,
                                b.residential_units,
                                case
                                        when h.total_hh is null then 0
                                        else h.total_hh
                                end as num_hh
                        into #bldg_res_units_hh
                        from #bldg_res_units b
                        left join #hh_by_building h
                        on b.building_id = h.building_id
                        '''
                r = self.connection.execute(query)
                r.close()
                r = self.connection.execute("IF OBJECT_ID('tempdb..#vac_res_units','local') IS NOT NULL DROP TABLE #vac_res_units")
                r.close()
                query = '''
                        select
                                building_id,
                                residential_units,
                                num_hh,
                                residential_units - num_hh as vacant_res_units
                        into #vac_res_units
                        from #bldg_res_units_hh
                        '''
                r = self.connection.execute(query)
                r.close()
                query = '''
                        select sum(vacant_res_units) from #vac_res_units where vacant_res_units > 0
                        '''
                r = self.connection.execute(query)
                for row in r:
                    self.worksheet.write(row_counter,self.column_counter,row[0])
                r.close()
                row_counter += 1
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
            r = self.connection.execute('select sum(persons) from %s_%s_households' % (self.run_name, year))
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

## SOMETHING IS WRONG W/ THIS QUERY
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
## NEEDS TO BE REWORKED TO ACCOUNT FOR SUBAREA ID NOT BEING ON BUILDINGS TABLE
## SEE 1ST MULTILINE QUERY THAT SUBSTITUTES 'subarea' 1ST
##
##def get_household_density_per_acre_by_subarea(subarea, years, workbook, run_name, base_year, connection):
##    # Get household density per acre by subarea in a separate sheet
##    # write column headings
##    worksheet = workbook.add_sheet('hh_density_by_%s_and_year' % (subarea))
##    worksheet.write(0,0,'%s_id' % (subarea))
##    column_counter = 1
##    for year in years:
##        worksheet.write(0,column_counter,'y'+str(year))
##        column_counter += 1
##    # get distinct subareas
##    row_counter = 1
##    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
##    for row in r:
##        worksheet.write(row_counter,0,row[0])
##        row_counter += 1
##    # get values and fill in table
##    column_counter = 1
##    for year in years:
##        print 'Computing households per acre by %s for %s' % (subarea, year)
##        row_counter = 1
##        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
##        r.close()
##        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
##        r.close()
##        query = '''select count(*) num_hh, b.%s_id, avg(z.acres) acres
##                    into #hh_zones_acres_%s
##                    from %s_%s_households h
##                    left join %s_%s_buildings b
##                    on h.building_id = b.building_id
##                    left join %s_%s_zones z
##                    on b.zone_id = z.zone_id
##                    group by b.zone_id
##                    order by b.zone_id''' % (subarea, year, run_name, year, run_name, year, run_name, year)
##        r = connection.execute(query)
##        r.close()
##        r = connection.execute('''select
##                                        case
##                                                when h.num_hh/h.acres is null then 0
##                                                else h.num_hh/h.acres
##                                        end
##                                from #distinct_%s d
##                                left join #hh_zones_acres_%s h
##                                on d.zone_id = h.zone_id
##                                order by d.zone_id''' % (subarea,year))
##        for row in r:
##            worksheet.write(row_counter, column_counter,row[0])
##            row_counter += 1
##        column_counter += 1
##        r.close()

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

def get_total_DUs_by_year_and_subarea(subarea, years, workbook, run_name, base_year, connection):
    # Get total residential units by subarea in a separate sheet
    # write column headings
    worksheet = workbook.add_sheet('res_units_by_%s_and_year' % (subarea))
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
        print 'Computing total residential units by %s for year %s' % (subarea, year)
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
        print 'Computing total SFR residential units by %s for year %s' % (subarea, year)
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
        print 'Computing total MFR residential units by %s for year %s' % (subarea, year)
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

def get_total_vacant_DUs_by_year_and_subarea(subarea, workbook, years, connection, run_name, base_year):
    # Get vacant residential units by year and subarea
    worksheet = workbook.add_sheet('vac_res_units_by_year_%s' % (subarea))
    worksheet.write(0,0,'%s_id' % (subarea))
    # get years
    column_counter = 1
    for year in years:
        worksheet.write(0,column_counter,'y'+str(year))
        column_counter += 1
    # write distinct subareas
    row_counter = 1
    r = connection.execute('select distinct(%s_id) from %s_%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
    subarea_counter = 0
    for row in r:
        worksheet.write(row_counter,0,row[0])
        row_counter += 1
        subarea_counter += 1
    r.close()
    # get values and fill in table
    column_counter = 1
    for year in years:
        print 'Computing vacant residential units by %s for year %s' % (subarea, year)
        row_counter = 1
        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
        r.close()
        r = connection.execute('select distinct(%s_id) into #distinct_%s from %s_%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea))
        r.close()
        r = connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units','local') IS NOT NULL DROP TABLE #bldg_res_units")
        r.close()
        query = '''
                select b.building_id, b.residential_units, p.%s_id
                into #bldg_res_units
                from %s_%s_buildings b
                left join %s_%s_zones p
                on b.zone_id = p.zone_id
                ''' % (subarea, run_name, year, run_name, year)
        r = connection.execute(query)
        r.close()
        r = connection.execute("IF OBJECT_ID('tempdb..#hh_by_building','local') IS NOT NULL DROP TABLE #hh_by_building")
        r.close()
        query = '''
                select building_id, count(*) as total_hh
                into #hh_by_building
                from %s_%s_households
                group by building_id
                ''' % (run_name, year)
        r = connection.execute(query)
        r.close()
        r = connection.execute("IF OBJECT_ID('tempdb..#bldg_res_units_hh','local') IS NOT NULL DROP TABLE #bldg_res_units_hh")
        r.close()
        query = '''
                select
                        b.building_id,
                        b.residential_units,
                        b.%s_id,
                                case
                                        when h.total_hh is null then 0
                                        else h.total_hh
                                end as num_hh
                into #bldg_res_units_hh
                from #bldg_res_units b
                left join #hh_by_building h
                on b.building_id = h.building_id
                ''' % subarea
        r = connection.execute(query)
        r.close()
        r = connection.execute("IF OBJECT_ID('tempdb..#vac_res_units','local') IS NOT NULL DROP TABLE #vac_res_units")
        r.close()
        query = '''
                select
                        building_id,
                        residential_units,
                        num_hh,
                        %s_id,
                        residential_units - num_hh as vacant_res_units
                into #vac_res_units
                from #bldg_res_units_hh
                ''' % subarea
        r = connection.execute(query)
        r.close()
        r = connection.execute("IF OBJECT_ID('tempdb..#vac_res_units_%s','local') IS NOT NULL DROP TABLE #vac_res_units_%s" % (year, year))
        r.close()
        query = '''
                select 
                        %s_id,
                        sum(vacant_res_units) as sum_vac_res_units
                into #vac_res_units_%s
                from #vac_res_units
                where vacant_res_units > 0
                group by %s_id
                order by %s_id
                ''' % (subarea, year, subarea, subarea)
        r = connection.execute(query)
        r.close()
        query = '''
                select
                        case
                                when s.sum_vac_res_units is null then 0
                                else s.sum_vac_res_units
                        end
                from #distinct_%s r
                left join #vac_res_units_%s s
                on r.%s_id = s.%s_id
                order by r.%s_id
                ''' % (subarea, year, subarea, subarea, subarea)
        r = connection.execute(query)
        for row in r:
            worksheet.write(row_counter,column_counter,row[0])
            row_counter += 1
        column_counter += 1
        r.close()

## NEEDS WORK
##def get_vacant_job_spaces_by_subarea(subarea, years, workbook, run_name, base_year, connection):
##    # Get vacant residential units by year and subarea
##    worksheet = workbook.add_sheet('vac_job_spaces_by_year_%s' % (subarea))
##    worksheet.write(0,0,'%s_id' % (subarea))
##    # get years
##    column_counter = 1
##    for year in years:
##        worksheet.write(0,column_counter,'y'+str(year))
##        column_counter += 1
##    # write distinct subareas
##    row_counter = 1
##    r = connection.execute('select distinct(%s_id) from %s_Y%s_zones order by %s_id' % (subarea, run_name, base_year, subarea))
##    subarea_counter = 0
##    for row in r:
##        worksheet.write(row_counter,0,row[0])
##        row_counter += 1
##        subarea_counter += 1
##    r.close()
##    # get values and fill in table
##    column_counter = 1
##    for year in years:
##        print 'Computing vacant job spaces by %s for year %s' % (subarea, year)
##        row_counter = 1
##        r = connection.execute("IF OBJECT_ID('tempdb..#distinct_%s','local') IS NOT NULL DROP TABLE #distinct_%s" % (subarea, subarea))
##        r.close()
##        query = 'select distinct(%s_id) into #distinct_%s from %s_Y%s_zones order by %s_id' % (subarea, subarea, run_name, base_year, subarea)
##        r = connection.execute(query)
##        r.close()
##        # get buildings w/ zone_id into temp table
##        r = connection.execute("IF OBJECT_ID('tempdb..#temp_buildings','local') IS NOT NULL DROP TABLE #temp_buildings")
##        r.close()
##        query = '''
##                    select
##                            b.building_id, b.building_type_id,
##                            b.non_residential_sqft, p.zone_id
##                    into #temp_buildings
##                    from %s_Y%s_buildings b
##                    left join %s_Y%s_zones p
##                    on b.zone_id = p.zone_id
##                ''' % (run_name, year, run_name, year)
##        r = connection.execute(query)
##        r.close()
##        # join sqft per job w/ temp buildings
##        r = connection.execute("IF OBJECT_ID('tempdb..#temp_buildings2','local') IS NOT NULL DROP TABLE #temp_buildings2")
##        r.close()
##        query = '''
##                    select t.*, b.building_sqft_per_job
##                    into #temp_buildings2
##                    from #temp_buildings t
##                    left join %s_Y%s_building_sqft_per_job b
##                    on t.zone_id = b.zone_id and t.building_type_id = b.building_type_id
##                ''' % (run_name, year)
##        r = connection.execute(query)
##        r.close()
##        # get count of jobs by building
##        r = connection.execute("IF OBJECT_ID('tempdb..#temp_jobs_by_bldg','local') IS NOT NULL DROP TABLE #temp_jobs_by_bldg")
##        r.close()
##        query = '''
##                    select 
##                            building_id, count(*) as num_jobs
##                    into #temp_jobs_by_bldg
##                    from %s_Y%s_jobs
##                    group by building_id
##                ''' % (run_name, year)
##        r = connection.execute(query)
##        r.close()
##        # combine building and job data
##        r = connection.execute("IF OBJECT_ID('tempdb..#buildings_jobs','local') IS NOT NULL DROP TABLE #buildings_jobs")
##        r.close()
##        query = '''
##                    select
##                            t.*, j.num_jobs
##                    into #buildings_jobs
##                    from #temp_buildings2 t
##                    left join #temp_jobs_by_bldg j
##                    on t.building_id = j.building_id
##                '''
##        r = connection.execute(query)
##        r.close()        
##        # update jobs data to zero where null
##        query = '''
##                    update #buildings_jobs
##                    set num_jobs = 0
##                    where num_jobs is null
##                '''
##        r = connection.execute(query)
##        r.close()
##        # compute total and vacant job spaces
##        r = connection.execute("IF OBJECT_ID('tempdb..#job_space_data','local') IS NOT NULL DROP TABLE #job_space_data")
##        r.close()
##        query = '''
##                    select
##                            building_id, zone_id, num_jobs,
##                            non_residential_sqft/building_sqft_per_job as total_job_spaces,
##                            (non_residential_sqft/building_sqft_per_job)-num_jobs as vacant_job_spaces
##                    into #job_space_data
##                    from #buildings_jobs
##                '''
##        r = connection.execute(query)
##        r.close()
##        # update vacant spaces to zero where < 1
##        query = '''
##                    update #job_space_data
##                    set vacant_job_spaces = 0
##                    where vacant_job_spaces < 1
##                '''
##        r = connection.execute(query)
##        r.close()
##        # calculate vacant job space by subarea
##        r = connection.execute("IF OBJECT_ID('tempdb..#vac_job_space_by_subarea','local') IS NOT NULL DROP TABLE #vac_job_space_by_subarea")
##        r.close()
##        query = '''
##                    select p.%s_id, sum(j.vacant_job_spaces) as vac_job_spc
##                    into #vac_job_space_by_subarea
##                    from #job_space_data j
##                    left join %s_Y%s_zones p
##                    on j.zone_id = p.zone_id
##                    group by p.%s_id
##                ''' % (subarea, run_name, year, subarea)
##        r = connection.execute(query)
##        r.close()
##        # join data to distinct subareas
##        query = '''
##                    select s.%s_id, 
##                               case
##                                    when v.vac_job_spc is null then 0
##                                    else v.vac_job_spc
##                               end
##                    from #distinct_%s s
##                    left join #vac_job_space_by_subarea v
##                    on s.%s_id = v.%s_id
##                ''' % (subarea, subarea, subarea, subarea)
##        r = connection.execute(query)
##        for row in r:
##            worksheet.write(row_counter,column_counter,row[1])
##            row_counter += 1
##        column_counter += 1
##        r.close()


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

def main():
    
    # other setup variables
    query_fields = ['Base Year','End Year','Run Name','Excel Output Path','Subarea']
    query_default_values = ['2009','2030','opus_magZoneV3c_runs_','c:/working/excel_outputs','']
    query_variables = multenterbox('','Enter Values',query_fields,query_default_values)
    base_year = int(query_variables[0])
    end_year = int(query_variables[1])
    run_name = query_variables[2]
    excel_output_path = query_variables[3]
    subarea = query_variables[4]
    years = range(base_year,end_year+1)

    # create Excel workbook
    workbook = xlwt.Workbook()
    
    while True:
        report_list = \
                        [ 'get_total_population_by_year'
                        , 'get_total_households_by_year'
                        , 'get_total_jobs_by_year'
                        , 'get_total_DUs_by_year'
                        , 'get_total_nonres_sqft_by_year'
                        , 'get_total_DUs_SF_by_year'
                        , 'get_total_DUs_MF_by_year'
                        , 'get_total_vacant_DUs_by_year'
                        , 'get_total_vacant_DUs_by_type_and_year'
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
                        ]
        
        # Add subarea query choices if subarea was specified
        if subarea <> '':
            report_list.extend(
                        [ 'get_total_jobs_by_year_and_subarea'
                        , 'get_total_households_by_year_and_subarea'
                        , 'get_total_population_by_year_and_subarea'
                        , 'get_total_DUs_by_year_and_subarea'
                        , 'get_total_nonres_sqft_by_year_and_subarea'
                        , 'get_total_vacant_DUs_by_year_and_subarea'
                        , 'get_total_DUs_MF_by_year_and_subarea'
                        , 'get_total_DUs_SF_by_year_and_subarea'
                        , 'get_total_households_in_SFR_by_year_and_subarea'
                        , 'get_total_households_in_MFR_by_year_and_subarea'
                        , 'get_total_population_in_SFR_by_year_and_subarea'
                        , 'get_total_population_in_MFR_by_year_and_subarea'
                        ]
                               )
        report_list.sort()
        
        # Open GUI
        choices = multchoicebox('Choose queries to run','Run Queries',report_list)
        if not choices: return
        
        # create report object:
        region_wide_report = RegionWideReport(workbook, years, connection, run_name, base_year)
        
        # Organize chosen queries into two lists
        region_wide_choices = []
        subarea_choices = []
        for choice in choices:
            if 'subarea' in choice:
                subarea_choices.append(choice)
            else:
                region_wide_choices.append(choice)
        
        # Run region wide queries
        for region_wide_choice in region_wide_choices:
            exec('region_wide_report.%s()' % region_wide_choice)
        # Run subarea queries
        for subarea_choice in subarea_choices:
            exec('%s(subarea, years, workbook, run_name, base_year, connection)' % subarea_choice)
        
        # Save excel workbook
        save_excel_workbook(run_name, excel_output_path, workbook)
        

if __name__ == "__main__":
    print 'Starting: Create Zone Simulation Report in Excel'
    # database connection variables   
    try:
        # get values as sys arguments
        username = sys.argv[1]
        password = sys.argv[2]
        server = sys.argv[3]
        database = sys.argv[4]
        # create the engine and connection
        engine = create_engine('mssql://%s:%s@%s/%s' % (username, password, server, database))
        connection = engine.connect()
        print 'SQL connection made to %s via command line arguments' % server
        main()
    except:
        # get values from gui
        db_connection_fields = ['Username','Password','Server Name','Database Name']
        db_connection_default_values = ['AZSMARTExport','thebigone','MAG1113','AZSMART_V3_zone']
        db_connection_values = multenterbox('','Enter values',db_connection_fields,db_connection_default_values)
        # create the engine and connection
        engine = create_engine('mssql://%s:%s@%s/%s' % (db_connection_values[0], db_connection_values[1], db_connection_values[2], db_connection_values[3]))
        connection = engine.connect()
        print 'SQL connection made to %s via GUI arguments' % db_connection_values[2]
        main()

#############################
########### NOTES ###########
#############################

    # REGION WIDE REPORTS
    # NOT WORKING AT ALL
    # region_wide_report.get_total_job_spaces_by_year()
    
    # SUBAREA REPORTS
    # NOT WORKING AT ALL
    #get_household_density_per_acre_by_subarea(subarea, years, workbook, run_name, base_year, connection)
    #get_vacant_job_spaces_by_subarea(subarea, years, workbook, run_name, base_year, connection)

# TODO:
# add a drop table if exists function
# some of these queries were designed to be run w/ a full simulation uploaded to SQL (every year) instead of
#      a partial run (e.g. 2005,2010,2015).  Generalization of the code to handle these cases would be good




