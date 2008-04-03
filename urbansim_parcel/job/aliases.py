#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

aliases = [
   "zone_id = job.disaggregate(urbansim_parcel.building.zone_id)",
   "parcel_id = job.disaggregate(building.parcel_id)",
   "grid_id = job.disaggregate(urbansim_parcel.building.grid_id)",
   "is_untaken_non_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==2)",   
   "is_untaken_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==1)",
   
           ]