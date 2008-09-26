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
# 



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QObject, SIGNAL

class OpusFileAction(object):
    def __init__(self, xmlFileObject, listen_to_menu = True):
        self.xmlFileObject = xmlFileObject

        self.currentColumn = None
        self.currentIndex = None
        self.classification = ""

        if listen_to_menu:
            QObject.connect(self.xmlFileObject.treeview,
                            SIGNAL("customContextMenuRequested(const QPoint &)"),
                            self.processCustomMenu)

    def processCustomMenu(self, position):
        raise Exception('Method processCustomMenu is not implemented')
