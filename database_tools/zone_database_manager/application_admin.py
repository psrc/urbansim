# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010 University of California, Berkeley
# See opus_core/LICENSE

from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section

class MyApplicationAdmin(ApplicationAdmin):
    name = 'UrbanSim Simple Zone Database Manager'
  
    def get_sections(self):
        from camelot.model.memento import Memento
        from .model import AnnualEmploymentControlTotal
        from .model import AnnualHouseholdControlTotal
        from .model import AnnualRelocationRatesForHousehold
        from .model import Building
        from .model import BuildingSqftPerJob
        from .model import BuildingType
        #from model import City
        from .model import County
        from .model import DevelopmentConstraint
        from .model import DevelopmentEventHistory
        from .model import EmploymentAdHocSectorGroup
        from .model import EmploymentAdHocSectorGroupDefinition
        from .model import EmploymentSector
        from .model import Faz
        from .model import HomeBasedStatus
        from .model import Household
        from .model import HouseholdCharacteristicsForHT
        from .model import HouseholdsForEstimation
        from .model import Job
        from .model import JobsForEstimation
        from .model import LargeArea
        from .model import PlanType
        from .model import RaceName
        from .model import Refinement
        from .model import ScheduledDevelopmentEvents
        from .model import ScheduledEmploymentEvents
        from .model import TargetVacancy
        from .model import TravelData
        from .model import Zone
        from camelot.model.i18n import Translation
        return [Section('Scenario Tables',
                        Icon('tango/24x24/apps/system-users.png'),
                        items = [ 
                            AnnualEmploymentControlTotal,
                            AnnualHouseholdControlTotal, 
                            AnnualRelocationRatesForHousehold,
                            DevelopmentConstraint,
                            Refinement,
                            ScheduledDevelopmentEvents,
                            ScheduledEmploymentEvents,
                            TargetVacancy
                            ]),
                Section('Base Year Data Core Tables',
                        Icon('tango/24x24/categories/preferences-system.png'),
                        items = [
                            Building,
                            Household,
                            HouseholdsForEstimation,
                            Job,
                            JobsForEstimation,
                            TravelData,
                            Zone
                        ]),
                Section('Base Year Data Lookup Tables',
                        Icon('tango/24x24/categories/preferences-system.png'),
                        items = [
                            BuildingSqftPerJob,
                            BuildingType,
                            #City,
                            County,
                            DevelopmentEventHistory,
                            EmploymentAdHocSectorGroup,
                            EmploymentAdHocSectorGroupDefinition,
                            EmploymentSector,
                            Faz,
                            HomeBasedStatus,
                            HouseholdCharacteristicsForHT,
                            LargeArea,
                            PlanType,
                            RaceName
                        ])
                        
                ]
