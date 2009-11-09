DATA PREPARATION
================
Automated process:

I.   Create a 'jobs' table from a table of businesses and 'building_sqft_per_job' table
****
Run the script unroll_jobs_from_establishments.py
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to MysqlStorage (where the business table lives),
                 outstorage set to FltStorage (where your cache data is; must contain the 'buildings' table)
  - The script creates a 'jobs' table by unrolling the business table, removes jobs with non-existing buildings, 
    and writes the 'jobs' table out into the outstorage.
  - In addition, the scripts creates a 'building_sqft_per_job' table from the existing jobs 
    and writes it out into the outstorage.
    
II.
****
Run 
python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_data_preparation
(update 'cache_directory_root' and 'existing_cache_to_copy' to your local environment)

This runs a simulation for 5 years (2001-2005), in each year processing one step of the data preparation process.
See the description of the steps in the section below. Thus, the final results are stored in year 2005 of the 
simulation cache.
If the process fails before completing the fifth year, proceed with the manual processing.

III. Post-process
****
Attributes that define higher-level geography should be deleted from 
datasets in the cache directory in order not to be treated as primary attributes,
and thus being re-computed from lower-level geography.
These are:
parcel_id, zone_id in households (will be re-computed from building_id)
parcel_id, zone_id in jobs (will be re-computed from building_id)
zone_id in buildings (will be re-computed from parcel_id)

IV. Exporting resulting tables to database
****
Export the following tables from your simulation cache to the database: 'households', 'buildings', 'jobs', 
'building_sqft_per_job'
  - For each table use:
    python opus_core/tools/do_export_cache_to_mysql_database.py -c your_cache_directory/year -t table_name -d database_name
    
    
---------------------------------------------------------------------------------------------------------------------------
Manual Process: 

I.   Create a 'jobs' table from a table of businesses
II.  Create new residential buildings to accommodate all households
III. Assign buildings to households
IV.  Assign buildings to jobs with known parcel_id
V.   Create new non-residential buildings to accommodate all jobs
VI.  Assign buildings to remaining jobs
VII. Post-process
VIII.Exporting resulting tables to database

Note: Make sure that buildings built after 2000 are removed.

I. Create a 'jobs' table and 'building_sqft_per_job' table
****
See Step I. in the automated process above.
           
II. Create new residential buildings
****
1. Run a development location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_buildings_residential
    (update 'cache_directory_root' and 'existing_cache_to_copy' to your local environment)

2. Copy the resulting 'buildings' table to your cache directory (replace the existing one).
   IMPORTANT: delete the attribute/file 'building_sqft.li4' (if it exists)! This is a computed attribute
   and must be recomputed.
   
3. Copy the attribute parcels/unit_price from the simulation directory into the parcels subdirectory of your cache.

Note: The procedure in Step 1. includes creating a proposal set which can be very time consuming. 
      If you pass the point where the proposal set is created and need to re-run the step, do the following:
      - copy the directory 'development_project_proposals' from the simulation directory to your baseyear cache
      - modify config_buildings_residential.py as follows:
          * add 'development_project_proposal': {} to the 'datasets_to_preload' entry
          * comment out entry 'real_estate_price_model' in "models". Copy the attribute parcels/unit_price 
            from the simulation directory into the parcels subdirectory of your cache.
          * if you need to also re-run the Development Project Proposal Regression Model,
            uncomment the line 
            self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["create_proposal_set"] = False
          * otherwise, comment out the entry "expected_sale_price_model" in "models" 
           (make sure the development_project_proposals directory in your baseyear cache has the attribute 'unit_price_expected',
            which is the result of the eliminated model)
      - If you want to re-run the development sampling model starting with the zone where your previous run ended,
        make sure that the development_project_proposals directory in your baseyear cache has the most recent version 
        of the attribute 'status_id' (the model flushes the dataset every 50 zones into the simulation directory).
      - If you want to re-run only the building construction model, leave only this model uncommented in "models", 
        and again, make sure that the development_project_proposals directory in your baseyear cache has the most 
        recent version of the attribute 'status_id' (updating this attribute is the result of the development sampling model).
      - invoke the start_run.py command (Step 1.) again
      - IMPORTANT CLEANUP: Delete the directory 'development_project_proposals' from your baseyear cache directory.
  
III. Assign buildings to households
****
1. Run a household location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_households
    (update 'cache_directory_root' and 'existing_cache_to_copy' to your local environment)
  
2. Copy the resulting 'households' table to your cache directory (replace the existing one).

IV. Assign buildings to jobs with known parcel_id
****
Note: We assume that the 'jobs' table have already assigned buildings from one-building parcels.
  
1. Run the script assign_bldgs_to_jobs_when_multiple_bldgs_in_parcel.py
    (see the script for a description of the algorithm)
  - choose appropriate settings in the __main__ part
  - recommended: instorage set to FltStorage (where your 'jobs' table is, e.g. the cache directory),
                 pool_storage set equal to instorage (where all your data is cached), 
                 outstorage set to FltStorage (some other directory)
  - The script assigns building_id to jobs where possible and writes out the 'jobs' table into the outstorage.
  - It also imputes non_residential_sqft to buildings where needed and writes out the 'buildings' table 
      into the outstorage.
  - It modifies the table 'building_sqft_per_job' and writes it out into outstorage.
  
2. Copy the 'jobs', 'buildings' and 'building_sqft_per_job' tables from outstorage into your cache directory 
   (replace the existing ones).
  
V. Create new non-residential buildings
****
1. Run a development location choice model.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_buildings_non_residential
    (update 'cache_directory_root' and 'existing_cache_to_copy' to your local environment)
  - See Note in Step II. if you need to re-run certain parts of this step.

2. Copy the resulting 'buildings' table to your cache directory (replace the existing one).
  
VI.  Assign buildings to remaining jobs
****
1. Estimate coefficients for home_based and non_home_based ELCM, using 
   psrc_parcel/estimation/run_estimation.py
  - Uncomment the appropriate model in __main__
  - Set the appropriate cache directory in my_estimation_config.py

2. Run the employment location choice model with the estimated coefficients in order to assign buildings 
   to the remaining jobs.
  - Use: python opus_core/tools/start_run.py -c psrc_parcel.data_preparation.config_jobs
    (update 'cache_directory_root' and 'existing_cache_to_copy' to your local environment)

3. Copy the resulting 'jobs' table to your cache directory (replace the existing one).
  
VII. Post-process
****
See Step III. in the automated process above.

VIII. Exporting resulting tables to database
****
See Step IV. in the automated process above.