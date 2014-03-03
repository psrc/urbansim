Instructions for Running Refinement in 20x0 (x={1,2,3,4}):
===========================================

- Copy 2000 and 20x0 cache into a base year directory
- Remove all *.computed sub-directories from 2000 and 20x0
- Copy all *_specification and *_coefficients tables from 2000 to 20x0
- Get an input table of refinements into 20x0 cache
- In project_configs/psrc_parcel_refinement.xml:
	o make sure it inherits from the right parent,
	o put the name of your cache directory into the scenario nodes existing_cache_to_copy and cache_directory.
- run a simulation:
python ~/workspace/src/opus_core/tools/start_run.py -x ~/workspace/project_configs/psrc_parcel_refinement_{faz|city}_20x0.xml -s '20x0_refinement'

Postprocessing:
- In the created 20x3 run cache, delete all *.computed directories, {households|jobs}/{zone_id, faz_id, city_id, transaction_id, refinement_id}.
- If used for continuing a run (e.g. 2010 refinement), replace tables households, persons, jobs, buildings, parcels in the 20x0 cache 
  of the to-be-continued run by the tables from the newly created 20x3 cache.

Description of the Refinement Process for 2010 on faz level:
============================================================
Goal is to create a spatial distribution of households and jobs that corresponds to observed distribution. 

A refinements table should be created by differencing simulation results in 2010 and observed data on faz level. 
Use only 'add' and 'subtract' actions. All transactions for households should have the same transaction id 
and  all transactions for jobs should have the same transaction id. 
All 'subtract' actions should be defined on building level; all 'add' actions should be defined on faz level.

Models are split into a three years run and they run in the following order:
---------------------------------------------------------------------
Year 2011:
1. Refinement model: 
Removing agents from buildings is done by first identifying buildings of the particular zone that were built after 2000 and are not MPDs. 
Then a building is randomly sampled and all agents (both households  and jobs) from that building are removed. 
The sampling is repeated until the desired amount of agents is reached. The sampled buildings are then demolished. 
If there is not enough such buildings, the rest of agents is sampled randomly across all other buildings of that zone and those buildings are not demolished.

Agents removed from their location in the previous step are now in a pool to be added to zones. No building_id is assigned in this step. 
If there are not enough agents in the  pool, other agents are cloned to meet the target.

2. Real estate price model

3. Expected sales price model
  
4. Development proposal choice model on faz level:
For each zone, the model makes an estimate how many households and jobs of each sector are going to look for a location in that zone. 
If there are not enough buildings to meet the target vacancy when the additional agents are added, it selects an appropriate 
number of proposals for buildings to be build in the next step.

5. Building construction model 

Year 2012: 
6. Household location choice model on faz level:
Runs only for households that have faz_id but no building_id assigned.

Year 2013:
7.  Employment location choice model on faz level:
Runs only for non-home based jobs that have faz_id but no building_id assigned.

8. Scaling model on faz level:
Places governmental jobs within each zone.

9. Breaking worker-job links:
For workers of households that were relocated, it breaks its job link only if the accessibility to work is lower than before. 
For workers whose jobs were re-located, it breaks all job links.

10. Workplace choice model:
Runs for workers who lost their job in the previous step.

For refinements in 2020, 2030 and 2040, we also do scaling unplaced households and jobs in place at the end,
since we do not care about the capacity. 



