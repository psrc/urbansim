from psrc_parcel.models.school_type_choice_model import SchoolTypeChoiceModel

class HomeSchoolModel(SchoolTypeChoiceModel):
        
    def prepare_for_estimate(self, *args, **kwargs):
        spec, index, estimation_set = SchoolTypeChoiceModel.prepare_for_estimate(self, *args, **kwargs)
        home_school = estimation_set.compute_variables("%s.school_type==3" % estimation_set.get_dataset_name())
        estimation_set.add_primary_attribute(name=self.choice_attribute_name, data=home_school)
        return (spec, index, estimation_set)