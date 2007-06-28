DATA PREPARATION
================
Process: 

I.   Create a 'jobs' table from a table of businesses
II.  Create new buildings to accommodate all households
III. Assign buildings to households
IV.  Assign buildings to jobs

I.
****
1. Run the script unroll_jobs_from_establishments.py
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to MysqlStorage (where the business table lives),
                 outstorage set to FltStorage (where your cache data is)
  - The script creates a 'jobs' table and writes it out into the outstorage.
           
II.
****
Buildings:
----------
1. Run a development location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_buildings

2. Copy the resulting 'buildings' table to your cache directory (replace the existing one).

3. Export the 'buildings' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t buildings -d database_name
  
III.
****
Households:
-----------
1. Run a household location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_households
  
2. Copy the resulting 'households' table to your cache directory (replace the existing one).

3. Export the 'households' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t households -d database_name

IV.
****
Jobs:
-----
Note: We assume that the 'jobs' table have already assigned buildings from one-building parcels.
  
1. Run the script assign_bldgs_to_jobs_when_multiple_bldgs_in_parcel.py
    (see the script for a description of the algorithm)
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to FltStorage (where your 'jobs' table is, e.g. the cache directory),
                 pool_storage set equal to instorage (where all your data is cached), 
                 outstorage set to FltStorage (some other directory)
    (Note: it also needs the table "building_sqft_per_job" on instorage, so one needs to cache it
    prior to running this script, if the instorage is Flt)
  - The script assigns building_id to jobs where possible and writes out the 'jobs' table into the outstorage.
  - It also imputes non_residential_sqft to buildings where needed and writes out the 'buildings' table 
      into the outstorage.
  
2. Copy the 'jobs' and 'buildings' tables into your cache directory (replace the existing ones).

3. Estimate coefficients for home_based and non_home_based ELCM, using 
   psrc_parcel/estimation/run_estimation.py
  - Uncomment the appropriate model in __main__
  - Set the appropriate cache directory in my_estimation_config.py

4. Run the employment location choice model with the estimated coefficients in order to assign buildings 
   to the remaining jobs.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_jobs

5. Copy the resulting 'jobs' table to your cache directory (replace the existing one).

6. Export the 'jobs' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t jobs -d database_name. 

  
  
  