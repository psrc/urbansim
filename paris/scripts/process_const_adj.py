# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from pandas import read_csv, read_clipboard, DataFrame
from itertools import product
import numpy as np

coef = read_csv('establishment_location_choice_model_coefficients_B4Adj.csv')
const_raw = read_csv('elcm_const_raw2.txt', sep='\t')
s, e = 2, 12
coef_name, sub_model_id = list(zip(*product(const_raw['Name'], list(range(s, e)))))

df = DataFrame({'coefficient_name': coef_name, 'sub_model_id': sub_model_id})
df['adjustment'] = 0.0
for i in range(s, e): 
    df['adjustment'][df['sub_model_id']==i] = np.asarray(const_raw[str(i)], dtype='f4')

df.set_index(['sub_model_id', 'coefficient_name'], inplace=True)
coef = coef.rename(columns=lambda s: s.split(':')[0])
coef = coef.set_index(['sub_model_id', 'coefficient_name'], inplace=True)
coef.to_csv('elcm_org.csv', sep=',', header=True)
coef['estimate'] = coef['estimate'].add(df['adjustment'], fill_value=0.0)
coef.to_csv('establishment_location_choice_model_coefficients.csv', sep=',', header=True)

