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

all_variables = [
    "lnsqft=ln(parcel.aggregate(urbansim_parcel.building.building_sqft))",
#    "lnsqftunit=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.residential_units))",
#    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotsqftunit=ln(parcel.parcel_sqft/parcel.aggregate(building.residential_units))",
#    "ln_bldgage=ln(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean))",
#    "far=parcel.aggregate(urbansim_parcel.building.building_sqft)/parcel.parcel_sqft",
                 ]

specification = {
       "_definition_": all_variables,

    101:   #Single Family Low Density
            [
    "constant",
    "lnsqft",
#    "lnlotsqft",
#    "ln_bldgage",
    ],

    165:   #Single Family High Density
            [
    "constant",
    "lnsqft",
#    "lnlotsqft",
    ],
#
#
#    4:   #Multi Family Residential
#            [
#    "constant",
#    "lnsqft",
#    "lnlotsqft",
#    "lnlotsqftunit",
#    ],
#
#
#    7:   #Industrial
#            [
#    "constant",
#    "lnsqft",
#    "lnlotsqft",
#    ],
#
#    8:   #Office
#            [
#    "constant",
#    "lnsqft",
#    "far",
#    "ln_bldgage",
#    ],
#
#    25:   #Mixed Use
#            [
#    "constant",
#    "lnlotsqft",
#    ],
#
#    27:   #Vacant
#            [
#    "constant",
#    "lnlotsqft",
#    ],
}
