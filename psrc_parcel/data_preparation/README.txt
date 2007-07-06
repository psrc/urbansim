DATA PREPARATION
================
Process: 

I.   Create a 'jobs' table from a table of businesses
II.  Create new residential buildings to accommodate all households
III. Assign buildings to households
IV.  Assign buildings to jobs with known parcel_id
V.   Create new non-residential buildings to accommodate all jobs
VI.  Assign buildings to remaining jobs

I. Create a 'jobs' table
****
1. Run the script unroll_jobs_from_establishments.py
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to MysqlStorage (where the business table lives),
                 outstorage set to FltStorage (where your cache data is)
  - The script creates a 'jobs' table and writes it out into the outstorage.
           
II. Create new residential buildings
****
1. Run a development location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_buildings_residential

2. Copy the resulting 'buildings' table to your cache directory (replace the existing one).

Note: The procedure in Step 1. includes creating a proposal set which can be very time consuming. 
      If you pass the point where the proposal set is created and need to re-run the step, do the following:
      - copy the directory 'development_project_proposals' from the simulation directory to your baseyear cache
      - modify config_buildings_residential.py as follows:
          * add 'development_project_proposal': {} to the 'datasets_to_preload' entry
          * if you need to also re-run the Development Project Proposal Regression Model,
            uncomment the line 
            self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["create_proposal_set"] = False
          * otherwise, comment out the entry "expected_sale_price_model" in "models" 
           (make sure the development_project_proposals directory in your baseyear cache has the attribute 'unit_price_expected',
            which is the result of the eliminated model)
      - if you want to re-run the development sampling model starting with the zone where your previous run ended,
        make sure that the development_project_proposals directory in your baseyear cache has the most recent version 
        of the attribute 'status_id' (the model flushes the dataset every 10 zones into the simulation directory).
      - invoke the start_run.py command (Step 1.) again
  
III. Assign buildings to households
****
1. Run a household location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_households
  
2. Copy the resulting 'households' table to your cache directory (replace the existing one).

3. Export the 'households' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t households -d database_name

IV. Assign buildings to jobs with known parcel_id
****
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
  
V. Create new non-residential buildings
****
1. Run a development location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_buildings_non_residential

2. Copy the resulting 'buildings' table to your cache directory (replace the existing one).

3. Export the 'buildings' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t buildings -d database_name
  
VI.  Assign buildings to remaining jobs
****
1. Estimate coefficients for home_based and non_home_based ELCM, using 
   psrc_parcel/estimation/run_estimation.py
  - Uncomment the appropriate model in __main__
  - Set the appropriate cache directory in my_estimation_config.py

2. Run the employment location choice model with the estimated coefficients in order to assign buildings 
   to the remaining jobs.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_jobs

3. Copy the resulting 'jobs' table to your cache directory (replace the existing one).

4. Export the 'jobs' table to the database.
  - Use: opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t jobs -d database_name.