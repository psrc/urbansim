# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import where, array, zeros, logical_and

class EducationModel(AgentRelocationModel):
    """
    """
    model_name = "Education Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name = person_set.get_dataset_name()
        index = AgentRelocationModel.run(self, person_set, resources=resources)
        logger.log_status("%s students decide to leave school" % (index.size) )

        #Update educational level attained by students, accounting for their age
        no_school = person_set.compute_variables('_no_school = (person.age > 2) * (person.age < 5)')
        nursery_to_fourth = person_set.compute_variables('_nurs_to_fourth = (person.age > 4) * (person.age < 10)')
        fifth_sixth = person_set.compute_variables('_fifth_sixth = (person.age > 9) * (person.age < 12)')
        seventh_eigth = person_set.compute_variables('_sev_eigth = (person.age > 11) * (person.age < 14)')
        ninth = person_set.compute_variables('_ninth = (person.age > 13) * (person.age < 15)')
        tenth = person_set.compute_variables('_tenth = (person.age > 14) * (person.age < 16) * (person.student_status > 1)')
        eleventh = person_set.compute_variables('_eleventh = (person.age > 15) * (person.age < 17) * (person.student_status > 1)')
        twelfth = person_set.compute_variables('_twelfth = (person.age > 16) * (person.age < 18) * (person.student_status > 1)')
        hsgrad = person_set.compute_variables('_hsgrad = (person.age > 17) * (person.age < 19) * (person.student_status > 1)')
        somecollege = person_set.compute_variables('_somecoll = (person.age > 18) * (person.age < 20) * (person.student_status > 1)')
        somecollege2 = person_set.compute_variables('_somecoll2 = (person.age > 19) * (person.age < 21) * (person.student_status > 1)')
        associate = person_set.compute_variables('_assoc = (person.age > 20) * (person.age < 22) * (person.student_status > 1)')
        bachelors = person_set.compute_variables('_bach = (person.age > 21) * (person.age < 24) * (person.student_status > 1)')
        masters = person_set.compute_variables('_mast = (person.age > 23) * (person.age < 25) * (person.student_status > 1)')
        professional = person_set.compute_variables('_prof = (person.age > 24) * (person.age < 28) * (person.student_status > 1)')
        phd = person_set.compute_variables('_phd = (person.age > 27) * (person.student_status > 1) ')

        idx_no_school = where(no_school)[0]
        idx_nursery_to_fourth = where(nursery_to_fourth)[0]
        idx_fifth_sixth = where(fifth_sixth)[0]
        idx_seventh_eigth = where(nursery_to_fourth)[0]
        idx_ninth = where(ninth)[0]
        idx_tenth = where(tenth)[0]
        idx_eleventh = where(eleventh)[0]
        idx_twelfth = where(twelfth)[0]
        idx_hsgrad = where(hsgrad)[0]
        idx_somecollege = where(somecollege)[0]
        idx_somecollege2 = where(somecollege2)[0]
        idx_associate = where(associate)[0]
        idx_bachelors = where(bachelors)[0]
        idx_masters = where(masters)[0]
        idx_professional = where(professional)[0]
        idx_phd = where(phd)[0]

        if idx_no_school.size > 0:
            person_set.modify_attribute('education', array(idx_no_school.size*[1]), idx_no_school)
            person_set.modify_attribute('student_status', array(idx_no_school.size*[1]), idx_no_school)
        if idx_nursery_to_fourth.size > 0:
            person_set.modify_attribute('education', array(idx_nursery_to_fourth.size*[2]), idx_nursery_to_fourth)
            person_set.modify_attribute('student_status', array(idx_nursery_to_fourth.size*[2]), idx_nursery_to_fourth)
        if idx_fifth_sixth.size > 0:
            person_set.modify_attribute('education', array(idx_fifth_sixth.size*[3]), fifth_sixth)
        if idx_seventh_eigth.size > 0:
            person_set.modify_attribute('education', array(idx_seventh_eigth.size*[4]), idx_seventh_eigth)
        if idx_ninth.size > 0:
            person_set.modify_attribute('education', array(idx_ninth.size*[5]), idx_ninth)
        if idx_tenth.size > 0:
            person_set.modify_attribute('education', array(idx_tenth.size*[6]), idx_tenth)
        if idx_eleventh.size > 0:
            person_set.modify_attribute('education', array(idx_eleventh.size*[7]), idx_eleventh)
        if idx_twelfth.size > 0:
            person_set.modify_attribute('education', array(idx_twelfth.size*[8]), idx_twelfth)
        if idx_hsgrad.size > 0:
            person_set.modify_attribute('education', array(idx_hsgrad.size*[9]), idx_hsgrad)
        if idx_somecollege.size > 0:
            person_set.modify_attribute('education', array(idx_somecollege.size*[10]), idx_somecollege)
        if idx_somecollege2.size > 0:
            person_set.modify_attribute('education', array(idx_somecollege2.size*[11]), idx_somecollege2)
        if idx_associate.size > 0:
            person_set.modify_attribute('education', array(idx_associate.size*[12]), associate)
        if idx_bachelors.size > 0:
            person_set.modify_attribute('education', array(idx_bachelors.size*[13]), idx_bachelors)
        if idx_masters.size > 0:
            person_set.modify_attribute('education', array(idx_masters.size*[14]), idx_masters)
        if idx_professional.size > 0:
            person_set.modify_attribute('education', array(idx_professional.size*[15]), idx_professional)
        if idx_phd.size > 0:
            person_set.modify_attribute('education', array(idx_phd.size*[16]), idx_phd)

        # Change the student_status of those predicted to exit from schooling.  Whatever educational level they have reached this year is their final level.
        person_set['student_status'][index] = 1