# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
