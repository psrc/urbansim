# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

"""size  class  of  the  establishment the  total  number  of  employees  working  in  the 
establishment 
worforce: W2, W3, W6, W10, W20, W50, W100 workforce 
slopes: W3slope W6slope W10slope W20slope W50slope W100slope (2, 3-5, 6-9, 10-19, 
20-49, 50-99, 100+) in each establishment 
"""

bins = [2, 3, 6, 10, 20, 50, 100]
bins_str = [str(i) for i in bins]
bin_pre = None
bin_var = 'establishment.employment_lag1'
lower_bound = ['(%s >= %s)' % (bin_var, bin) for bin in bins]
upper_bound = ['(%s < %s)' % (bin_var, bin) for bin in bins[1:]] + ['']
vars = []
for bin, l, u in zip(bins_str, lower_bound, upper_bound):
    w = 'w%s=%s*%s' % (bin, l, u)
    vars.append( w.strip('*') )
    wslope = 'w%sslope=paris.establishment.w%s*(%s - %s)' % (bin, bin, bin_var, bin)
    vars.append( wslope )

aliases = vars + [
        "dept_id = establishment.disaggregate(building.dept)",
        "insee = establishment.disaggregate(zone.insee, intermediates=[building])",
        "LaDef = numpy.setmember1d(establishment.insee, (92050, 92026, 92062))",
        "CVilNouvel = numpy.setmember1d(establishment.insee, (92050, 92026, 92062))",
        "rmse_ln_emp_ratio = numpy.sqrt(establishment.disaggregate(sector.aggregate(establishment._init_error_ln_emp_ratio**2, function=mean)))",
        "emp_250 = (establishment.employment < 250).astype('i')"
           ]
