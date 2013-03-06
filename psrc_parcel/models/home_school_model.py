# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.models.school_type_choice_model import SchoolTypeChoiceModel

class HomeSchoolModel(SchoolTypeChoiceModel):
    model_name = "Home School Model"    
    def prepare_for_estimate(self, *args, **kwargs):
        spec, index, estimation_set = SchoolTypeChoiceModel.prepare_for_estimate(self, *args, **kwargs)
        home_school = estimation_set.compute_variables("%s.school_type==3" % estimation_set.get_dataset_name())
        estimation_set.add_primary_attribute(name=self.choice_attribute_name, data=home_school)
        return (spec, index, estimation_set)
    
    def prepare_for_estimate_hh(self, *args, **kwargs):
        spec, index, estimation_set = SchoolTypeChoiceModel.prepare_for_estimate_hh(self, *args, **kwargs)
        home_school = estimation_set.compute_variables("household.aggregate(person.school_type==3)>0",
                                                       dataset_pool=self.dataset_pool)
        estimation_set.add_primary_attribute(name=self.choice_attribute_name, data=home_school)
        return (spec, index, estimation_set)