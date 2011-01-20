# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import Qt, QString
from PyQt4.QtGui import QFont, QFontMetrics, QColor, QIcon, QLabel, QWidget, QVBoxLayout
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

# Main
class EditorBase(QsciScintilla):
    def __init__(self, mainwindow):
        QsciScintilla.__init__(self, mainwindow)
        self.mainwindow = mainwindow
        ## define the font to use
        font = QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(10)
        # the font metrics here will help
        # building the margin width later
        fm = QFontMetrics(font)

        ## set the default font of the editor
        ## and take the same font for line numbers
        self.setFont(font)
        self.setMarginsFont(font)

        ## Line numbers
        # conventionnaly, margin 0 is for line numbers
        self.setMarginWidth(0, fm.width( "00000" ) + 5)
        self.setMarginLineNumbers(0, True)

        ## Edge Mode shows a red vetical bar at 80 chars
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QColor("#CCCCCC"))

        ## Folding visual : we will use boxes
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ## Editing line color
        #self.setCaretLineVisible(True)
        #self.setCaretLineBackgroundColor(QColor("#CDA869"))

        ## Margins colors
        # line numbers margin
        self.setMarginsBackgroundColor(QColor("#333333"))
        self.setMarginsForegroundColor(QColor("#CCCCCC"))

        # folding margin colors (foreground,background)
        #self.setFoldMarginColors(QColor("#99CC66"),QColor("#333300"))
        self.setFoldMarginColors(QColor("#CCCCCC"),QColor("#CCCCCC"))

        ## Choose a lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

class EditorTab(object):
    def __init__(self, mainwindow, filePath):
        self.mainwindow = mainwindow

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "Editor Dyn Tab"

        self.tab = QWidget(self.mainwindow)

        self.widgetLayout = QVBoxLayout(self.tab)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.editorStatusLabel = QLabel(self.tab)
        self.editorStatusLabel.setAlignment(Qt.AlignCenter)
        self.editorStatusLabel.setObjectName("editorStatusLabel")
        self.editorStatusLabel.setText(QString("No files currently loaded..."))
        self.widgetLayout.addWidget(self.editorStatusLabel)
        self.editorStuff = EditorBase(self.mainwindow)
        self.widgetLayout.addWidget(self.editorStuff)
        try:
            f = open(filePath,'r')
        except:
            return
        for l in f.readlines():
            self.editorStuff.append(l)
        f.close()
        self.editorStatusLabel.setText(QString(filePath))

        self.mainwindow.tabWidget.insertTab(0,self.tab,self.tabIcon,self.tabLabel)
        self.mainwindow.tabWidget.setCurrentIndex(0)

