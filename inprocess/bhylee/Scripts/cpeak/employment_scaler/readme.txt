This set of two scripts provides a way to (very simply) model employment growth in 
sectors which don't necessarily allocate jobs by participating in the real estate
market in the same way that most private sector employers do.  This algorithm simply 
allocates jobs to cells which previously had jobs in them, and does so in proportion 
to the distribution of previously-existing jobs.  

The employment_scaler can be run through the scaler_entry_point.py script.  
The user can specify the years on which to run the scaler by specifying the range in 
the variable "years", and can also adjust the sectors to scale by adjusting the 
range in the variable "sectors".  

NOTE: This script was written solely as a first draft, or specification for an algorithm
to be improved upon later.  At the time of this writing, it runs VERY slowly due to a
dependence on queries made against the database.  