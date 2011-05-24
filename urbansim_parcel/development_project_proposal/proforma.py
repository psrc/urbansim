# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
import numpy as np
from numpy import ma, zeros, arange, array, asarray
from numpy import float32, column_stack, asscalar

periods_per_year = 4
construction_loan_rate = 0.085 / periods_per_year
construction_loan_size = 0.50

ltv_max = 0.75
dcr_max = 1.25
perm_loan_rate = 0.075
perm_loan_term = 20 * periods_per_year  #period
discount_rate = 0.15
cap_rate = 0.07
max_periods_of_sale = 5 * periods_per_year
for_rent_seasoning_threshold = 4
perm_load_occupancy_threshold = 0.85

property_insurance = 1

class proforma(Variable):
    """
    Do the proforma calculation for the new new real estate model
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return ["property_tax = development_project_proposal.disaggregate(parcel.property_tax)",
                "land_cost = development_project_proposal.disaggregate(parcel.land_cost)",
                "sales_revenue = development_project_proposal.aggregate(development_project_proposal_component.sales_revenue)",
                "sales_revenue_per_period = development_project_proposal.aggregate(development_project_proposal_component.sales_absorption)",
                "rent_revenue = development_project_proposal.aggregate(development_project_proposal_component.rent_revenue)",
                "rent_revenue_per_period = safe_array_divide(development_project_proposal_component.rent_revenue, development_project_proposal_component.rent_absorption)",
                "rent_revenue_per_period = development_project_proposal.aggregate(development_project_proposal_component.rent_revenue_per_period)",
                "rent_vacancy_per_period = development_project_proposal.aggregate(development_project_proposal_component.rent_revenue_per_period * development_project_proposal_component.vacancy_rates)",
                "rent_operating_cost_per_period = development_project_proposal.aggregate(development_project_proposal_component.rent_revenue_per_period * development_project_proposal_component.operating_cost)",

                "leases_revenue = development_project_proposal.aggregate(development_project_proposal_component.leases_revenue)",
                "leases_revenue_per_period = safe_array_divide(development_project_proposal_component.leases_revenue, development_project_proposal_component.leases_absorption)",
                "leases_revenue_per_period = development_project_proposal.aggregate(development_project_proposal_component.leases_revenue_per_period)",
                "leases_vacancy_per_period = development_project_proposal.aggregate(development_project_proposal_component.leases_revenue_per_period * development_project_proposal_component.vacancy_rates)",
                "leases_operating_cost_per_period = development_project_proposal.aggregate(development_project_proposal_component.leases_revenue_per_period * development_project_proposal_component.operating_cost)",
                #"urbansim_parcel.development_project_proposal.existing_units",
                #"improvement_value=development_project_proposal.disaggregate(urbansim_parcel.parcel.improvement_value)",
                #"urbansim_parcel.development_project_proposal.land_area_taken",
                #"land_area=development_project_proposal.disaggregate(parcel.parcel_sqft)",
                ]

    def compute(self, dataset_pool):
        p = self.get_dataset()
        c = dataset_pool.get_dataset('development_project_proposal_component')
        max_periods = max_periods_of_sale + asscalar(p['sales_start_period'])
        revenues = zeros(max_periods)
        costs = zeros(max_periods)
        #cash_flow = zeros(max_periods)

        construction_loan_balance = p['construction_cost'] * construction_loan_size
        perm_loan_size = 0
        perm_loan_interest_payment = 0
        perm_loan_repayment = 0
        perm_loan_proceeds = 0.0

        full_rent_periods = 0
        sold_for_rent = 0
        component_sales_revenue = c['sales_revenue'].copy()
        component_rent_revenue = c['rent_revenue_per_period'].copy()
        component_leases_revenue = c['leases_revenue_per_period'].copy()
        construction_periods = p['sales_start_period'] - p['construction_start_period']
        
        for period in arange(max_periods)+1:
            
            if period == 1:
                land_equity = p['land_cost']
                costs[period] += land_equity            
            
            if period < p['sales_start_period']:
                #revenues
                public_contribution = 0 if p['public_contribution'] == 0 \
                                        else p['public_contribution'] / \
                                             float(construction_periods)
                
                sales_revenue = 0
                rent_revenue = 0 
                leases_revenue = 0
                revenues[period] += public_contribution

                #costs
                operating_cost = 0
                vacancy = 0
                tax = p['property_tax'] * p['land_cost']
                construction_equity = p['construction_cost'] * (1 - construction_loan_size) \
                        / (p['sales_start_period'] - 1)
                construction_loan_interest_payment = construction_loan_balance * construction_loan_rate
                construction_loan_repayment = revenues[period] \
                        if construction_loan_balance > revenues[period] \
                        else construction_loan_balance
                costs[period] += tax + construction_equity + \
                     construction_loan_interest_payment + construction_loan_repayment
                construction_loan_balance -= construction_loan_repayment
            else:
                if any(component_sales_revenue):
                    # TODO this would not work when we do proforma on multiple proposals at once
                    sales_revenue = np.min(column_stack((c['sales_absorption'],
                                                          component_sales_revenue)),
                                            axis=1
                                               ).sum()
                    component_sales_revenue -= c['sales_absorption']
                    np.clip(component_sales_revenue, 
                            0, component_sales_revenue.max(),
                            out=component_sales_revenue)
                else:
                    sales_revenue = 0
                
                # before reaching full occupancy for rent property
                if not sold_for_rent and any(component_rent_revenue <= c['rent_revenue']):
                    rent_revenue = np.min(column_stack((c['rent_revenue'],
                                                        component_rent_revenue)),
                                          axis=1
                                          )
                    operating_cost = (rent_revenue * c['operating_cost']).sum()
                    vacancy = (rent_revenue * c['vacancy_rates']).sum()
                    rent_revenue = rent_revenue.sum()                    
                    component_rent_revenue += c['rent_revenue_per_period']
                    np.clip(component_rent_revenue, 
                            0, c['rent_revenue'],
                            out=component_rent_revenue)
                    
                if not sold_for_rent and any(component_leases_revenue <= c['leases_revenue']):
                    leases_revenue = np.min(column_stack((c['leases_revenue'],
                                                          component_leases_revenue)),
                                            axis=1
                                            )
                    operating_cost += (leases_revenue * c['operating_cost']).sum()
                    vacancy += (leases_revenue * c['vacancy_rates']).sum()
                    leases_revenue = leases_revenue.sum()
                    component_leases_revenue += c['leases_revenue_per_period']
                    np.clip(component_leases_revenue, 
                            0, c['leases_revenue'],
                            out=component_leases_revenue)                    

                if component_rent_revenue.sum() >= c['rent_revenue'].sum() and \
                   component_leases_revenue.sum() >= c['leases_revenue'].sum():
                    full_rent_periods += 1
                    
                #revenues
                if not sold_for_rent:
                    revenues[period] += sales_revenue + rent_revenue + leases_revenue
                else:
                    revenues[period] = sales_revenue
                    if revenues[period] == 0:
                        break                

                #costs
                taxable_proportion = p['rent_sqft'] / p['total_sqft'].astype(float32)
                tax = p['property_tax'] * (p['land_cost'] + p['construction_cost']) * taxable_proportion
                insurance = p['rent_sqft'] * property_insurance
                construction_equity = 0
                construction_loan_interest_payment = construction_loan_balance * construction_loan_rate
                construction_loan_repayment = revenues[period] \
                        if construction_loan_balance > revenues[period] \
                        else construction_loan_balance
                
                #adjustment to revenues/costs
                for_rent_noi = rent_revenue + leases_revenue - tax - insurance - operating_cost - vacancy
                meets_perm_load_occupancy_threshold = rent_revenue + leases_revenue > \
                                                               ( p['rent_revenue'] + p['leases_revenue']) * \
                                                               perm_load_occupancy_threshold
                
                if perm_loan_size == 0 and \
                   for_rent_noi > 0 and \
                   meets_perm_load_occupancy_threshold:
                    perm_loan_size = min((for_rent_noi / cap_rate) * ltv_max,
                                          -np.pv(perm_loan_rate, 
                                                perm_loan_term, 
                                                for_rent_noi / dcr_max)
                                       )
                    perm_loan_proceeds = perm_loan_size
                    revenues[period] += perm_loan_proceeds

                if perm_loan_size > 0:
                    perm_loan_interest_payment = -np.pmt(perm_loan_rate, perm_loan_term, perm_loan_size)
                
                if not sold_for_rent:
                    costs[period] += tax + insurance + operating_cost + vacancy + \
                            construction_loan_interest_payment + construction_loan_repayment + \
                            perm_loan_interest_payment
                else:
                    costs[period] = 0
                
                construction_loan_balance -= construction_loan_repayment
                    
                if full_rent_periods > for_rent_seasoning_threshold and \
                   not sold_for_rent:
                    #sell_for_rent = 1
                    perm_loan_repayment = perm_loan_size
                    for_rent_sale = for_rent_noi / cap_rate
                    revenues[period] += for_rent_sale
                    costs[period] += perm_loan_repayment
                    sold_for_rent = 1
                    #break

        cash_flow = (revenues - costs)[1:period]
        npv = np.npv(discount_rate, cash_flow)
        irr = np.irr(cash_flow)

        return asarray(npv)
    
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            
            'parcel':
            {
                "parcel_id":        array([1]),
                "property_tax":     array([0.01]),
                "land_cost":        array([ 5]) * 1000000, #Land + other equity                
                 
            },
            
            'development_project_proposal_component':
            {
                "proposal_component_id": array([1,  2,  3,  4,  5]),
                "proposal_id":           array([1,  1,  1,  1,  1]),
           "building_type_id":           array([1,  1,  1,  1,  5]),  #Single Family, Single Family builder, Condo
                   "bedrooms":           array([1,  2,  3,  4,  0]),
                   "sales_revenue":      array([2,  3,  4,  5,  0]) * 1000000, #total
                "sales_absorption":    array([.25,0.3,0.35,0.4,  0]) * 1000000, #per period
                    "rent_revenue":    array([ .1,0.2,0.3,0.4,  0]) * 1000000, #per period
                  "rent_absorption":   array([  8,  4,  4,  8,  8]),
                 "leases_revenue":      array([  0,  0,  0,  0,  4]) * 1000000, #per period
                  "leases_absorption":  array([  0,  0,  0,  0,  8]),                   
              "vacancy_rates":         array([ 1.0, 0.5, 0.25, 1.0,  0.6]) / 12,
             "operating_cost":         array([0.2,0.2,0.2,0.2, 0.1]),
             },
            'development_project_proposal':
            {
             
                "proposal_id":array([1]),
                  "parcel_id":array([1]),
  "construction_start_period":array([ 1]),           #construction start date                  
     "sales_start_period":    array([ 5]),           #Sales/Rent start date
     "rent_sqft":             array([ 75]) * 1000,
     "total_sqft":            array([ 75]) * 1000,  #TODO:fake it so that it pays taxes on all portions
     "construction_cost":     array([ 30]) * 1000000,
     "public_contribution":   array([ 0.0]),
            },
            
            }
        )
        
        should_be = array([-4938532.5]) #array([-5116654.78223655])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)

    def test_visitacion(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            
            'parcel':
            {
                "parcel_id":        array([1]),
                "property_tax":     array([0.01]),
                #"land_cost":        array([ 5]) * 1000000, #Land + other equity
                "land_cost":        array([ 100000]), #Land + other equity                                
                 
            },
            
            'development_project_proposal_component':
            {
                "proposal_component_id": array([1,  2,  3,  4,  5]),
                "proposal_id":           array([1,  1,  1,  1,  1]),
           "building_type_id":           array([1,  1,  1,  1,  5]),  #Condo, non-residential
                   "bedrooms":           array([1,  2,  3,  4,  0]),
                   "sales_revenue":      array([0,  374800000,  0,  0,  0]), #total
                "sales_absorption":      array([0,   26000000,  0,  0,  0]), #per period
                    "rent_revenue":      array([0,    1173750,  0,  0,  0], dtype='f'), #per period
                  "rent_absorption":   array([  0,          4,  0,  0,  0]),
                 "leases_revenue":      array([  0,  0,  0,  0,  468563], dtype='f'), #per period
                  "leases_absorption":  array([  0,  0,  0,  0,  12], dtype='f'),                   
              "vacancy_rates":         array([ 1.0, 0.5, 0.25, 1.0,  0.6]) / 12,
             "operating_cost":         array([0.2,0.2,0.2,0.2, 0.1]),
             },
            'development_project_proposal':
            {
             
                "proposal_id":array([1]),
                  "parcel_id":array([1]),
  "construction_start_period":array([ 1]),           #construction start date                                    
     "sales_start_period":    array([10]),           #Sales/Rent start date
     "rent_sqft":             array([  375600 ]),
     "total_sqft":            array([  1620000]),
     "construction_cost":     array([ 448293833 ]),
     "public_contribution":   array([ 365000000.0]),     
            },
            
            }
        )
        
        should_be = array([-40036575])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)
        
if __name__=='__main__':
    opus_unittest.main()
    
