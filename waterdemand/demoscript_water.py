# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

print "Create Dataset object for weather"
import waterdemand
us_path = waterdemand.__path__[0]
from waterdemand.weather import WeatherSet
weather = WeatherSet(in_storage_type = "tab",
in_storage_location = us_path,
in_table_name = "weather.tab", id_name="year_id")


print "Access weather information"
print weather.get_nonderived_attribute_names()
print weather.get_id_attribute()
print weather.get_attribute_names()
print weather.get_attribute("p_tot2")
print weather.summary()