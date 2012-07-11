Instructions for Running Refinement in 2010:
===========================================

- Copy 2000 and 2010 cache into a base year directory
- Remove all *.computed sub-directories from 2000 and 2010
- Copy all *_specification and *_coefficients tables from 2000 to 2010
- Get an input table of refinements into 2010 cache
- run a simulation:
python ~/workspace/src/opus_core/tools/start_run.py -x ~/workspace/project_configs/psrc_parcel_refinement.xml -s '2010_refinement'

Postprocessing:
- In the created run cache, delete all *.computed directories, households/zone_id, jobs/zone_id, jobs/transaction_id, and jobs/refinement_id.
- Replace tables households, persons, jobs, buildings, parcels in the 2010 cache of the 'refined' run by the tables from the newly created 2011 cache.

Description of the Refinement Process:
=====================================
Goal is to create a spacial distribution of households and jobs that corresponds to observed distribution. 

A refinements table should be created by differencing simulation results in 2010 and observed data on zone level. Use only 'add' and 'subtract' actions. All transactions for households should have the same transaction id and  all transactions for jobs should have the same transaction id. All 'subtract' actions should be defined on building level; all 'add' actions should be defined on zone level.

Models are run in the following order:
--------------------------------------
1. Refinement model: 
Removing agents from buildings is done by first identifying buildings of the particular zone that were built after 2000 and are not MPDs. Then a building is randomly sampled and all agents (both households  and jobs) from that building are removed. The sampling is repeated until the desired amount of agents is reached. The sampled buildings are then demolished. If there is not enough such buildings, the rest of agents is sampled randomly across all other buildings of that zone and those buildings are not demolished.

Agents removed from their location in the previous step are now in a pool to be added to zones. No building_id is assigned in this step. If there are not enough agents in the  pool, other agents are cloned to meet the target.

2. Real estate price model

3. Expected sales price model
  
4. Development proposal choice model on zonal level:
For each zone, the model makes an estimate how many households and jobs of each sector are going to look for a location in that zone. If there are not enough buildings to meet the target vacancy when the additional agents are added, it selects an appropriate number of proposals for buildings to be build in the next step.

5. Building construction model 

6. Household location choice model on zonal level:
Runs only for households that have zone_id but no building_id assigned. There is no sampling of alternatives, i.e. each household sees all available  buildings in that zone.

7.  Employment location choice model on zonal level:
Runs only for non-home based jobs that have zone_id but no building_id assigned. There is no sampling of alternatives, i.e. each job sees all available  buildings in that zone.

8. Scaling model on zonal level:
Places governmental jobs within each zone.

9. Breaking worker-job links:
For workers of households that were relocated, it breaks its job link only if the accessibility to work is lower than before. 
For workers whose jobs were re-located, it breaks all job links.

10. Workplace choice model:
Runs for workers who lost their job in the previous step.





