import sys
import os
sys.path.append(os.path.join(sys.path[0], r'..\..\..\Estimation\Library'))
import mdbi

print "beginning jobs_for_estimation table"

obs_per_sector = 5000

db_con = mdbi.DbConnection(db = 'PSRC_jobs_for_estimation_creation',
                           hostname = 'trondheim.cs.washington.edu',
                           username = 'urbansim',
                           password = 'UrbAnsIm4Us')


# Get the sectors
sector_table = db_con.GetResultsFromQuery("select sector_id from PSRC_2000_baseyear.employment_sectors")
sectors = []
for rec in sector_table[1:]:
    sectors.append(rec[0])


db_con.DoQuery('drop table if exists jobs_for_estimation')
db_con.DoQuery("""CREATE TABLE jobs_for_estimation
    (job_id INT, grid_id INT, sector_id INT, home_based TINYINT)""")

    

for sector in sectors:
    
    qry = """INSERT INTO jobs_for_estimation (job_id, grid_id, sector_id, home_based)
        select job_id, grid_id, sector_id, home_based from jobs_for_estimation_primary 
        where sector_id = """ + str(sector) + """
        order by rand()
        limit """ + str(obs_per_sector)
    db_con.DoQuery(qry)
   
   
print "jobs_for_estimation table completed."
