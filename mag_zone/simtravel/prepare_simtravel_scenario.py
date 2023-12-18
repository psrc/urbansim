# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from pandas import read_csv
from numpy import where, concatenate, array, unique, ones
from numpy.random import permutation
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.paths import get_opus_data_path_path
from opus_core.sampling_toolbox import sample_noreplace

data_path = get_opus_data_path_path()
cache_dir = os.path.join(data_path, 'mag_zone/base_year_data')
year = 2009
simulation_state = SimulationState()
simulation_state.set_current_time(year)
SimulationState().set_cache_directory(cache_dir)
attribute_cache = AttributeCache()
dataset_pool = SessionConfiguration(new_instance=True,
                         package_order=['mag_zone', 'urbansim_zone', 
                                        'urbansim', 'opus_core'],
                         in_storage=attribute_cache
                        ).get_dataset_pool()

hh = dataset_pool.get_dataset('household')
ps = dataset_pool.get_dataset('person')
def update_households_persons():

    hh_df = read_csv(in_fname, sep=",")
    ps_df = read_csv(in_fname, sep=",")
    ## which fields need to be updated
    hh_attrs = {'': ''}
    hh_attrs_known = hh.get_known_attribute_names()
    for k, v in hh_attrs.items():
        new_values = hh_df[v].values
        if k not in hh_attrs_known:
            hh.add_attribute(k, new_values)
        else:
            hh[k] = new_values

## update buildings
def relocate_jobs():
    bldg = dataset_pool.get_dataset('building')
    jobs = dataset_pool.get_dataset('job')
    in_fname = os.path.join(data_path, 'mag_zone/simtravel_data/',
                            'alternate_employment_scenario/buildings_new.csv')
    ## remove trailing 'i4' from header
    os.system("sed 's/i4,/,/g' -i %s" % in_fname)
    bldg_df = read_csv(in_fname, sep=",")

    #bldg_df_reloc = bldg_df.set_index(['taz', 'building_type_id'])
    #bldg_df = bldg_df.join(bldg_df_reloc['building_id'], rsuffix='_new')
    bldg_reloc = where(bldg_df['zone_id'] != bldg_df['taz'])[0]
    bldg_df.set_index(['zone_id', 'building_type_id'], inplace=True)
    from numpy import asscalar, array
    for index in bldg_reloc:
    #for bldg_id, bldg_id_new in zip(bldg_df['building_id', 'zone_id'].ix[bldg_reloc]):
        a_bldg = bldg_df.ix[[index]]
        a_bldg = a_bldg.reset_index()
        ## "move" non residential spaces around
        bldg_id_org = (a_bldg.building_id).values
        bldg_of_org_id = bldg['building_id']== bldg_id_org
        taz_bldgtype_index = (asscalar(a_bldg.taz), asscalar(a_bldg.building_type_id))
        try:
            bldg_id_new = bldg_df.ix[taz_bldgtype_index, 'building_id']
            bldg_of_new_id = bldg['building_id']==bldg_id_new
            bldg_sqft_nr1 = bldg['non_residential_sqft'][bldg_of_new_id]
        except KeyError:
            ## the building id doesn't exist in the original buildings table
            max_id = max(bldg['building_id'])
            bldg_id_new = max_id + 1
            bldg.add_elements({'building_id': array([bldg_id_new]),
                              'zone_id': array([taz_bldgtype_index[0]]),
                              'building_type_id': array([taz_bldgtype_index[1]])},
                             require_all_attributes=False)
            bldg_sqft_nr1 = 0

        bldg_sqft_nr0 = bldg['non_residential_sqft'][bldg_of_org_id]
        bldg.modify_attribute('non_residential_sqft', bldg_sqft_nr0+bldg_sqft_nr1,
                              index=bldg_of_new_id)
        bldg.modify_attribute('non_residential_sqft', 0, index=bldg_of_org_id)
        ## relocate jobs
        jobs.modify_attribute('building_id', bldg_id_new, 
                              index=jobs['building_id']==bldg_id_org)

    jobs.write_dataset(attributes="*", out_storage=attribute_cache, 
                       out_table_name='jobs_employment_scenario')
    bldg.write_dataset(attributes="*", out_storage=attribute_cache,
                      out_table_name='buildings_employment_scenario')

## assign workplace to persons (workers)
persons = dataset_pool.get_dataset('person')
jobs = dataset_pool.get_dataset('job')
jobs.compute_variables('zone_id=job.disaggregate(building.zone_id)', 
                       dataset_pool=dataset_pool)
persons.add_attribute(name='job_id', data=-1*ones(persons.size(), dtype='i4'), 
                      metadata=1)
job_ids = array([], dtype='i4')
person_indices = array([], dtype='i4')
for zone in unique(persons['wtaz']):
    persons_in_zone = (where(persons['wtaz']==zone)[0]).astype('i4')
    jobs_in_zone = jobs['job_id'][jobs['zone_id']==zone]
    if persons_in_zone.size < jobs_in_zone.size:
        person_index = persons_in_zone
        new_ids = sample_noreplace(jobs_in_zone, persons_in_zone.size)
    elif persons_in_zone.size > jobs_in_zone.size:
        person_index = sample_noreplace(persons_in_zone, jobs_in_zone.size)
        new_ids = jobs_in_zone
    else:
        person_index = persons_in_zone
        new_ids = jobs_in_zone[permutation(jobs_in_zone.size)]

    job_ids = concatenate((job_ids, new_ids))
    person_indices = concatenate((person_indices, persons_in_zone))

persons.modify_attribute(name='job_id', data=job_ids, index=person_indices)
persons.write_dataset(attributes="*", out_storage=attribute_cache, 
                   out_table_name='persons')

