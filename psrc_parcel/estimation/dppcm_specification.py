# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

all_variables = []
specification = {}

specification = {
    #"_definition_": all_variables,                               
    
    -2:{
        "equation_ids":(1, 2),  # 1:accepted; 2:unaccepted
        "constant":(0, "beta2_asc"),
        #"urbansim_parcel.development_project_proposal.unit_price_expected":("beta1_price", 0),
        #"urbansim_parcel.development_project_proposal.total_revenue":("beta1_revenue",0),
        #"urbansim_parcel.development_project_proposal.acquisition_cost":("beta1_acqcost",0),
        #"urbansim_parcel.development_project_proposal.demolition_cost":("beta1_demcost",0),
        #"urbansim_parcel.development_project_proposal.construction_cost":("beta1_concost",0),
        #"urbansim_parcel.development_project_proposal.total_investment":("beta1_totcost",0),
        "urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment":("beta1_roi",0),


        #"constant+0.0132":(0, "beta2_asc"),
        #"person.disaggregate(household.persons)":("beta1_hhsize", 0),
        #"person.disaggregate(household.children > 0)":("beta1_haschild", 0),
        #"income=person.disaggregate(household.income)":("beta1_income", 0),
        #"kemp30m=person.disaggregate(urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone, intermediates=[household])/1000":(0, "beta2_kemp30m"),
        #"hlogsum=person.disaggregate(psrc_parcel.household.trip_weighted_average_logsum_hbw_am_from_residence)":(0, "beta2_hlogsum"),        
        #"plogsum1=person.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_1, intermediates=[household])":(0, "beta2_logsum1"),        
        #"plogsum2=person.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_2, intermediates=[household])":(0, "beta2_logsum2"),        
        #"plogsum3=person.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_3, intermediates=[household])":(0, "beta2_logsum3"),        
        #"plogsum4=person.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_4, intermediates=[household])":(0, "beta2_logsum4"),        
        #"age3=person.disaggregate(urbansim_parcel.household.persons_with_age_le_3>0)":("beta1_age3", 0),
        #"age6=person.disaggregate(urbansim_parcel.household.persons_with_age_le_6>0)":("beta1_age6", 0),
        #"age13=person.disaggregate(urbansim_parcel.household.persons_with_age_le_13>0)":("beta1_age13", 0),
        #"age16=person.disaggregate(urbansim_parcel.household.persons_with_age_le_16>0)":("beta1_age16", 0),
        #"age18=person.disaggregate(urbansim_parcel.household.persons_with_age_le_18>0)":("beta1_age18", 0),        
        #"person.disaggregate(household.workers-1)":("beta1_workers", 0),
        #"person.age":("beta1_age", 0),
        #"person.edu":("beta1_edu", 0),
        #"parttime=person.employment_status==2":("beta1_parttm", 0), ##part time worker
    }

}
