# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import sys, os
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory

# get path as program argument
path = sys.argv[1].__str__() # path looks like this: '/Users/thomas/Development/opus_home/data/psrc_parcel/base_year_data_re-estimate/2000/'
output_folder = None
if len(sys.argv) > 2:
    output_folder = sys.argv[2].__str__()

# init storage using path reference
storage = StorageFactory().get_storage('flt_storage', storage_location = path)
# coefficients of following models are printed out
models = ['real_estate_price_model_coefficients', 'household_location_choice_model_coefficients', 'non_home_based_employment_location_choice_model_coefficients', 'home_based_employment_location_choice_model_coefficients', 'work_at_home_choice_model_coefficients', 'workplace_choice_model_for_resident_coefficients' ]

content_coefficients = ''   # contains whole content for coefficients
content_specification = ''  # contains whole content for specifications

# go trough all models ...
for m in range(len(models)):
    
    model = models[m]
    
    content_coefficients+='\n\r'    
    content_coefficients+='Model: %s\n\r' %model
    
    # ... get their coefficients ...
    coefficients = Coefficients(in_storage=storage)
    coefficients.load(resources=None, in_storage=storage, in_table_name=model)
    
    # ... prepare for printing ...
    names = coefficients.names
    estimates = coefficients.values
    std_errors = coefficients.standard_errors
    sub_ids = coefficients.submodels
    t_stats = coefficients.other_measures['t_statistic']

    # ... finally print out all available data 
    content_coefficients+='{0:40s} {1:10s} {2:10s} {3:10s} {4:10s}\n\r'.format('coefficient_name', 'estimate', 'error', 'submodel_id', 't_statistic')
    for i in range(len(names)):
        if len(sub_ids) <= 0:
            content_coefficients+='{0:40s} {1:10f} {2:10f} {3:10s} {4:10f}\n'.format(names[i], estimates[i], std_errors[i], '-', t_stats[i])#'{0:30s} {1:10f} {2:10f} {3:10s} {4:10f}\n'.format(names[i], estimates[i], std_errors[i], '-', t_stats[i])
        else:            
            content_coefficients+='{0:40s} {1:10f} {2:10f} {3:10s} {4:10f}\n'.format(names[i], estimates[i], std_errors[i], sub_ids[i], t_stats[i]) #'{0:30s} {1:10f} {2:10f} {3:10s} {4:10f}\n'.format(names[i], estimates[i], std_errors[i], sub_ids[i], t_stats[i])
    content_coefficients+='\n\r'
    
    # now do the same for the specification ...
    
    model = model.replace('coefficients', 'specification')
    
    content_specification+='\n\r'  
    content_specification+='Model: %s\n\r' %model
    
    # get model specification ...
    specification = EquationSpecification(in_storage=storage)
    specification.load(in_table_name=model)
    
    # store specification directly as csv
    #from opus_core.store.csv_storage import csv_storage
    #out_path = os.path.join(path, model)
    #out_storage = csv_storage(storage_location = out_path)
    #specification.write(out_storage=out_storage, out_table_name=model) # writes out specifications as csv file
    
    # ... prepare for printing ...
    names_spec = specification.get_coefficient_names()
    submodels_spec = specification.get_submodels()
    long_var_names_spec = specification.get_long_variable_names()
    
    # ... finally print out all available data 
    content_specification+='{0:40s} {1:10s} {2:20s}\n\r'.format('coefficient_name', 'submodel_id', 'variable_name')
    for x in range(len(names_spec)):
        if len(submodels_spec) <= 0:
            content_specification+='{0:40s} {1:10s} {2:20s}\n'.format(names_spec[x], '-', long_var_names_spec[x])
        else:
            content_specification+='{0:40s} {1:10s} {2:20s}\n'.format(names_spec[x], submodels_spec[x], long_var_names_spec[x]) #'{0:30s} {1:10s} {2:20s}\n'.format(names_spec[x], submodels_spec[x], long_var_names_spec[x])
    content_specification+='\n\r'
    
# print and store coefficients
print content_coefficients
print ''

output_dir = ''
if output_folder == None:
    output_dir = path
else:
    if not os.path.exists(output_folder):
        try: os.mkdir( output_folder )
        except: pass
    output_dir = output_folder
    
content_path = os.path.join(output_dir, 'coefficients.txt')
print '...dumping content_coefficients into %s' %content_path
f = open(content_path, 'w')
f.write(content_coefficients)
f.flush()
f.close()

# print and store specification
print content_coefficients
print ''

content_path = os.path.join(output_dir, 'specifications.txt')
print '...dumping content_specifications into %s' %content_path
f = open(content_path, 'w')
f.write(content_specification)
f.flush()
f.close()