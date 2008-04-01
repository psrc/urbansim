###############
# Algorithm: 
# Get count of jobs in sector S to be placed on gridcells
# For each job j:
#    randomly select a job of sector S from jobs table
#    assign j to this gridcell
###############

import mdbi, os

class EmploymentScaler:
    

    ##############
    # Connect to a baseyear database
    #
    def __init__(self, database):
        
        self.db = mdbi.DbConnection(db = database,
                            hostname = os.environ['MYSQLHOSTNAME'],
                            username = os.environ['MYSQLUSERNAME'],
                            password = os.environ['MYSQLPASSWORD'])
               
                                 
    ##############
    # Get count of jobs in sector S to be placed on gridcells
    #    
    def GetJobsToAdd( self, year, sector_id ):
        
        target_year_jobs = self.db.GetResultsFromQuery("""select total_employment 
                from annual_employment_control_totals
                where year =  %i and
                sector_id = %i""" % (year, sector_id))
        
        starting_year = year - 1

        starting_year_jobs = self.db.GetResultsFromQuery("""select total_employment 
                from annual_employment_control_totals
                where year = %i and
                sector_id = %i""" % (starting_year, sector_id))
        
        self.jobs_to_add = target_year_jobs[1][0] - starting_year_jobs[1][0]
        print "total jobs to add: " + str(self.jobs_to_add)
        
    #################
    # Grow (scale) the jobs in a sector
    #    
    def Scale( self, sector_id ):
        # Get the max pre-existing job_id
        self.GetMaxJobID()
        
        for job in range(1,self.jobs_to_add):
            new_grid_id_list = self.db.GetResultsFromQuery("""select grid_id from jobs
                            where sector_id = %i order by rand() 
                            limit 1""" % sector_id)
            new_grid_id = new_grid_id_list[1][0]
            self.db.DoQuery("""INSERT INTO jobs (job_id, grid_id, sector_id, home_based)
                            values (%i, %i, %i, 0)""" % (self.max_job_id, new_grid_id, sector_id))
            print "assigning job " + str(self.max_job_id + 1) + " to gridcell " + str(new_grid_id)
            self.max_job_id = self.max_job_id + 1
            
            
    ################
    # Get the maximum job id
    #
    def GetMaxJobID(self):
        
        query_result = self.db.GetResultsFromQuery("select max(job_id) from jobs")
        
        self.max_job_id = query_result[1][0]
        print "max_job_id = "+ str(self.max_job_id)
        
        