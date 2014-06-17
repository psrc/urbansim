# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.person_x_job.logsum_hbw_am_from_home_to_work import logsum_hbw_am_from_home_to_work

class logsum_hbw_am_from_home_to_work_4k(logsum_hbw_am_from_home_to_work):
    """logsum_hbw_am_time_from_home_to_work (4k model)
       logsum breaks by income:
           Less than $34K;
           $34K to $64K;
           $64 to $102K;
           More than $102K.
    """
    default_value = -20
    agent_category_attribute = "logsum_income_break = (person.disaggregate(psrc_parcel.household.income_breaks_34000_64000_102000)).astype(int32)"

