# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.monte_carlo_assignment_model import MonteCarloAssignmentModel
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
    
if __name__ == '__main__':        
    cache_directory = '/workspace/urbansim_cache/mag_zone/base_year_data.asu2wtaz_schtaz'
    year = 2009
    
    simulation_state = SimulationState()
    simulation_state.set_cache_directory(cache_directory)
    simulation_state.set_current_time(year)
    attribute_cache = AttributeCache()
    dataset_pool = SessionConfiguration(new_instance=True,
#                                        package_order=config['dataset_pool_configuration'].package_order,
                                        in_storage=attribute_cache).get_dataset_pool()
    persons = dataset_pool.get_dataset('person')
    persons.compute_variables(["htaz=person.disaggregate(household.disaggregate(building.zone_id)) * numpy.in1d(person.work_status, (1,2))",
                               #"is_student=numpy.in1d(person.student_status<3, (1,2))",
                               "is_student=person.student_status<3",
                               ])
    hbw_trips = dataset_pool.get_dataset('hbw_trip', dataset_arguments={'id_name':[]})
    hbw_trips.compute_variables(["htaz=(hbw_trip.from_zone_id).astype('i4')",
                                 "wtaz=(hbw_trip.to_zone_id).astype('i4')",
                                 "zone_id=(hbw_trip.from_zone_id).astype('i4')",
                                 "weight=safe_array_divide(hbw_trip.var, (hbw_trip.disaggregate(zone.aggregate(hbw_trip.var))).astype('f'))",
                               ])

    MonteCarloAssignmentModel().run(persons, hbw_trips, 
                                    id_name1='htaz', id_name2='wtaz',
                                    fraction_attribute_name="weight")
    persons.write_dataset(out_storage=attribute_cache, 
                                     out_table_name="persons",
                                     attributes=["wtaz"])
    
    schools = dataset_pool.get_dataset('school', dataset_arguments={'id_name':[]})
    schools.compute_variables(["is_student=school.total_mean>0",
                               "schtaz=(school.taz).astype('i4')",
                               "weight=(school.total_mean).astype('f') / alldata.aggregate_all(school.total_mean)"
                               ])
    MonteCarloAssignmentModel().run(persons, schools, 
                                    id_name1='is_student', id_name2='schtaz',
                                    fraction_attribute_name="weight")
    persons.write_dataset(out_storage=attribute_cache, 
                                     out_table_name="persons", 
                                     attributes=["schtaz"])