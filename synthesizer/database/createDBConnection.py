# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtSql import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from gui.file_menu.newproject import DBInfo

class createDBC(object):
    def __init__(self, db, name=None):
        super(createDBC, self).__init__()

        if name is not None:
            if not QSqlDatabase.contains(name):
                self.dbc = QSqlDatabase.addDatabase(db.driver, name)
            else:
                self.dbc = QSqlDatabase.database(name)

            self.dbc.setDatabaseName(name)
        else:
            self.dbc = QSqlDatabase.addDatabase(db.driver)
        self.dbc.setHostName(db.hostname)
        self.dbc.setUserName(db.username)
        self.dbc.setPassword(db.password)



def main():
    app = QApplication(sys.argv)

    db = DBInfo("localhost", "root", "1234")
    a = createDBC(db, "fayken1")

    
    try:
        if not a.dbc.open():
            QMessageBox.warning(None, "oisdf", 
                                QString("Database Error: %1").arg(a.dbc.lastError().text()))

            query = QSqlQuery()
            if not query.exec_("""show tables"""):
                raise Exception, query.lastError().text()

            sys.exit(1)
            a.dbc.close()
        else:
            QMessageBox.warning(None, "oisdf", 
                                QString("Found"))

            b = createDBC(db, "fayken1")
            b.dbc.open()
            print 'duplicatewqeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
            b.dbc.close()
            a.dbc.close()
    except Exception, e:
        print "Error: %s" %e

    


if __name__=="__main__":


    main()


        
        
        
