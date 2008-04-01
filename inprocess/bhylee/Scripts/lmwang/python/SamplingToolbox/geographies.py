#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
# 

from numarray import where, array
import path_configuration
from misc.miscellaneous import create_list_string, do_id_mapping


class Geography:
    """The attributes of this class are set in the method GeographySet.get_object."""

class GeographyAttribute:
    def __init__(self, parent, recarray):
        self.parent = parent
        self.array = recarray
        
    def data(self):
        """Returns the 1D array which this attribute represents"""
        return self.array
        
class GeographySet:
    def __init__(self, database_connection, mapping_table="gridcells_in_geography", table="geographies",geography_type="district"):
        """Reads geographies and their mapping with gridcells from MySQL tables. """
        self.attribute_names = ["grid_id", "geography_id", geography_type] #"geography_type_id", "geography_type_title",
        self.geography_type = geography_type.lower()
        columns = create_list_string(map(lambda(x): "a." + x, self.attribute_names[0:2]), ", ")
         query = "select " + columns
         #columns = create_list_string(map(lambda(x): "b." + x, self.attribute_names[3:]), ", ")
         #query = query + ", " + columns
        query = query + ", " + "geography_id as " + geography_type
        query = query + " from " + mapping_table + " a"
        query = query + " inner join "+ table + " b"
        query = query + " using (geography_type_id) where b.geography_type_title='" + self.geography_type + "'"
        query = query + " order by a.grid_id"
        geographiesarray = database_connection.TryGetRecordArrayFromQuery(query)
        self.geographies={}
        self.area={}
        self.id_mapping = do_id_mapping(geographiesarray,"grid_id")
        for attribute in self.attribute_names:
            self.geographies[attribute] = GeographyAttribute(self, array(geographiesarray.field(attribute)))
        self.n = len(geographiesarray.field(0))
        self.map_geography_area()
        
    def get_object(self, index):
        """Returns an object of class Geography of the given index. """
        geography = Geography()
        for col in self.attribute_names:
            setattr(geography, col, self.get_attribute(col)[index])
        return geography
        
    def get_object_by_id(self, id):
        """Returns an object of class Geography of the given geography_id. """
        self.check_id(id)
        return self.get_object(self.id_mapping[id])

    def map_geography_area(self,geography_id=None):
        for i in range(self.n):
            g = self.get_object(i)
            self.area.setdefault(g.geography_id, []).append(i)            
        return self.area.get(geography_id)

    def subset_by_geography_id(self,geography_id):
        if len(self.area) == 0:
            self.map_geography_area()
        subset = GeographySubset(self, self.area[geography_id])
        return subset
            
    def get_attribute(self, attribute):
        """Returns the given attribute, as a numarray of the correct type, for all geographies.
        Attribute names are the same as column names in the database table, but in lowercase"""
        if not (attribute in self.attribute_names):
            raise NameError, "Attribute " + attribute + " not found!"
        return self.geographies[attribute].data()
        
    def get_attribute_by_id(self, attribute, id):
        self.check_id(id)
        return self.get_attribute(attribute)[self.id_mapping[id]]
        
    def check_id(self, id):
        if not self.id_mapping.has_key(id):
            raise RuntimeError, "Id " + id + " not found in geography set"
                    
class GeographySubset(GeographySet):
    """Class for viewing a subset of a GeographySet object, identified by a list of indices."""
    def __init__(self, parent, index):
        self.parent = parent
        self.n = len(index)
        self.index = index
    
    def get_attribute(self, attribute):
        return self.parent.get_attribute(attribute)[self.index]
    
    def get_attribute_names(self):
        return self.parent.get_attribute_names()


if __name__ == "__main__":
    import os
    from multiDB.MultiDB import DbConnection
    
    print "run tests..."
    #indb = "Eugene_baseyear"
    indb = "PSRC_2000_baseyear_sampling_script_testbed_lmwang"
    db_host_name=os.environ['MYSQLHOSTNAME']
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']
        
    print "Connecting database ..."
    Con = DbConnection(db=indb, hostname=db_host_name, username=db_user_name, 
               password=db_password)
    bdir = "./households_export"
    #gridcells = GridcellSet(database_connection=Con, base_directory=bdir)
    geography_name = "fazdistrict"
    districts = GeographySet(database_connection=Con, geography_type=geography_name)

    for geography_id in districts.area.keys():
        districts_subset = districts.subset_by_geography_id(geography_id)
        print "in", geography_name, geography_id, ":"
        print districts_subset.get_attribute('grid_id')
