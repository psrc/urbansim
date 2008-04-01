
from run_indicator import database_name_for_2010_2020_2030_results
from run_indicator import ExcelChart

chart = ExcelChart(database_name_for_2010_2020_2030_results, "region")

# Indicators that do NOT work
#----------------------------
## Real Estate indicators 
#chart.show( "Nonresidential sqft per year" )
#chart.show( "Nonresidential sqft added per year" )
#chart.show( "Vacant nonresidential sqft per year" )
#chart.show( "Acres of land converted from type vacant developable per development type per year" )
#chart.show( "Cells per development type per year" )
#chart.show( "Nonresidential sqft added per starting development type per year" )
#chart.show( "Nonresidential sqft vacancy rate per development type per year" )
#chart.show( "Number of development events per starting development type per year" )
#chart.show( "Residential units added per ending development type per year" )
#chart.show( "Residential units added per starting development type per year" )
#chart.show( "Residential vacancy rate per development type per year" )
## Population Indicators
#chart.show( "Household car ownership" )

# Indicators that DO work:
#-------------------------
## Real Estate indicators
chart.show( "Nonresidential sqft vacancy rate per year" )
chart.show( "Occupied nonresidential sqft per year" )
chart.show( "Nonresidential sqft vacancy rate per year" )
chart.show( "Occupied nonresidential sqft per year" )
chart.show( "Occupied residential units per year" )
chart.show( "Residential density" )
chart.show( "Residential units per year" )
chart.show( "Residential units added per year" )
chart.show( "Residential vacancy rate per year" )
chart.show( "Vacant residential units per year" )
chart.show( "Acres of vacant developable land per year" )
chart.show( "Number of development events per year" )
## Employment Indicators
chart.show( "Employment density" )
chart.show( "Jobs per capita" )
chart.show( "Jobs per year" )
chart.show( "Employment change" )
chart.show( "Jobs housing balance" )
chart.show( "Jobs moving per year" )
chart.show( "Job spaces per year" )
chart.show( "Unplaced jobs per year" )
## Household Indicators
chart.show( "Household density" )
chart.show( "Households per year" )
chart.show( "Mean household income" )
chart.show( "Population" )
chart.show( "Population change" )
chart.show( "Population density" )
chart.show( "Households added or deleted per year" )
chart.show( "Households moving per year" )
chart.show( "Unplaced households per year" )

print 'Done generating indicators'
