# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class regionTool(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self,canvas)
        self.dragging=False
        self.selectRect = QRect()
        self.rubberBand = 0
        self.canvas=canvas
        self.ll = None
        self.ur = None
        self.o = QObject()
        self.cursor = QCursor(QPixmap(["16 16 3 1","# c None","a c #000000",". c #ffffff",".###############","...#############",".aa..###########","#.aaa..a.a.a.a.#","#.aaaaa..#####a#","#a.aaaaaa..###.#","#..aaaaaa...##a#","#a.aaaaa.#####.#","#.#.aaaaa.####a#","#a#.aa.aaa.###.#","#.##..#..aa.##a#","#a##.####.aa.#.#","#.########.aa.a#","#a#########.aa..","#.a.a.a.a.a..a.#","#############.##"]))


    def canvasPressEvent(self,event):
        #print "got an event"
        self.selectRect.setRect(event.pos().x(),event.pos().y(),0,0)
        #print event.pos().x(),event.pos().y()
        transform = self.canvas.getCoordinateTransform()
        coord = transform.toMapCoordinates(event.pos().x(),event.pos().y())
        #print coord.x(), coord.y()

    def canvasMoveEvent(self,event):
        if not event.buttons() == Qt.LeftButton:
            return
        if not self.dragging:
            self.dragging=True
            self.rubberBand = QRubberBand(QRubberBand.Rectangle,self.canvas)
        self.selectRect.setBottomRight(event.pos())
        self.rubberBand.setGeometry(self.selectRect.normalized())
        self.rubberBand.show()

    def canvasReleaseEvent(self,e):
        if not self.dragging:
            return
        self.rubberBand.hide()
        self.selectRect.setRight(e.pos().x())
        self.selectRect.setBottom(e.pos().y())
        transform = self.canvas.getCoordinateTransform()
        ll = transform.toMapCoordinates(self.selectRect.left(),self.selectRect.bottom())
        ur = transform.toMapCoordinates(self.selectRect.right(),self.selectRect.top())
        self.bb = QgsRect(
            QgsPoint(ll.x(),ll.y()),
            QgsPoint(ur.x(),ur.y())
            )
        self.o.emit(SIGNAL("finished()"))
#        self.msg.hide()


#    def activate(self):
#        self.msg = QLabel("Draw rectangle on canvas")
#        self.msg.show()
#        self.canvas.setCursor(self.cursor)


    def deactivate(self):
        pass
        #print "Deactivate!"


    def isZoomTool(self):
        return False





