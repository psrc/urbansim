#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
        # aggregate sector job totals:
        "number_of_jobs = tazi03.number_of_agents(job)",
        "number_of_public_jobs = tazi03.aggregate(job.sector_id==21)+tazi03.aggregate(job.sector_id==22)",
        "number_of_industrial_jobs = tazi03.aggregate(job.sector_id==2)+tazi03.aggregate(job.sector_id==5)+tazi03.aggregate(job.sector_id==6)+tazi03.aggregate(job.sector_id==8)",
        "number_of_entertainment_jobs = tazi03.aggregate(job.sector_id==7)+tazi03.aggregate(job.sector_id==18)+tazi03.aggregate(job.sector_id==19)",
        "number_of_homebased_jobs = tazi03.aggregate(job.home_based==1)",
        # individual sector job totals:
        "number_of_agricultural_jobs = tazi03.aggregate(job.sector_id==1)",
        "number_of_mining_jobs = tazi03.aggregate(job.sector_id==2)",
        "number_of_utilities_jobs = tazi03.aggregate(job.sector_id==3)",
        "number_of_construction_jobs = tazi03.aggregate(job.sector_id==4)",
        "number_of_manufacturing_jobs = tazi03.aggregate(job.sector_id==5)",
        "number_of_wholesale_jobs = tazi03.aggregate(job.sector_id==6)",
        "number_of_retail_jobs = tazi03.aggregate(job.sector_id==7)",
        "number_of_transportation_jobs = tazi03.aggregate(job.sector_id==8)",
        "number_of_information_jobs = tazi03.aggregate(job.sector_id==9)",
        "number_of_finance_jobs = tazi03.aggregate(job.sector_id==10)",
        "number_of_realestate_jobs = tazi03.aggregate(job.sector_id==11)",
        "number_of_professional_jobs = tazi03.aggregate(job.sector_id==12)",
        "number_of_healthcare_jobs = tazi03.aggregate(job.sector_id==16)",
        "number_of_accomodation_jobs = tazi03.aggregate(job.sector_id==18)",
        "number_of_foodservice_jobs = tazi03.aggregate(job.sector_id==19)",
        "number_of_pubfedstate_jobs = tazi03.aggregate(job.sector_id==21)",
        "number_of_publocal_jobs = tazi03.aggregate(job.sector_id==22)",
        # population and household totals:
        "number_of_households = tazi03.number_of_agents(household)",
        "number_of_pop = tazi03.number_of_agents(person)",
        "number_of_children = tazi03.aggregate(where(person.age < 17, 1,0))",        
        # specific population totals:
        "number_of_persons_with_at_least_high_school_diploma = tazi03.aggregate(mag_zone.person.at_least_high_school_diploma)",
        "number_of_persons_with_at_least_bachelors_degree = tazi03.aggregate(mag_zone.person.at_least_bachelors_degree)",        
        "number_of_office_jobs = tazi03.aggregate(job.sector_id == 9) + tazi03.aggregate(job.sector_id == 10) + tazi03.aggregate(job.sector_id == 11) + tazi03.aggregate(job.sector_id == 13)",
        
           ]

