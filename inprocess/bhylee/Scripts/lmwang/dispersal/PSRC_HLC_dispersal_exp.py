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

from configure_path import *
import os
from gridcellset.gridcells import GridcellSet
from householdset.households import HouseholdSet
from classifications.races import RaceSet
from classifications.developmenttypes import DevelopmentTypeSet
from classifications.rates import RateSet
from zoneset.zones import ZoneSet
#from example_gridcells import DB_settings
from const.constants import read_constants_from_DB
from coefficients import Coefficients
from equation_specification import EquationSpecification
from storage_creator import StorageCreator
from store.MultiDB import DbConnection
from household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from household_relocation_model_creator import HouseholdRelocationModelCreator
from indicators import Indicators
from resources import Resources
from numarray.random_array import seed
from numarray import ones, arange, where
from numarray.ma import filled
from random import sample
from math import ceil
from time import time

def get_data_objects_from_DB(con, accessibilitiesflag=0, debuglevel=0):
    constants = read_constants_from_DB(con)
    races = RaceSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    devtypes = DevelopmentTypeSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    zones = ZoneSet(in_base = con, in_storage_type="MySQL", \
        accessibilitiesflag=accessibilitiesflag, debuglevel=debuglevel)
    resources = {"constants":constants, "developmenttype":devtypes, "zone":zones, "race":races}
    return resources

class DB_settings:
    db_host_name=os.environ['MYSQLHOSTNAME']
    #db_host_name="localhost"
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']    
       
class PSRC_Settings:
    dir = "./PSRC_data_dir"
    outputdir = dir + "/output"
    gcsubdir = "gc"
    hhsubdir = "hh"
    db = "PSRC_2000_baseyear_0510_lmwang"
        
class PSRC_simulation:
    def run(self, gcs, hhs, data_objects, dbcon, variables=[], years=1, debuglevel=0):
        t1 = time()
        storage = StorageCreator().get_storage("MySQL", Resources({"base":dbcon}))
        coefficients = Coefficients(storage=storage)
        coefficients.load(place="household_location_choice_model_coefficients")
        specification = EquationSpecification(storage=storage)
        specification.load(place="household_location_choice_model_specification", \
                variables=variables)
        hlcm = HouseholdLocationChoiceModelCreator().get_model(\
            choicestype="lottery", sample_size_locations=10, \
            sample_proportion_locations=None, \
            debuglevel=debuglevel)
        hrm = HouseholdRelocationModelCreator().get_model(debuglevel=debuglevel)
        hh_rateset = RateSet(in_base = dbcon, what="households", debuglevel=debuglevel)
        hh_relocation_resources = Resources({"rates":hh_rateset})

        for year in range(years):
            print "Simulation for year "+str(year+1)
            # delete variables
            gcs.delete_derived_attributes()
            hhs.delete_derived_attributes()
            # relocate
            relocation_results = hrm.run(hhs,resources=hh_relocation_resources)
            # run hlcm
            result = hlcm.run(specification, coefficients, gcs, hhs, nchunks=12, \
                    agents_index=relocation_results, data_objects=data_objects)  
        print "Simulation done. " + str(time()-t1) + " s"


    
class Run_PSRCsimulation_and_map_results:
    def __init__(self, variables=[], indicators=None, years=1, debuglevel=0):
#        from rpy import r 
#        r.postscript(file="zones_"+indicators+".ps")
#        r.par(mfrow=r.c(2,1))
        Con = DbConnection(db=PSRC_Settings.db, hostname=DB_settings.db_host_name, \
                username=DB_settings.db_user_name, password=DB_settings.db_password)

        self.gcs = GridcellSet(in_base = PSRC_Settings.dir, in_storage_type="flt", \
                               in_place=PSRC_Settings.gcsubdir, debuglevel=debuglevel)
        self.hhs = HouseholdSet(in_base = PSRC_Settings.dir, in_storage_type="flt", \
                                in_place=PSRC_Settings.hhsubdir, debuglevel=debuglevel)
        self.data_objects = get_data_objects_from_DB(Con, accessibilitiesflag=1, debuglevel=debuglevel)
        self.resources = Resources(self.data_objects)
        self.resources.merge({"household":self.hhs, "gridcell":self.gcs})
        # compute and store indicators for the base year
        self.indicators = Indicators(names=indicators, datasets={"zone":self.data_objects["zone"], \
                "gridcell":self.gcs})
        self.compute_indicators_and_write_results(indicators, base=PSRC_Settings.outputdir, type="flt", \
            subdir = "base")
        # plot indicator for the base year
        #import pdb; pdb.set_trace()
#         self.plot_variable(indicator, self.data_objects["zone"], \
#                 main="base year for zones")
#         # store indicator for the base year
#         self.gcs.compute_variables(indicator, resources=self.resources)
#         self.write_gridcells_results([indicator, "aggregated_"+indicator], base=PSRC_Settings.outputdir,\
#             type="flt", place="base/"+PSRC_Settings.gcsubdir)
        #simulate
        PSRC_simulation().run(gcs=self.gcs, hhs=self.hhs, data_objects=self.data_objects,\
                dbcon=Con, variables=variables, years=years, \
            debuglevel=debuglevel)
#         self.gcs.delete_derived_attributes()
#         self.hhs.delete_derived_attributes()
#         self.data_objects["zone"].delete_derived_attributes()
#         # plot indicator for the end year
#         self.plot_variable(indicator, self.data_objects["zone"], \
#                 main="after " + str(years)+ " years (zones)")
#         r.dev_off()
#         # store indicator for the end year
#         self.gcs.compute_variables(indicator, resources=self.resources)
#         self.write_gridcells_results([indicator, "aggregated_"+indicator], base=PSRC_Settings.outputdir,\
#             type="flt", place="year_"+ str(years)+'/'+PSRC_Settings.gcsubdir)
        Con.close_connection()
        
#     def plot_variable(self, name, object, main=""):
#         object.compute_variables(name, resources=self.resources)
#         values = filled(object.get_attribute(name),0.0)
#         values_min = values[where(values>0.0)[0]].min()
#         print values_min
#         new_name = name
#         if object <> self.gcs:
#             new_name="aggregated_"+name
#             self.gcs.join(object,name, new_name=new_name)
#         self.gcs.r_image(new_name, min_value=values_min, main=main)
        
#     def write_gridcells_results(self, names, base, type, place=""):
#         out_storage = StorageCreator().build_storage(base=base, type=type)
        
#         self.gcs.write_dataset(out_storage=out_storage, out_place=place, attributes=names)
    def compute_indicators_and_write_results(self, names, base, type, subdir=""):
        print "Compute indicators"
        self.indicators.compute_all(resources=self.resources)
        self.gcs.join(self.indicators.get_dataset("zone"),"average_income", \
                      new_name="aggregated_average_income")
        print "Store indicators"
        out_storage = StorageCreator().build_storage(base=base, type=type)
        self.indicators.write(storages=out_storage, places={"zone":subdir+"/zone", \
            "gridcell":subdir+"/"+PSRC_Settings.gcsubdir})
        self.gcs.write_dataset(out_storage=out_storage, out_place=subdir+"/"+PSRC_Settings.gcsubdir, \
            attributes=["aggregated_average_income", "relative_x", "relative_y"])
        self.hhs.write_dataset(out_storage=out_storage, out_place=subdir+"/"+PSRC_Settings.hhsubdir)
        
    def delete_variables(self):
        self.gcs.delete_derived_attributes()
        self.hhs.delete_derived_attributes()
        self.data_objects["zone"].delete_derived_attributes()
        
class PlotPSRCResults:
    def __init__(self, indicator):
        from rpy import r 
        r.postscript(file="PSRC_base_zones_"+indicator+".ps")
#        r.par(mfrow=r.c(2,1))
        gcs = GridcellSet(in_base = PSRC_Settings.outputdir, in_storage_type="flt", \
                in_place="base/" + PSRC_Settings.gcsubdir)
        gcs.r_image(indicator, min_value=10000, max_value=150000, main="base year for zones")
        gcs30 = GridcellSet(in_base = PSRC_Settings.outputdir, in_storage_type="flt", \
                in_place="year_30/" + PSRC_Settings.gcsubdir)
        gcs30.r_image(indicator, min_value=10000, max_value=150000, main="after 30 years (zones)")
        r.dev_off()
        
if __name__ == "__main__":
#    choices = TestHLCModelEugene().run(["residential_units_when_household_has_children", "cost_to_income_ratio"], debuglevel=3)
    sim = Run_PSRCsimulation_and_map_results(variables=[], indicators=[("gridcell","average_income"),\
            ("zone", "average_income")], \
            years=1, debuglevel=3)

#    PlotPSRCResults(indicator="aggregated_average_income")

