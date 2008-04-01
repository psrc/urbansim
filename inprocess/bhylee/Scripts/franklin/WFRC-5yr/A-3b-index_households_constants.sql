# select the output database

use WFRC_1997_output_5yr_2003;

# Create the index that UrbanSim currently fails to create on its own
# (hopefully this will be fixed soon)

create index households_constants_household_id 
  on households_constants (household_id);
