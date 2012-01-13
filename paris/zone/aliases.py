# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

package = 'paris'
dataset = 'zone'
sectors = range(1, 12)
var_template = "employees_of_sector{0}={dataset}.aggregate(establishment.employees * (establishment.sector_id=={0}))"
vars = [var_template.format(sector, package=package, dataset=dataset) for sector in sectors] 
var_lag_template = "{package}.{dataset}.employees_of_sector{0}_lag4"
vars += [var_lag_template.format(sector, package=package, dataset=dataset) for sector in sectors] 
var_lndiff_template = "ln_bounded(numpy.abs({package}.{dataset}.employees_of_sector{0} - {package}.{dataset}.employees_of_sector{0}_lag4))"
vars += [var_lndiff_template.format(sector, package=package, dataset=dataset) for sector in sectors] 

aliases = vars + [
        "LaDef = numpy.setmember1d(establishment.insee, (92050, 92026, 92062))",
        "CVilNouvel = numpy.setmember1d(establishment.insee, (92050, 92026, 92062))",
        "limit = numpy.setmember1d(establishment.insee, (92050, 92026, 92062))",

        "CLSuperf = ln(zone.careakm2)",
        "Cpop9 = zone.aggregate(household.size)",
        "Cdensity = paris.zone.Cpop9 / zone.careakm2",
        "households = zone.number_of_agents(household)",
        "Cyoung = safe_array_divide(zone.aggregate(household.age_of_head <= 35), paris.zone.households)",
        "Cmedium = safe_array_divide(zone.aggregate(numpy.logical_and(household.age_of_head > 35, household.age_of_head<=55)), paris.zone.households)",
        "Cchild11_m = safe_array_divide(zone.aggregate(household.children11 > 0), paris.zone.households)",

        "CLEmpTot = ln(zone.aggregate(establishment.employees))",
           ]
