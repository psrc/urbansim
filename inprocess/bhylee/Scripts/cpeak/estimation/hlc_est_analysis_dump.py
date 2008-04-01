import sys
import os
print os.path.join(sys.path[0], r'..\..\..\Estimation\Library')
sys.path.append(os.path.join(sys.path[0], r'..\..\..\Estimation\Library'))
import mdbi

myDB = mdbi.DbConnection(db = 'PSRC_baseyear_hlc_est_sungyop',
                         hostname = os.environ['MYSQLHOSTNAME'],
                         username = os.environ['MYSQLUSERNAME'],
                         password = os.environ['MYSQLPASSWORD'])

for table in ['fazdist_chosen_vs_maxprobs',                 
              'fazdist_chosen_vs_montecarlo',               
              'fazdist_chosen_vs_prob_sums',                
              'fazdist_matrix_prediction_maxprob',          
              'fazdist_matrix_prediction_montecarlo',       
              'fazdist_matrix_probability',                
              'fazdist_pct_matrix_prediction_maxprob',      
              'fazdist_pct_matrix_prediction_montecarlo',  
              'fazdist_pct_matrix_probability']:
      
    results = myDB.GetResultsFromQuery('select * from %s' % table)
    data = results[1:]
    
    mdbi.RsToCsv(recset = data,
                 wd = r'R:\Projects\PSRC\Estimation\HouseLocChoice\estimation_results\Fazdist_summaries',
                 filename = table)