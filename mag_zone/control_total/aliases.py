# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           'county_id=mpa_id*0+1',
           'households = control_total.number_of_agents(household)',
           'jobs = control_total.number_of_agents(job)',
           ]