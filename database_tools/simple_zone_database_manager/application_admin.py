from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section

class MyApplicationAdmin(ApplicationAdmin):
    name = 'UrbanSim Simple Zone Database Manager'
  
    def get_sections(self):
        from camelot.model.memento import Memento
        from model import AnnualEmploymentControlTotal
        from model import AnnualHouseholdControlTotal
        from model import Building
        from model import BuildingType
        from model import EmploymentSector
        from model import Household
        from model import HouseholdCharacteristicsForHT
        from model import Job
        from model import TravelData
        from model import Zone
        from camelot.model.i18n import Translation
        return [Section('Scenario Tables',
                        Icon('tango/24x24/apps/system-users.png'),
                        items = [ 
                            AnnualEmploymentControlTotal, 
                            AnnualHouseholdControlTotal
                            ]),
                Section('Base Year Data Core Tables',
                        Icon('tango/24x24/categories/preferences-system.png'),
                        items = [
                            Building,
                            Household,
                            Job,
                            TravelData,
                            Zone
                        ]),
                Section('Base Year Data Lookup Tables',
                        Icon('tango/24x24/categories/preferences-system.png'),
                        items = [
                            BuildingType,
                            EmploymentSector,
                            HouseholdCharacteristicsForHT,
                        ])
                        
                ]
