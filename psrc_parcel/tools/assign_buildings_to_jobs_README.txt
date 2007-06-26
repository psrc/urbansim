JOB DATA PREPARATION
====================
Starting from a business table that have assigned buildings only from one-building parcels, the following step
should be done in order to assign buildings to the remaining jobs:

1. Run the script unroll_jobs_from_establishments.py
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to MysqlStorage (where the business table lives),
          outstorage set to FltStorage (where your cache data is)
  - The script creates a 'jobs' table and writes it out into the outstorage.
  
2. Run the script assign_bldgs_to_jobs_when_multiple_bldgs_in_parcel.py
  (see the script for a description of the algorithm)
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to FltStorage (where your 'jobs' table is),
          pool_storage set equal to instorage (where all your data is cached), 
          outstorage set to FltStorage (some other directory)
    (Note: it also needs the table "building_sqft_per_job" on instorage, so one needs to cache it
    prior to running this script, if the instorage is Flt)
  - The script assigns building_id to jobs where possible and writes out the table into the outstorage.
  - It also imputes non_residential_sqft to buildings where needed and writes out the buildings table 
      into the outstorage.
  
3. Estimate coefficients for home_based and non_home_based ELCM, using 
  psrc_parcel/estimation/run_estimation.py
  - Uncomment the appropriate model in __main__
  - Set the appropriate cache directory in my_estimation_config.py

4. Run a simulation with estimated coefficients in order to assign buildings to the remaining jobs.
  - Prior to this, copy the resulting tables from step 2. (jobs, buildings) into your cache_directory.
  - Use start_run.py with the configuration psrc_parce.configs.data_preparation (not tested yet)

5. Export the resulting jobs table from the simulation cache into database,
  using opus_core/tools/do_export_cache_to_mysql_database.py with the -t option.
  
  
  