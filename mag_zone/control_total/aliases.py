# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           #'mpa_id=control_total.disaggregate(raz2012.mpa_id)',
           'county_id = control_total.disaggregate(super_raz.county_id)',
           'households = control_total.number_of_agents(household)',
           'jobs = control_total.number_of_agents(job)',
           'persons = control_total.number_of_agents(person)',
           ]
