#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
        "residential_units = zone.aggregate(pseudo_building.residential_units)",
        "vacant_residential_units = numpy.maximum(0, urbansim_zone.zone.residential_units - urbansim.zone.number_of_households)",
        "commercial_job_spaces = zone.aggregate(pseudo_building.commercial_job_spaces)",
        "industrial_job_spaces = zone.aggregate(pseudo_building.industrial_job_spaces)",
        "number_of_vacant_commercial_jobs = numpy.maximum(0, urbansim_zone.zone.commercial_job_spaces - urbansim_zone.zone.number_of_commercial_jobs)",
        "number_of_vacant_industrial_jobs = numpy.maximum(0, urbansim_zone.zone.industrial_job_spaces - urbansim_zone.zone.number_of_industrial_jobs)",
        "developable_residential_units = numpy.maximum(0, zone.aggregate(pseudo_building.residential_units_capacity - pseudo_building.residential_units))",
           ]
