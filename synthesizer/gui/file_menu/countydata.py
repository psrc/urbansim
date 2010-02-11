# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cPickle

class County(object):
    def __init__(self, stateID, state, countyID, county):
        self.stateID = stateID
        self.stateName = state
        self.countyID = countyID
        self.countyName = county


class CountyContainer(object):
    def __init__(self, filename=QString()):
        self.filename = filename
        self.counties = {}
        self.countyNames = set()
        self.stateNames = set()

    def __len__(self):
        return len(self.counties)

    def __iter__(self):
        for county in self.counties.values():
            yield county

    def inOrder(self):
        return sorted(self.ships.values())

    def inStateOrder(self):
        def compare(a,b):
            if a.state != b.state:
                return QString.localeAwareCompare(a.state, b.state)
            #print a.county, b.county
            return QString.localAwareCompare(a.county, b.county)
        return sorted(self.counties.values(), compare)

    def load(self):
        exception = None
        file = None
        try:
            file = QFile(self.filename)

            if not file.open(QIODevice.ReadOnly):
                raise IOError, unicode(file.errorString())

            while not file.atEnd():
                a = file.readLine()
                a = a.split(",")
                stateID = int(a[0])
                stateName = a[1]
                countyID = int(a[2])
                countyName = a[3]
                county = County(stateID, stateName, countyID, countyName)
                self.counties[id(county)] = county
                self.countyNames.add(countyName)
                self.stateNames.add(stateName)
        except IOError, e:
            exception = e
        finally:
            if file is not None:
                file.close()
            if exception is not None:
                raise exception











