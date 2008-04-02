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
aliases = ['is_worker = person.employment_status > 0',
           'is_worker_without_job = numpy.logical_and(urbansim_parcel.person.is_worker, person.job_id <= 0)',
           'is_worker_with_job = numpy.logical_and(urbansim_parcel.person.is_worker, person.job_id > 0)',
           'is_non_home_based_worker_with_job = numpy.logical_and( numpy.logical_and(urbansim_parcel.person.is_worker,  (person.work_at_home!=1)), person.job_id > 0)',
           'is_non_home_based_worker_without_job = numpy.logical_and( numpy.logical_and(urbansim_parcel.person.is_worker,  (person.work_at_home!=1)), person.job_id <= 0)',
           'zone_id=person.disaggregate(urbansim_parcel.household.zone_id)',
           ]