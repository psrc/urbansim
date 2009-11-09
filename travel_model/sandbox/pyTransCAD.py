# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# -*- coding: mbcs -*-
# Created by makepy.py version 0.4.95
# By python version 2.4.3 (#69, Mar 29 2006, 17:35:34) [MSC v.1310 32 bit (Intel)]
# From type library 'tcw.tlb'
# On Sat Aug 05 02:09:22 2006
"""TransCAD Type Library"""
makepy_version = '0.4.95'
python_version = 0x20403f0

import win32com.client.CLSIDToClass, pythoncom
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{AD38C0E3-40E9-11D1-9288-00609753E196}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IMacroVal(DispatchBaseClass):
    """Definition of interface IID_IMacroVal"""
    CLSID = IID('{AD38C0E5-40E9-11D1-9288-00609753E196}')
    coclass_clsid = None

    def Copy(self):
        """Get a copy of a value"""
        ret = self._oleobj_.InvokeTypes(1610743835, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'Copy', None, UnicodeToString=0)
        return ret

    def IsEqual(self, compare=defaultNamedNotOptArg):
        """Check if two items are equal"""
        return self._oleobj_.InvokeTypes(1610743836, LCID, 1, (3, 0), ((9, 1),),compare
            )

    _prop_map_get_ = {
        "Angle": (1610743819, 2, (5, 0), (), "Angle", None),
        "Blue": (1610743827, 2, (3, 0), (), "Blue", None),
        "Center": (1610743812, 2, (9, 0), (), "Center", None),
        "ColIndex": (1610743834, 2, (8, 0), (), "ColIndex", None),
        "Core": (1610743832, 2, (8, 0), (), "Core", None),
        "Green": (1610743825, 2, (3, 0), (), "Green", None),
        "Height": (1610743817, 2, (5, 0), (), "Height", None),
        "Lat": (1610743810, 2, (3, 0), (), "Lat", None),
        "Links": (1610743830, 2, (3, 0), (), "Links", None),
        "Lon": (1610743808, 2, (3, 0), (), "Lon", None),
        "Matrix": (1610743831, 2, (9, 0), (), "Matrix", None),
        "Nodes": (1610743829, 2, (3, 0), (), "Nodes", None),
        "Projection": (1610743821, 2, (9, 0), (), "Projection", None),
        "Radius": (1610743814, 2, (5, 0), (), "Radius", None),
        "Red": (1610743823, 2, (3, 0), (), "Red", None),
        "RowIndex": (1610743833, 2, (8, 0), (), "RowIndex", None),
        "Width": (1610743815, 2, (5, 0), (), "Width", None),
    }
    _prop_map_put_ = {
        "Angle": ((1610743819, LCID, 4, 0),()),
        "Blue": ((1610743827, LCID, 4, 0),()),
        "Center": ((1610743812, LCID, 4, 0),()),
        "Green": ((1610743825, LCID, 4, 0),()),
        "Height": ((1610743817, LCID, 4, 0),()),
        "Lat": ((1610743810, LCID, 4, 0),()),
        "Lon": ((1610743808, LCID, 4, 0),()),
        "Projection": ((1610743821, LCID, 4, 0),()),
        "Red": ((1610743823, LCID, 4, 0),()),
        "Width": ((1610743815, LCID, 4, 0),()),
    }

class ITransCAD(DispatchBaseClass):
    """Definition of interface IID_ITransCAD"""
    CLSID = IID('{AD38C0E2-40E9-11D1-9288-00609753E196}')
    coclass_clsid = IID('{AD38C0E0-40E9-11D1-9288-00609753E196}')

    def Circle(self, Center=defaultNamedNotOptArg, Radius=defaultNamedNotOptArg):
        """Create a Circle"""
        ret = self._oleobj_.InvokeTypes(1610743809, LCID, 1, (9, 0), ((9, 1), (5, 1)),Center
            , Radius)
        if ret is not None:
            ret = Dispatch(ret, 'Circle', None, UnicodeToString=0)
        return ret

    def Coord(self, longitude=defaultNamedNotOptArg, latitude=defaultNamedNotOptArg):
        """Create a Coord"""
        ret = self._oleobj_.InvokeTypes(1610743808, LCID, 1, (9, 0), ((3, 1), (3, 1)),longitude
            , latitude)
        if ret is not None:
            ret = Dispatch(ret, 'Coord', None, UnicodeToString=0)
        return ret

    def Function(self, macroname=defaultNamedNotOptArg, arg1=defaultNamedOptArg, arg2=defaultNamedOptArg, arg3=defaultNamedOptArg
            , arg4=defaultNamedOptArg, arg5=defaultNamedOptArg, arg6=defaultNamedOptArg, arg7=defaultNamedOptArg, arg8=defaultNamedOptArg
            , arg9=defaultNamedOptArg):
        """Run a GISDK Function"""
        return self._ApplyTypes_(1610743812, 1, (12, 0), ((8, 1), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)), 'Function', None,macroname
            , arg1, arg2, arg3, arg4, arg5
            , arg6, arg7, arg8, arg9)

    def Lock(self):
        """Set the lock flag"""
        return self._oleobj_.InvokeTypes(1610743815, LCID, 1, (3, 0), (),)

    def LockTime(self):
        """Return the time since the lock flag was last set"""
        return self._oleobj_.InvokeTypes(1610743817, LCID, 1, (5, 0), (),)

    def Macro(self, macroname=defaultNamedNotOptArg, dbname=defaultNamedNotOptArg, arg1=defaultNamedOptArg, arg2=defaultNamedOptArg
            , arg3=defaultNamedOptArg, arg4=defaultNamedOptArg, arg5=defaultNamedOptArg, arg6=defaultNamedOptArg, arg7=defaultNamedOptArg
            , arg8=defaultNamedOptArg, arg9=defaultNamedOptArg):
        """Run a Macro or DBox in a GISDK User Interface Database"""
        return self._ApplyTypes_(1610743814, 1, (12, 0), ((8, 1), (8, 1), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)), 'Macro', None,macroname
            , dbname, arg1, arg2, arg3, arg4
            , arg5, arg6, arg7, arg8, arg9
            )

    def RunMacro(self, macroname=defaultNamedNotOptArg, arg1=defaultNamedOptArg, arg2=defaultNamedOptArg, arg3=defaultNamedOptArg
            , arg4=defaultNamedOptArg, arg5=defaultNamedOptArg, arg6=defaultNamedOptArg, arg7=defaultNamedOptArg, arg8=defaultNamedOptArg
            , arg9=defaultNamedOptArg):
        """Run a GISDK Function"""
        return self._ApplyTypes_(1610743811, 1, (12, 0), ((8, 1), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)), 'RunMacro', None,macroname
            , arg1, arg2, arg3, arg4, arg5
            , arg6, arg7, arg8, arg9)

    def RunUIMacro(self, macroname=defaultNamedNotOptArg, dbname=defaultNamedNotOptArg, arg1=defaultNamedOptArg, arg2=defaultNamedOptArg
            , arg3=defaultNamedOptArg, arg4=defaultNamedOptArg, arg5=defaultNamedOptArg, arg6=defaultNamedOptArg, arg7=defaultNamedOptArg
            , arg8=defaultNamedOptArg, arg9=defaultNamedOptArg):
        """Run a Macro or DBox in a GISDK User Interface Database"""
        return self._ApplyTypes_(1610743813, 1, (12, 0), ((8, 1), (8, 1), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)), 'RunUIMacro', None,macroname
            , dbname, arg1, arg2, arg3, arg4
            , arg5, arg6, arg7, arg8, arg9
            )

    def Scope(self, Center=defaultNamedNotOptArg, Width=defaultNamedNotOptArg, Height=defaultNamedNotOptArg, Angle=defaultNamedNotOptArg):
        """Create a Scope"""
        ret = self._oleobj_.InvokeTypes(1610743810, LCID, 1, (9, 0), ((9, 1), (5, 1), (5, 1), (5, 1)),Center
            , Width, Height, Angle)
        if ret is not None:
            ret = Dispatch(ret, 'Scope', None, UnicodeToString=0)
        return ret

    def Unlock(self):
        """Free the lock flag"""
        return self._oleobj_.InvokeTypes(1610743816, LCID, 1, (24, 0), (),)

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'TransCAD.AutomationServer'
class TransCAD(CoClassBaseClass): # A CoClass
    # TransCAD Object Type Information
    CLSID = IID('{AD38C0E0-40E9-11D1-9288-00609753E196}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        ITransCAD,
    ]
    default_interface = ITransCAD

IMacroVal_vtables_dispatch_ = 1
IMacroVal_vtables_ = [
    (( 'Lon' , 'longitude' , ), 1610743808, (1610743808, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'Lon' , 'longitude' , ), 1610743808, (1610743808, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'Lat' , 'latitude' , ), 1610743810, (1610743810, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
    (( 'Lat' , 'latitude' , ), 1610743810, (1610743810, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
    (( 'Center' , 'Center' , ), 1610743812, (1610743812, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 44 , (3, 0, None, None) , 0 , )),
    (( 'Center' , 'Center' , ), 1610743812, (1610743812, (), [ (9, 1, None, None) , ], 1 , 4 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
    (( 'Radius' , 'Radius' , ), 1610743814, (1610743814, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 52 , (3, 0, None, None) , 0 , )),
    (( 'Width' , 'Width' , ), 1610743815, (1610743815, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
    (( 'Width' , 'Width' , ), 1610743815, (1610743815, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
    (( 'Height' , 'Height' , ), 1610743817, (1610743817, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
    (( 'Height' , 'Height' , ), 1610743817, (1610743817, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 68 , (3, 0, None, None) , 0 , )),
    (( 'Angle' , 'Angle' , ), 1610743819, (1610743819, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
    (( 'Angle' , 'Angle' , ), 1610743819, (1610743819, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 76 , (3, 0, None, None) , 0 , )),
    (( 'Projection' , 'Angle' , ), 1610743821, (1610743821, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
    (( 'Projection' , 'Angle' , ), 1610743821, (1610743821, (), [ (9, 1, None, None) , ], 1 , 4 , 4 , 0 , 84 , (3, 0, None, None) , 0 , )),
    (( 'Red' , 'Red' , ), 1610743823, (1610743823, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
    (( 'Red' , 'Red' , ), 1610743823, (1610743823, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 92 , (3, 0, None, None) , 0 , )),
    (( 'Green' , 'Green' , ), 1610743825, (1610743825, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
    (( 'Green' , 'Green' , ), 1610743825, (1610743825, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 100 , (3, 0, None, None) , 0 , )),
    (( 'Blue' , 'Blue' , ), 1610743827, (1610743827, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
    (( 'Blue' , 'Blue' , ), 1610743827, (1610743827, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 108 , (3, 0, None, None) , 0 , )),
    (( 'Nodes' , 'Nodes' , ), 1610743829, (1610743829, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
    (( 'Links' , 'Links' , ), 1610743830, (1610743830, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 116 , (3, 0, None, None) , 0 , )),
    (( 'Matrix' , 'Matrix' , ), 1610743831, (1610743831, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
    (( 'Core' , 'Core' , ), 1610743832, (1610743832, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 124 , (3, 0, None, None) , 0 , )),
    (( 'RowIndex' , 'rowidx' , ), 1610743833, (1610743833, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
    (( 'ColIndex' , 'colidx' , ), 1610743834, (1610743834, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 132 , (3, 0, None, None) , 0 , )),
    (( 'Copy' , 'value' , ), 1610743835, (1610743835, (), [ (16393, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
    (( 'IsEqual' , 'compare' , 'result' , ), 1610743836, (1610743836, (), [ (9, 1, None, None) , 
            (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 140 , (3, 0, None, None) , 0 , )),
]

ITransCAD_vtables_dispatch_ = 1
ITransCAD_vtables_ = [
    (( 'Coord' , 'longitude' , 'latitude' , 'Coord' , ), 1610743808, (1610743808, (), [ 
            (3, 1, None, None) , (3, 1, None, None) , (16393, 10, None, None) , ], 1 , 1 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'Circle' , 'Center' , 'Radius' , 'Circle' , ), 1610743809, (1610743809, (), [ 
            (9, 1, None, None) , (5, 1, None, None) , (16393, 10, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'Scope' , 'Center' , 'Width' , 'Height' , 'Angle' , 
            'Circle' , ), 1610743810, (1610743810, (), [ (9, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
            (5, 1, None, None) , (16393, 10, None, None) , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
    (( 'RunMacro' , 'macroname' , 'arg1' , 'arg2' , 'arg3' , 
            'arg4' , 'arg5' , 'arg6' , 'arg7' , 'arg8' , 
            'arg9' , 'ret' , ), 1610743811, (1610743811, (), [ (8, 1, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (16396, 10, None, None) , ], 1 , 1 , 4 , 9 , 40 , (3, 0, None, None) , 0 , )),
    (( 'Function' , 'macroname' , 'arg1' , 'arg2' , 'arg3' , 
            'arg4' , 'arg5' , 'arg6' , 'arg7' , 'arg8' , 
            'arg9' , 'ret' , ), 1610743812, (1610743812, (), [ (8, 1, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (16396, 10, None, None) , ], 1 , 1 , 4 , 9 , 44 , (3, 0, None, None) , 0 , )),
    (( 'RunUIMacro' , 'macroname' , 'dbname' , 'arg1' , 'arg2' , 
            'arg3' , 'arg4' , 'arg5' , 'arg6' , 'arg7' , 
            'arg8' , 'arg9' , 'ret' , ), 1610743813, (1610743813, (), [ (8, 1, None, None) , 
            (8, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (16396, 10, None, None) , ], 1 , 1 , 4 , 9 , 48 , (3, 0, None, None) , 0 , )),
    (( 'Macro' , 'macroname' , 'dbname' , 'arg1' , 'arg2' , 
            'arg3' , 'arg4' , 'arg5' , 'arg6' , 'arg7' , 
            'arg8' , 'arg9' , 'ret' , ), 1610743814, (1610743814, (), [ (8, 1, None, None) , 
            (8, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
            (16396, 10, None, None) , ], 1 , 1 , 4 , 9 , 52 , (3, 0, None, None) , 0 , )),
    (( 'Lock' , 'rslt' , ), 1610743815, (1610743815, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
    (( 'Unlock' , ), 1610743816, (1610743816, (), [ ], 1 , 1 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
    (( 'LockTime' , 'rslt' , ), 1610743817, (1610743817, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
    '{AD38C0E0-40E9-11D1-9288-00609753E196}' : TransCAD,
    '{AD38C0E2-40E9-11D1-9288-00609753E196}' : ITransCAD,
    '{AD38C0E5-40E9-11D1-9288-00609753E196}' : IMacroVal,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{AD38C0E2-40E9-11D1-9288-00609753E196}' : 'ITransCAD',
    '{AD38C0E5-40E9-11D1-9288-00609753E196}' : 'IMacroVal',
}


NamesToIIDMap = {
    'IMacroVal' : '{AD38C0E5-40E9-11D1-9288-00609753E196}',
    'ITransCAD' : '{AD38C0E2-40E9-11D1-9288-00609753E196}',
}

