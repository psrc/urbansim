# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from collections import defaultdict

from misc.zipfile import ZipFile
import os

class UnzipFile:
    def __init__(self, mountpoint, file):
        self.mountpoint = mountpoint

        self.mountpoint = os.path.realpath(self.mountpoint)
        self.mountpoint = self.mountpoint.replace("\\", "/")

        self.filename = os.path.join(self.mountpoint, file)

    def unzip(self):
        zipObject = ZipFile(self.filename)

        archFiles = zipObject.namelist()

        for i in archFiles:
            fileArchInfo = zipObject.getinfo(i)
            try:
                fileExtrInfo = os.stat(os.path.join(self.mountpoint, i))
                reply = QMessageBox.question(None, "Extracting Data",
                                             QString("""Would you like to replace the existing file <font color = brown>"""
                                                     """%s (size %s) </font>"""
                                                     """ with the file <font color = blue>%s (size %s)</font>"""
                                                     """ from the zip folder?"""
                                             %(i, fileExtrInfo.st_size, i, fileArchInfo.file_size)),
                                             QMessageBox.Yes| QMessageBox.YesToAll|
                                             QMessageBox.No| QMessageBox.NoToAll)
                if reply == QMessageBox.Yes:
                    zipObject.extract(fileArchInfo, self.mountpoint)
                if reply == QMessageBox.YesToAll:
                    index = archFiles.index(i)
                    for j in archFiles[index:]:
                        fileArchInfo = zipObject.getinfo(j)
                        zipObject.extract(fileArchInfo, self.mountpoint)
                    break

                if reply == QMessageBox.NoToAll:
                    break

            except Exception, e:
                zipObject.extract(fileArchInfo, self.mountpoint)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    a = UnzipFile('C:\\PopGen\\data\\California\\PUMS', 'all_California.zip')
    a.unzip()




