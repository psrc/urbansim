# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "building_type_id = household.disaggregate(building.building_type_id)",
           "large_area_id = household.disaggregate(faz.large_area_id, intermediates=[zone,parcel,building])",
           "nonneg_large_area_id = (psrc_parcel.household.large_area_id > 0)*psrc_parcel.household.large_area_id",
           "age_of_oldest_child = household.aggregate((person.age<=18) * person.age, function=maximum)",
           "age_of_oldest_child_in_private_school = household.aggregate(psrc_parcel.person.is_in_private_k12_school * person.age, function=maximum)",
           "age_of_oldest_child_in_home_school = household.aggregate(psrc_parcel.person.is_in_home_school * person.age, function=maximum)",
           "is_poor = %s + %s + %s + %s + %s + %s + %s + %s" % (
                            "(household.persons==1)*(household.income < 8350)",
                            "(household.persons==2)*(household.income < 11250)",
                            "(household.persons==3)*(household.income < 14150)",
                            "(household.persons==4)*(household.income < 17050)",
                            "(household.persons==5)*(household.income < 19950)",
                            "(household.persons==6)*(household.income < 22850)",
                            "(household.persons==7)*(household.income < 25750)",
                            "(household.persons==8)*(household.income < 28650)",
                            ),
            "is_wealthy = %s + %s + %s + %s + %s + %s + %s + %s" % (
                            "(household.persons==1)*(household.income > 83500)",
                            "(household.persons==2)*(household.income > 112500)",
                            "(household.persons==3)*(household.income > 141500)",
                            "(household.persons==4)*(household.income > 170500)",
                            "(household.persons==5)*(household.income > 199500)",
                            "(household.persons==6)*(household.income > 228500)",
                            "(household.persons==7)*(household.income > 257500)",
                            "(household.persons==8)*(household.income > 286500)",
                            )
           ]
