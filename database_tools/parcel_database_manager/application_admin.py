# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010 University of California, Berkeley
# See opus_core/LICENSE

from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section

class MyApplicationAdmin(ApplicationAdmin):
    name = 'UrbanSim Parcel Database Manager'
  
    def get_sections(self):
        from camelot.model.memento import Memento
        from model import AnnualHouseholdControlTotal
        from model import EmploymentSector
        from model import AnnualEmploymentControlTotal
        from model import AnnualRelocationRatesForHousehold
        from model import AnnualJobRelocationRates
        from model import Building
        from model import BuildingSqftPerJob
        from model import BuildingType
        #from model import City
        from model import County
        from model import DemolitionCostPerSqft
        from model import DevelopmentConstraint
        from model import DevelopmentEventHistory
        from model import DevelopmentProjectProposal
        from model import DevelopmentTemplate
        from model import DevelopmentTemplateComponents
        from model import EmploymentAdHocSectorGroup
        from model import EmploymentAdHocSectorGroupDefinition
        from model import EmploymentSector
        from model import Faz
        from model import GenericLandUseType
        from model import HomeBasedStatus
        from model import Household
        from model import HouseholdCharacteristicsForHT
        from model import HouseholdsForEstimation
        from model import Job
        from model import JobsForEstimation
        from model import LandUseType
        from model import LargeArea
        from model import Parcel
        from model import PlanType
        from model import RaceName
        from model import Refinement
        from model import ScheduledDevelopmentEvents
        from model import ScheduledEmploymentEvents
        from model import TargetVacancy
        from model import TravelData
        from model import VelocityFunction
        from model import Zone
        from camelot.model.i18n import Translation
        #self.register(AnnualHouseholdControlTotal, AnnualHouseholdControlTotal.Admin)
        #self.register(AnnualEmploymentControlTotal, AnnualEmploymentControlTotal.Admin)
        #self.register(AnnualRelocationRatesForHousehold, AnnualRelocationRatesForHousehold.Admin)
        return [Section('Scenario Tables',
                        Icon('tango/22x22/apps/system-users.png'),
                        items = [ 
                            AnnualHouseholdControlTotal, 
                            AnnualEmploymentControlTotal,
                            AnnualRelocationRatesForHousehold,
                            AnnualJobRelocationRates,
                            DemolitionCostPerSqft,
                            DevelopmentConstraint,
                            DevelopmentProjectProposal,
                            Refinement,
                            ScheduledDevelopmentEvents,
                            ScheduledEmploymentEvents,
                            TargetVacancy,
                            VelocityFunction
                            ]),
                Section('Base Year Data Core Tables',
                        Icon('tango/22x22/categories/preferences-system.png'),
                        items = [
                            Building,
                            Household,
                            HouseholdsForEstimation,
                            Job,
                            JobsForEstimation,
                            Parcel,                        
                            TravelData,
                            Zone
                        ]),
                Section('Base Year Data Lookup Tables',
                        Icon('tango/22x22/categories/preferences-system.png'),
                        items = [
                            BuildingSqftPerJob,
                            BuildingType,
                            #City,
                            County,
                            DevelopmentEventHistory,
                            EmploymentSector,
                            DevelopmentTemplate,
                            DevelopmentTemplateComponents,
                            EmploymentAdHocSectorGroup,
                            EmploymentAdHocSectorGroupDefinition,
                            EmploymentSector,
                            Faz,
                            GenericLandUseType,
                            HomeBasedStatus,
                            HouseholdCharacteristicsForHT,
                            LandUseType,
                            LargeArea,
                            PlanType,
                            RaceName
                        ])
                        
                ]
