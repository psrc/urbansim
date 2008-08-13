#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.

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