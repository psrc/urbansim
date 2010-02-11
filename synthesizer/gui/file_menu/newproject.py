# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from __future__ import with_statement
from collections import defaultdict

import pickle, numpy

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gui.global_vars  import *


class Geocorr(object):
    def __init__(self, userprov=None, geocorrLocation=""):
        self.userProv = userprov
        self.location = geocorrLocation

class Sample(object):
    def __init__(self, userprov=None, defSource="", sampleHHLocation="", sampleGQLocation="", samplePersonLocation=""):
        self.userProv = userprov
        self.defSource = defSource
        self.hhLocation = sampleHHLocation
        self.gqLocation = sampleGQLocation
        self.personLocation = samplePersonLocation

class Control(object):
    def __init__(self, userprov=None, defSource="", controlHHLocation="", controlGQLocation="", controlPersonLocation=""):
        self.userProv = userprov
        self.defSource = defSource
        self.hhLocation = controlHHLocation
        self.gqLocation = controlGQLocation
        self.personLocation = controlPersonLocation

class DBInfo(object):
    def __init__(self, hostname="", username="", password="", driver="QMYSQL"):
        self.driver = driver
        self.hostname = hostname
        self.username = username
        self.password = password


class SelectedVariableDicts(object):
    def __init__(self, hhldVariables=defaultdict(dict), gqVariables=defaultdict(dict), personVariables=defaultdict(dict),
                 persControl=True, hhldMargsModify=False, hhldSizeVarName="", aveHhldSizeLastCat="", refPersName=""):
        self.hhld = hhldVariables
        self.gq = gqVariables
        self.person = personVariables
        self.persControl = persControl
        self.hhldMargsModify = hhldMargsModify
        self.hhldSizeVarName = hhldSizeVarName
        self.aveHhldSizeLastCat = aveHhldSizeLastCat
        self.refPersName = refPersName



class AdjControlsDicts(object):
    def __init__(self, hhldAdj=defaultdict(dict), gqAdj=defaultdict(dict), personAdj=defaultdict(dict)):
        self.hhld = hhldAdj
        self.gq = gqAdj
        self.person = personAdj


class Geography(object):
    def __init__(self, state, county, tract, bg, puma5=None):
        self.state = state
        self.county = county
        self.tract = tract
        self.bg = bg
        self.puma5 = puma5


class Parameters(object):
    def __init__(self,
                 ipfTol=IPF_TOLERANCE,
                 ipfIter=IPF_MAX_ITERATIONS,
                 ipuTol=IPU_TOLERANCE,
                 ipuIter=IPU_MAX_ITERATIONS,
                 synPopDraws=SYNTHETIC_POP_MAX_DRAWS,
                 synPopPTol=SYNTHETIC_POP_PVALUE_TOLERANCE,
                 roundingProcedure=ROUNDING_PROCEDURE):

        self.ipfTol = ipfTol
        self.ipfIter = ipfIter
        self.ipuTol = ipuTol
        self.ipuIter = ipuIter
        self.synPopDraws = synPopDraws
        self.synPopPTol = synPopPTol
        self.roundingProcedure = roundingProcedure



class NewProject(object):
    def __init__(self, name="", filename="", location="", description="",
                 region="", state="", countyCode="", stateCode="", stateAbb="",
                 resolution="", geocorrUserProv=Geocorr(),
                 sampleUserProv=Sample(), controlUserProv=Control(),
                 db=DBInfo(), scenario=1, parameters=Parameters(), controlVariables=SelectedVariableDicts(),
                 adjControls = AdjControlsDicts(),
                 hhldVars=None, hhldDims=None, gqVars=None, gqDims=None, personVars=None, personDims=None, geoIds={}):
        self.name = name
        self.filename = name + 'scenario' + str(scenario)
        self.location = location
        self.description = description
        self.region = region
        self.state = state
        self.countyCode = countyCode
        self.stateCode = stateCode
        self.stateAbb = stateAbb
        self.resolution = resolution
        self.geocorrUserProv = geocorrUserProv
        self.sampleUserProv = sampleUserProv
        self.controlUserProv = controlUserProv
        self.db = db
        self.scenario = scenario
        self.parameters = parameters
        self.selVariableDicts = controlVariables
        self.adjControlsDicts = adjControls
        self.hhldVars = hhldVars
        self.hhldDims = hhldDims
        self.gqVars = gqVars
        self.gqDims = gqDims
        self.personVars = personVars
        self.personDims = personDims
        self.synGeoIds = geoIds

    def save(self):
        self.filename = self.name + 'scenario' + str(self.scenario)
        #print self.filename

        with open('%s/%s/%s.pop' %(self.location, self.name, self.filename),
                  'wb') as f:
            pickle.dump(self, f, True)


    def update(self):
        pass



if __name__ == "__main__":
    a = ControlVariable()

    print dir(a)
    print type(a)



