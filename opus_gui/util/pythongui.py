# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from PyQt4.QtCore import QObject, SIGNAL, QString
from PyQt4.QtGui import QTextBrowser, QFont
# General system includes
import sys
from code import InteractiveConsole

class OpusPythonShell(QTextBrowser):
    class Output:
        def __init__( self, writefunc ):
            self.writefunc = writefunc
        def write( self, line ):
            if line != "\n":
                map( self.writefunc, line.split("\n") )

    def __init__( self, parent, cmdline, localdict={} ):
        QTextBrowser.__init__( self, parent )
        QObject.connect( cmdline, SIGNAL( "returnPressed()" ),
                         self.returnPressed )
        self.setFont(QFont("Fixed",10))
        self.console = InteractiveConsole( localdict )
        self.cmdline = cmdline
        sys.ps1 = ">>> "
        sys.ps2 = "... "
        self.append("---- OpusPython ----")
        self.append( "Python %s on %s\n" % ( sys.version, sys.platform) )
        self.append("--------")
        self.more, self.prompt = 0, sys.ps1
        self.output = OpusPythonShell.Output(self.writeResult)
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def writeResult( self, result ):
        if result == "":
            return
        self.append( result )

    def processInput( self, line ):
        self.append( sys.ps1 + line )
        sys.stdout, sys.stderr = self.output, self.output
        self.more = self.console.push(line)
        sys.stdout, sys.stderr = self.stdout, self.stderr

    def returnPressed( self ):
        line = str(self.cmdline.text())
        self.cmdline.clear()
        self.processInput( line )
        self.append( QString("--------") )
