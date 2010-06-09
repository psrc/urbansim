"""This module allows programs to work with dBase III and VFP 6 type tables."""
###############################################################################################
# dbf -- Python package for reading/writing dBase III and VFP 6 tables and memos
# Author: Ethan Furman (ethanf@admailinc.com)
# Copyright (c) 2008, Ad-Mail, Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Ad-Mail, Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Ad-Mail, Inc ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Ad-Mail, Inc BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################################
#
# The entire table is read into memory, and all operations occur on the in-memory table, with
# data changes being written to disk as they occur.
#
# Goals:  programming style with databases
# functions that change the current record will use the currently active index, which defaults
# to physical order.
#
#   table = dbf.table('table name'[, fielddesc[, fielddesc[, ....]]])
#           fielddesc examples:  name C(30), age N(3.0), wisdom M, marriage D
#   record = [ table.current() | table[int] | table.append() | table.[next|prev|top|bottom|goto]() ]
#   record.field or record['field'] accesses the field
#
# Table Functions:
#
#   addFields(fieldspec):
#       adds field(s) to the table layout; format is Name Type(Length.Decimals)[, Name Type(Length.Decimals)[...]]
#
#   append(dict={}, drop=False, kamikaze='', multiple=1):
#       adds <multiple> blank records, and fills fields with dict values if present
#
#   bottom():
#       sets record pointer to last (non-deleted) record; raises DbfError if table is empty,
#       Bof if all records deleted and useDeleted is False
#
#   close():
#        closes disk files, releases table
#
#   current():
#       returns current logical record
#
#   deleteRecord():
#       marks record as deleted
#
#   deleteFields(fields):
#       removes field(s) from the table
#
#   export(filename='', fieldlist='', format='csv', header=True):
#       writes the table using CSV or tab-delimited format, using the filename
#       given if specified, otherwise the table name
#
#   find(match, dictionary=False, recordnumber=False, contained=False):
#       searches through table looking for records that match all the criteria in match,
#       which is a dictionary of fieldname, value pairs.  Brute force search of entire table.
#
#   hasBeenDeleted():
#       returns True if record is deleted
#
#   gatherFields(dict, drop=False):
#       saves a dictionary into a records fields
#       keys with no matching field will raise a FieldMissing exception unless drop = True
#
#   goto(match):
#       changes the record pointer to the first matching record
#       match should be either a dictionary of name:value pairs, or
#       an integer to go to
#
#   new(filename, _fieldlist=''):
#       returns a new table of the same type (dBase, Vfp, etc.)
#
#   next():
#       set record pointer to next (non-deleted) record
#
#   order(fields='ORIGINAL'):
#       orders the table using the field(s) provided; removes order if no field provided
#
#   prev():
#       set record pointer to previous (non-deleted) record
#
#   recNum():
#       returns the current logical record number
#
#   renameField(oldname, newname):
#       renames an existing field
#
#   scatterFields(blank=False):
#       returns a dictionary of fieldnames and values which can be used with gather().
#       if Blank is True, values are empty.
#
#   search(match, dictionary=False, recordnumber=False):
#       searches using a binary algorythm looking for records that match the criteria in match,
#       which is a dictionary with a single fieldname, value pair
#       table must be sorted by a single field, whole, field, and only that field can be used
#       for searching
#
#   size(field):
#       returns size of field
#
#   structure():
#       return character list of fields suitable for creating same table layout
#
#   top():
#       sets record pointer to first (non-deleted) record; raises DbfError if table is empty,
#       Eof if all records are deleted and useDeleted is True
#
#   type(field):
#       returns type of field
#
#   undeleteRecord():
#       undeletes current record
#
#   zap(areyousure=False):
#       removes all records from table -- this cannot be undone!
#       areyousure must be True, else error is raised
#
#
# Record Functions:
#
#   deleteRecord()
#       marks record as deleted
#
#   gatherFields(dict, drop=False):
#       saves a dictionary into a record's fields
#       keys with no matching field will raise a FieldMissing exception unless drop=True
#
#   scatterFields(blank=False):
#       returns a dictionary of fieldnames and values which can be used with gatherFields()
#       if blank=True, values are empty
#
#   undeleteRecord():
#       marks record as active
#
#
# NOTE:  Of the VFP data types, auto-increment and null settings are not implemented.
#
###############################################################################################
#
# Module variables:
#   version     --> version of dbf
#
# Publicly accessible table variables (read-only):
#   .filename       --> name of dbf file
#   .memoname       --> name of dbt/fpt file
#   .version        --> type of table
#   .fields         --> list of fields
#   .fieldcount     --> number of fields
#   .record_number  --> current record number
#
# Publicly writable table variables:
#   .useDeleted --> False = ignore deleted records
#
# Publicly accessible record variables (read-only):
#
#   .record_number    --> physical record number
#   .has_been_deleted --> True if record has been marked for deletion
#   .table_fields     --> list of fields
#
# Naming conventions:
#   Class names     --> StudlyCaps
#   Method names    --> mixedCaps
#   Function names  --> mixedCaps
#   Variable names  --> lowercase or lower_case_underscore
#   Parameter names --> lowercase
#
###############################################################################################

import os
import sys
import datetime
import time
import csv
import struct
from decimal import Decimal
import Tkinter as tk

version = (0, 84, 18)

__all__ = ['DbfWarning', 'Bof', 'Eof', 'DbfError', 'FieldMissing', \
           'Table', 'DbfList', 'Date', 'DateTime', 'Time']

# Constants
VFPTIME = 1721425

class DbfCsv(csv.Dialect):
    delimiter = ','
    doublequote = True
    escapechar = None
    lineterminator = '\r\n'
    quotechar = '"'
    skipinitialspace = True
    quoting = csv.QUOTE_NONNUMERIC
csv.register_dialect('dbf', DbfCsv)

class Date(object):
    "adds null capable datetime.date constructs"
    __slots__ = ['_date']
    def __new__(cls, year=None, month=0, day=0):
        """date should be either a datetime.date, a string in yyyymmdd format, 
        or date/month/day should all be appropriate integers"""
        nd = object.__new__(cls)
        nd._date = False
        if type(year) == datetime.date:
            nd._date = year
        elif type(year) == Date:
            nd._date = year._date
        elif year is not None:
            nd._date = datetime.date(year, month, day)
        return nd
    def __add__(yo, other):
        if yo and type(other) == datetime.timedelta:
            return Date(yo._date + other)
        else:
            return NotImplemented
    def __eq__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date == other
            elif type(other) == Date:
                if other:
                    return yo._date == other._date
                return False
        else:
            if type(other) == datetime.date:
                return False
            elif type(other) == Date:
                if other:
                    return False
                return True
        return NotImplemented
    def __getattr__(yo, name):
        if yo:
            attribute = yo._date.__getattribute__(name)
            return attribute
        else:
            raise AttributeError('null Date object has no attribute %s' % name)
    def __ge__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date >= other
            elif type(other) == Date:
                if other:
                    return yo._date >= other._date
                return False
        else:
            if type(other) == datetime.date:
                return False
            elif type(other) == Date:
                if other:
                    return False
                return True
        return NotImplemented
    def __gt__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date > other
            elif type(other) == Date:
                if other:
                    return yo._date > other._date
                return True
        else:
            if type(other) == datetime.date:
                return False
            elif type(other) == Date:
                if other:
                    return False
                return False
        return NotImplemented
    def __hash__(yo):
        return yo._date.__hash__()
    def __le__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date <= other
            elif type(other) == Date:
                if other:
                    return yo._date <= other._date
                return False
        else:
            if type(other) == datetime.date:
                return True
            elif type(other) == Date:
                if other:
                    return True
                return True
        return NotImplemented
    def __lt__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date < other
            elif type(other) == Date:
                if other:
                    return yo._date < other._date
                return False
        else:
            if type(other) == datetime.date:
                return True
            elif type(other) == Date:
                if other:
                    return True
                return False
        return NotImplemented
    def __ne__(yo, other):
        if yo:
            if type(other) == datetime.date:
                return yo._date != other
            elif type(other) == Date:
                if other:
                    return yo._date != other._date
                return True
        else:
            if type(other) == datetime.date:
                return True
            elif type(other) == Date:
                if other:
                    return True
                return False
        return NotImplemented
    def __nonzero__(yo):
        if yo._date:
            return True
        return False
    __radd__ = __add__
    def __rsub__(yo, other):
        if yo and type(other) == datetime.date:
            return other - yo._date
        elif yo and type(other) == Date:
            return other._date - yo._date
        elif yo and type(other) == datetime.timedelta:
            return Date(other - yo._date)
        else:
            return NotImplemented
    def __repr__(yo):
        if yo:
            return "Date(%d, %d, %d)" % yo.timetuple()[:3]
        else:
            return "Date()"
    def __str__(yo):
        if yo:
            return yo.isoformat()
        return "no date"
    def __sub__(yo, other):
        if yo and type(other) == datetime.date:
            return yo._date - other
        elif yo and type(other) == Date:
            return yo._date - other._date
        elif yo and type(other) == datetime.timedelta:
            return Date(yo._date - other)
        else:
            return NotImplemented
    def date(yo):
        if yo:
            return yo._date
        return None
    @classmethod
    def fromordinal(cls, number):
        if number:
            return cls(datetime.date.fromordinal(number))
        return cls()
    @classmethod
    def fromtimestamp(cls, timestamp):
        return cls(datetime.date.fromtimestamp(timestamp))
    @classmethod
    def fromymd(cls, yyyymmdd):
        if yyyymmdd == '        ':
            return cls()
        return cls(datetime.date(int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:])))
    def strftime(yo, format):
        if yo:
            return yo._date.strftime(format)
        return '<no date>'
    @classmethod
    def today(cls):
        return cls(datetime.date.today())
    def ymd(yo):
        if yo:
            return "%04d%02d%02d" % yo.timetuple()[:3]
        else:
            return '        '
Date.max = Date(datetime.date.max)
Date.min = Date(datetime.date.min)
class DateTime(object):
    "adds null capable datetime.datetime constructs"
    __slots__ = ['_datetime']
    def __new__(cls, year=None, month=0, day=0, hour=0, minute=0, second=0, microsec=0):
        """year may be a datetime.datetime"""
        ndt = object.__new__(cls)
        ndt._datetime = False
        if type(year) == datetime.datetime:
            ndt._datetime = year
        elif type(year) == DateTime:
            ndt._datetime = year._datetime
        elif year is not None:
            ndt._datetime = datetime.datetime(year, month, day, hour, minute, second, microsec)
        return ndt
    def __add__(yo, other):
        if yo and type(other) == datetime.timedelta:
            return DateTime(yo._datetime + other)
        else:
            return NotImplemented
    def __eq__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime == other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime == other._datetime
                return False
        else:
            if type(other) == datetime.datetime:
                return False
            elif type(other) == DateTime:
                if other:
                    return False
                return True
        return NotImplemented
    def __getattr__(yo, name):
        if yo:
            attribute = yo._datetime.__getattribute__(name)
            return attribute
        else:
            raise AttributeError('null DateTime object has no attribute %s' % name)
    def __ge__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime >= other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime >= other._datetime
                return False
        else:
            if type(other) == datetime.datetime:
                return False
            elif type(other) == DateTime:
                if other:
                    return False
                return True
        return NotImplemented
    def __gt__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime > other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime > other._datetime
                return True
        else:
            if type(other) == datetime.datetime:
                return False
            elif type(other) == DateTime:
                if other:
                    return False
                return False
        return NotImplemented
    def __hash__(yo):
        return yo._datetime.__hash__()
    def __le__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime <= other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime <= other._datetime
                return False
        else:
            if type(other) == datetime.datetime:
                return True
            elif type(other) == DateTime:
                if other:
                    return True
                return True
        return NotImplemented
    def __lt__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime < other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime < other._datetime
                return False
        else:
            if type(other) == datetime.datetime:
                return True
            elif type(other) == DateTime:
                if other:
                    return True
                return False
        return NotImplemented
    def __ne__(yo, other):
        if yo:
            if type(other) == datetime.datetime:
                return yo._datetime != other
            elif type(other) == DateTime:
                if other:
                    return yo._datetime != other._datetime
                return True
        else:
            if type(other) == datetime.datetime:
                return True
            elif type(other) == DateTime:
                if other:
                    return True
                return False
        return NotImplemented
    def __nonzero__(yo):
        if yo._datetime is not False:
            return True
        return False
    __radd__ = __add__
    def __rsub__(yo, other):
        if yo and type(other) == datetime.datetime:
            return other - yo._datetime
        elif yo and type(other) == DateTime:
            return other._datetime - yo._datetime
        elif yo and type(other) == datetime.timedelta:
            return DateTime(other - yo._datetime)
        else:
            return NotImplemented
    def __repr__(yo):
        if yo:
            return "DateTime(%d, %d, %d, %d, %d, %d, %d, %d, %d)" % yo._datetime.timetuple()[:]
        else:
            return "DateTime()"
    def __str__(yo):
        if yo:
            return yo.isoformat()
        return "no datetime"
    def __sub__(yo, other):
        if yo and type(other) == datetime.datetime:
            return yo._datetime - other
        elif yo and type(other) == DateTime:
            return yo._datetime - other._datetime
        elif yo and type(other) == datetime.timedelta:
            return DateTime(yo._datetime - other)
        else:
            return NotImplemented
    @classmethod
    def combine(cls, date, time):
        if Date(date) and Time(time):
            return cls(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond)
        return cls()
    def date(yo):
        if yo:
            return Date(yo.year, yo.month, yo.day)
        return Date()
    def datetime(yo):
        if yo:
            return yo._datetime
        return None
    @classmethod    
    def fromordinal(cls, number):
        if number:
            return cls(datetime.datetime.fromordinal(number))
        else:
            return cls()
    @classmethod
    def fromtimestamp(cls, timestamp):
        return DateTime(datetime.datetime.fromtimestamp(timestamp))
    @classmethod
    def now(cls):
        return cls(datetime.datetime.now())
    def time(yo):
        if yo:
            return Time(yo.hour, yo.minute, yo.second, yo.microsecond)
        return Time()
    @classmethod
    def utcnow(cls):
        return cls(datetime.datetime.utcnow())
    @classmethod
    def today(cls):
        return cls(datetime.datetime.today())
DateTime.max = DateTime(datetime.datetime.max)
DateTime.min = DateTime(datetime.datetime.min)
class Time(object):
    "adds null capable datetime.time constructs"
    __slots__ = ['_time']
    def __new__(cls, hour=None, minute=0, second=0, microsec=0):
        """hour may be a datetime.time"""
        nt = object.__new__(cls)
        nt._time = False
        if type(hour) == datetime.time:
            nt._time = hour
        elif type(hour) == Time:
            nt._time = hour._time
        elif hour is not None:
            nt._time = datetime.time(hour, minute, second, microsec)
        return nt
    def __add__(yo, other):
        if yo and type(other) == datetime.timedelta:
            return Time(yo._time + other)
        else:
            return NotImplemented
    def __eq__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time == other
            elif type(other) == Time:
                if other:
                    return yo._time == other._time
                return False
        else:
            if type(other) == datetime.time:
                return False
            elif type(other) == Time:
                if other:
                    return False
                return True
        return NotImplemented
    def __getattr__(yo, name):
        if yo:
            attribute = yo._time.__getattribute__(name)
            return attribute
        else:
            raise AttributeError('null Time object has no attribute %s' % name)
    def __ge__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time >= other
            elif type(other) == Time:
                if other:
                    return yo._time >= other._time
                return False
        else:
            if type(other) == datetime.time:
                return False
            elif type(other) == Time:
                if other:
                    return False
                return True
        return NotImplemented
    def __gt__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time > other
            elif type(other) == DateTime:
                if other:
                    return yo._time > other._time
                return True
        else:
            if type(other) == datetime.time:
                return False
            elif type(other) == Time:
                if other:
                    return False
                return False
        return NotImplemented
    def __hash__(yo):
        return yo._datetime.__hash__()
    def __le__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time <= other
            elif type(other) == Time:
                if other:
                    return yo._time <= other._time
                return False
        else:
            if type(other) == datetime.time:
                return True
            elif type(other) == Time:
                if other:
                    return True
                return True
        return NotImplemented
    def __lt__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time < other
            elif type(other) == Time:
                if other:
                    return yo._time < other._time
                return False
        else:
            if type(other) == datetime.time:
                return True
            elif type(other) == Time:
                if other:
                    return True
                return False
        return NotImplemented
    def __ne__(yo, other):
        if yo:
            if type(other) == datetime.time:
                return yo._time != other
            elif type(other) == Time:
                if other:
                    return yo._time != other._time
                return True
        else:
            if type(other) == datetime.time:
                return True
            elif type(other) == Time:
                if other:
                    return True
                return False
        return NotImplemented
    def __nonzero__(yo):
        if yo._time is not False:
            return True
        return False
    __radd__ = __add__
    def __rsub__(yo, other):
        if yo and type(other) == datetime.time:
            return other - yo._time
        elif yo and type(other) == Time:
            return other._time - yo._time
        elif yo and type(other) == datetime.timedelta:
            return Time(other - yo._datetime)
        else:
            return NotImplemented
    def __repr__(yo):
        if yo:
            return "Time(%d, %d, %d, %d)" % (yo.hour, yo.minute, yo.second, yo.microsecond)
        else:
            return "Time()"
    def __str__(yo):
        if yo:
            return yo.isoformat()
        return "no time"
    def __sub__(yo, other):
        if yo and type(other) == datetime.time:
            return yo._time - other
        elif yo and type(other) == Time:
            return yo._time - other._time
        elif yo and type(other) == datetime.timedelta:
            return Time(yo._time - other)
        else:
            return NotImplemented
Time.min = Time(datetime.time.min)
Time.max = Time(datetime.time.max)

version_map = {
        '\x02' : 'FoxBASE',
        '\x03' : 'dBase III Plus',
        '\x04' : 'dBase IV',
        '\x05' : 'dBase V',
        '\x30' : 'Visual FoxPro',
        '\x31' : 'Visual FoxPro (auto increment field)',
        '\x43' : 'dBase IV SQL',
        '\x7b' : 'dBase IV w/memos',
        '\x83' : 'dBase III Plus w/memos',
        '\x8b' : 'dBase IV w/memos',
        '\x8e' : 'dBase IV w/SQL table' }

def Table(filename, fieldlist='', memosize=128, ignore_memos=False, \
          readonly=False, keep_memos=False, metaonly=False, type='db3'):
    type = type.lower()
    if fieldlist:
        if type == 'db3':
            return DbfTable(filename, fieldlist, memosize, ignore_memos)
        elif type == 'vfp':
            return VfpTable(filename, fieldlist, memosize, ignore_memos)
        else:
            raise TypeError("Unknown table type: %s" % type)
    else:
        base, ext = os.path.splitext(filename)
        if ext == '':
            filename = base + '.dbf'
        if not os.path.exists(filename):
            raise DbfError("File %s not found, fieldlist not specified" % filename)
        fd = open(filename)
        version = fd.read(1)
        fd.close()
        fd = None
        if not version in version_map:
            raise TypeError("Unknown dbf type: %x" % ord(version))
        for tabletype in (DbfTable, VfpTable):
            if version in tabletype._supported_tables:
                return tabletype(filename, fieldlist, memosize, ignore_memos, \
                                 readonly, keep_memos, metaonly)
        else:
            raise TypeError("Tables of type <%s [%x]> are not supported." % (version_map.get(version, 'Unknown: %s' % version), ord(version)))
def tableType(filename):
    base, ext = os.path.splitext(filename)
    if ext == '':
        filename = base + '.dbf'
    if os.path.exists(filename):
        fd = open(filename)
        version = fd.read(1)
        fd.close()
        fd = None
        if not version in version_map:
            raise TypeError("Unknown dbf type: %s (%x)" % (version, ord(version)))
        return version_map[version]
    return 'File %s not found' % filename
def _packShortInt(value, bigendian=False):
        "Returns a two-bye integer from the value, or raises DbfError"
        # 256 / 65,536
        if value > 65535:
            raise DbfError("Maximum Integer size exceeded.  Possible: 65535.  Attempted: %d" % value)
        if bigendian:
            return struct.pack('>H', value)
        else:
            return struct.pack('<H', value)
def _packLongInt(value, bigendian=False):
        "Returns a four-bye integer from the value, or raises DbfError"
        # 256 / 65,536 / 16,777,216
        if value > 4294967295:
            raise DbfError("Maximum Integer size exceeded.  Possible: 4294967295.  Attempted: %d" % value)
        if bigendian:
            return struct.pack('>L', value)
        else:
            return struct.pack('<L', value)
def _packDate(date):
        "Returns a group of three bytes, in integer form, of the date"
        return "%c%c%c" % (date.year-1900, date.month, date.day)
def _packStr(string):
        "Returns an 11 byte, upper-cased, null padded string suitable for field names; raises DbfError if the string is bigger than 10 bytes"
        if len(string) > 10:
            raise DbfError("Maximum string size is ten characters -- %s has %d characters" % (string, len(string)))
        return struct.pack('11s', string.upper())       
def _unpackShortInt(bytes, bigendian=False):
        "Returns the value in the two-byte integer passed in"
        if bigendian:
            return struct.unpack('>H', bytes)[0]
        else:
            return struct.unpack('<H', bytes)[0]
def _unpackLongInt(bytes, bigendian=False):
        "Returns the value in the four-byte integer passed in"
        if bigendian:
            return int(struct.unpack('>L', bytes)[0])
        else:
            return int(struct.unpack('<L', bytes)[0])
def _unpackDate(bytestr):
        "Returns a Date() of the packed three-byte date passed in"
        year, month, day = struct.unpack('<BBB', bytestr)
        year += 1900
        return Date(year, month, day)
def _unpackStr(chars):
        "Returns a normal, lower-cased string from a null-padded byte string"
        return struct.unpack('%ds' % len(chars), chars)[0].replace('\x00','').lower()
def _convertToBool(value):
    """Returns boolean true or false; normal rules apply to non-string values; string values
    must be 'y','t', 'yes', or 'true' (case insensitive) to be True"""
    if type(value) == str:
        return bool(value.lower() in ['t', 'y', 'true', 'yes'])
    else:
        return bool(value)
def _unsupportedType(something, field, memo=None):
    "called if a data type is not supported for that style of table"
    raise DbfError('field type is not supported.')
def _retrieveCharacter(string, fielddef={}, memo=None):
    "Returns the string in 'string' with trailing white space removed"
    return string.rstrip()
def _updateCharacter(string, fielddef, memo=None):
    "returns the string, truncating if string is longer than it's field"
    if type(string) != str:
        raise DbfError("incompatible type: %s" % type(string))
    return string.rstrip()
def _retrieveCurrency(bytes, fielddef={}, memo=None):
    value = struct.unpack('<q', bytes)[0]
    return Decimal("%de-4" % value)
def _updateCurrency(value, fielddef={}, memo=None):
    #if not (type(value) in (int, long, float)):
    #    raise DbfError("incompatible type: %s" % type(value))
    currency = int(value * 10000)
    if not -9223372036854775808 < currency < 9223372036854775808:
        raise DbfError("value %s is out of bounds" % value)
    return struct.pack('<q', currency)
def _retrieveDate(string, fielddef={}, memo=None):
    "Returns the ascii coded date as a Date object"
    return Date.fromymd(string)
def _updateDate(moment, fielddef={}, memo=None):
    "returns the Date or datetime.date object ascii-encoded (yyyymmdd)"
    if moment:
        return "%04d%02d%02d" % moment.timetuple()[:3]
    return '        '
def _retrieveDateTime(bytes, fielddef={}, memo=None):
    """returns the date/time stored in bytes; dates <= 01/01/1981 00:00:00
    may not be accurate;  BC dates are nulled."""
    # two four-byte integers store the date and time.
    # millesecords are discarded from time
    time = _retrieveInteger(bytes[4:])
    microseconds = (time % 1000) * 1000
    time = time // 1000                      # int(round(time, -3)) // 1000 discard milliseconds
    hours = time // 3600
    mins = time % 3600 // 60
    secs = time % 3600 % 60
    time = Time(hours, mins, secs, microseconds)
    possible = _retrieveInteger(bytes[:4])
    possible -= VFPTIME
    possible = max(0, possible)
    date = Date.fromordinal(possible)
    return DateTime.combine(date, time)
def _updateDateTime(moment, fielddef={}, memo=None):
    """sets the date/time stored in moment
    moment must have fields year, month, day, hour, minute, second, microsecond"""
    #if type(moment) != datetime.datetime:
    #    raise DbfError("incompatible type: %s" % type(moment))
    bytes = [0] * 8
    hour = moment.hour
    minute = moment.minute
    second = moment.second
    millisecond = moment.microsecond // 1000       # convert from millionths to thousandths
    time = ((hour * 3600) + (minute * 60) + second) * 1000 + millisecond
    bytes[4:] = _updateInteger(time)
    bytes[:4] = _updateInteger(moment.toordinal() + VFPTIME)
    return ''.join(bytes)
def _retrieveDouble(bytes, fielddef={}, memo=None):
    return struct.unpack('<d', bytes)[0]
def _updateDouble(value, fielddef={}, memo=None):
    if not (type(value) in (int, long, float)):
        raise DbfError("incompatible type: %s" % type(value))
    return struct.pack('<d', value)
def _retrieveInteger(bytes, fielddef={}, memo=None):
    "Returns the binary number stored in bytes in little-endian format"
    return struct.unpack('<i', bytes)[0]
def _updateInteger(value, fielddef={}, memo=None):
    "returns value in little-endian binary format"
    if not (type(value) in (int, long)):
        raise DbfError("incompatible type: %s" % type(value))
    if not -2147483648 < value < 2147483647:
        raise DbfError("Integer size exceeded.  Possible: -2,147,483,648..+2,147,483,647.  Attempted: %d" % value)
    return struct.pack('<i', value)
def _retrieveLogical(string, fielddef={}, memo=None):
    "Returns True if string is 't', 'T', 'y', or 'Y', and False otherwise"
    return string in ['t','T','y','Y']
def _updateLogical(logical, fielddef={}, memo=None):
    "Returs 'T' if logical is True, 'F' otherwise"
    if type(logical) != bool:
        logical = _convertToBool(logical)
    if type(logical) <> bool:
        raise DbfError('Value %s is not logical.' % logical)
    return logical and 'T' or 'F'
def _retrieveMemo(stringval, fielddef, memo):
    "Returns the block of data from a memo file"
    if stringval.strip():
        block = int(stringval.strip())
    else:
        block = 0
    return memo.getMemo(block, fielddef)
def _updateMemo(string, fielddef, memo):
    "Writes string as a memo, returns the block number it was saved into"
    block = memo.putMemo(string)
    if block == 0:
        block = ''
    return "%*s" % (fielddef['length'], block)
def _retrieveNumeric(string, fielddef, memo=None):
    "Returns the number stored in string as integer if field spec for decimals is 0, float otherwise"
    if string.strip() == '':
        string = '0'
    if fielddef['decimals'] == 0:
        return int(string)
    else:
        return float(string)
def _updateNumeric(value, fielddef, memo=None):
    "returns value as ascii representation, rounding decimal portion as necessary"
    if not (type(value) in (int, long, float)):
        raise DbfError("incompatible type: %s" % type(value))
    decimalsize = fielddef['decimals']
    if decimalsize:
        decimalsize += 1
    maxintegersize = fielddef['length']-decimalsize
    integersize = len("%.0f" % value)
    if integersize > maxintegersize:
        raise DbfError('Integer portion too big')
    return "%*.*f" % (fielddef['length'], fielddef['decimals'], value)
def _retrieveVfpMemo(bytes, fielddef, memo):
    "Returns the block of data from a memo file"
    block = struct.unpack('<i', bytes)[0]
    return memo.getMemo(block, fielddef)
def _updateVfpMemo(string, fielddef, memo):
    "Writes string as a memo, returns the block number it was saved into"
    block = memo.putMemo(string)
    return struct.pack('<i', block)
def _addCharacter(format):
    if format[1] != '(' or format[-1] != ')':
        raise DbfError("Format for Character field creation is C(n), not %s" % format)
    length = int(format[2:-1])
    if not 0 < length < 255:
        raise ValueError
    decimals = 0
    return length, decimals
def _addDate(format):
    length = 8
    decimals = 0
    return length, decimals
def _addLogical(format):
    length = 1
    decimals = 0
    return length, decimals
def _addMemo(format):
    length = 10
    decimals = 0
    return length, decimals
def _addNumeric(format):
    if format[1] != '(' or format[-1] != ')':
        raise DbfError("Format for Numeric field creation is N(n.n), not %s" % format)
    length, decimals = format[2:-1].split('.')
    length = int(length)
    decimals = int(decimals)
    if not (0 < length < 18 and 0 <= decimals <= length - 2):
        raise ValueError
    return length, decimals
def _addVfpCurrency(format):
    length = 8
    decimals = 0
    return length, decimals
def _addVfpDateTime(format):
    length = 8
    decimals = 8
    return length, decimals
def _addVfpDouble(format):
    length = 8
    decimals = 0
    return length, decimals
def _addVfpInteger(format):
    length = 4
    decimals = 0
    return length, decimals
def _addVfpMemo(format):
    length = 4
    decimals = 0
    return length, decimals
def _addVfpNumeric(format):
    if format[1] != '(' or format[-1] != ')':
        raise DbfError("Format for Numeric field creation is N(n.n), not %s" % format)
    length, decimals = format[2:-1].split('.')
    length = int(length)
    decimals = int(decimals)
    if not (0 < length < 21 and 0 <= decimals <= length - 2):
        raise ValueError
    return length, decimals
class DbfError(Exception):
    "Fatal errors elicit this response."
    def __init__(yo, problem):
        yo.message = problem
    def __str__(yo):

        return yo.message
class FieldMissing(DbfError):
    def __init__(yo, fieldname):
        yo.message = '%s:  no such field in table' % fieldname
class DbfWarning(Exception):
    "Normal operations elicit this response"
    warning = 'You should not see this message.  Contact a programmer.'
    def __str__(yo):
        return yo.warning
class Eof(DbfWarning):
    "End of file reached"
    warning = 'End of file reached'
class Bof(DbfWarning):
    "Beginning of file reached"
    warning = 'Beginning of file reached'
class _MetaData(dict):
    blankrecord = None
    fields = None
    filename = None
    dfd = None
    memoname = None
    newmemofile = False
    memo = None
    mfd = None
    ignorememos = False
    memofields = None
    order = None
    orderresults = []
class _TableHeader(object):
    def __init__(yo, data):
        if len(data) != 32:
            raise DbfError('table header should be 32 bytes, but is %d bytes' % len(data))
        yo._data = data + '\x0d'
    def __getattr__(yo, name):
        if name[0:2] == '__' and name[-2:] == '__':
            raise AttributeError, 'Method %s is not implemented.' % name
        elif name not in ['data', 'version', 'update', 'recordcount', 'start', \
                'fieldcount', 'recordlength', 'codepage', 'fields', 'extra']:
            raise AttributeError
        elif name == 'data':
            date = _packDate(datetime.datetime.now().date())
            header = list(yo._data)
            header[1:4] = date
            yo._data = ''.join(header)
            return yo._data
        elif name == 'version':
            return yo._data[0]
        elif name == 'update':
            return _unpackDate(yo._data[1:4])
        elif name == 'recordcount':
            return _unpackLongInt(yo._data[4:8])
        elif name == 'start':
            return _unpackShortInt(yo._data[8:10])
        elif name == 'fieldcount':
            fieldblock = yo._data[32:]
            for i in range(len(fieldblock)//32+1):
                cr = i * 32
                if fieldblock[cr] == '\x0d':
                    break
            else:
                raise DbfError("corrupt field structure")
            return len(fieldblock[:cr]) // 32
        elif name == 'recordlength':
            return _unpackShortInt(yo._data[10:12])
        elif name == 'codepage':
            return yo._data[29]
        elif name == 'fields':
            fieldblock = yo._data[32:]
            for i in range(len(fieldblock)//32+1):
                cr = i * 32
                if fieldblock[cr] == '\x0d':
                    break
            else:
                raise DbfError("corrupt field structure")
            return fieldblock[:cr]
        elif name == 'extra':
            fieldblock = yo._data[32:]
            for i in range(len(fieldblock)//32+1):
                cr = i * 32
                if fieldblock[cr] == '\x0d':
                    break
            else:
                raise DbfError("corrupt field structure")
            return fieldblock[cr+1:]
        else:
            raise AttributeError
    def __setattr__(yo, name, value):
        if name not in ['_data', 'version', 'recordcount', 'codepage', 'fields', 'extra']:
            raise AttributeError
        elif name == '_data':
            if len(value) < 32:
                raise DbfError("value for _data is less than 32 - %d" % len(value))
            object.__setattr__(yo, '_data', value)
        elif name == 'version':
            yo._data = value + yo._data[1:]
        elif name == 'recordcount':
            yo._data = yo._data[:4] + _packLongInt(value) + yo._data[8:]
        elif name == 'codepage':
            yo._data = yo._data[:29] + value + yo._data[30:]
        elif name == 'fields':
            fieldblock = yo._data[32:]
            for i in range(len(fieldblock)//32+1):
                cr = i * 32
                if fieldblock[cr] == '\x0d':
                    break
            else:
                raise DbfError("corrupt field structure")
            fieldlen = len(value)
            if fieldlen % 32 != 0:
                raise DbfError("fields structure corrupt: %d is not a multiple of 32" % fieldlen)
            yo._data = yo._data[:32] + value + fieldblock[cr:]                          # fields
            yo._data = yo._data[:8]  + _packShortInt(len(yo._data)) + yo._data[10:]   # start
            fieldlen = fieldlen // 32
            recordlen = 1                                                               # deleted flag
            for i in range(fieldlen):
                recordlen += ord(value[i*32+16])
            yo._data = yo._data[:10] + _packShortInt(recordlen) + yo._data[12:]
        elif name == 'extra':
            fieldblock = yo._data[32:]
            for i in range(len(fieldblock)//32+1):
                cr = i * 32
                if fieldblock[cr] == '\x0d':
                    break
            else:
                raise DbfError("corrupt field structure")
            cr += 33    # skip past table data and final CR
            yo._data = yo._data[:cr] + value                                            # extra
            yo._data = yo._data[:8]  + _packShortInt(len(yo._data)) + yo._data[10:]   # start
        else:
            raise AttributeError
class _DbfRecord(object):
    """Provides routines to extract and save data within the fields of a dbf record."""
    __slots__ = ['_recnum', '_layout', '_data']
    def _retrieveFieldValue(yo, string, fielddef):
        "calls appropriate routine to fetch value stored in field from string"
        return yo._layout.fieldtypes[fielddef['type']]['Retrieve'](string, fielddef, yo._layout.memo)
    def _updateFieldValue(yo, fielddef, value):
        "calls appropriate routine to convert value to ascii bytes, and save it in record"
        type = fielddef['type']
        fieldtype = yo._layout.fieldtypes[type]
        callable = fieldtype['Update']
        update = list(yo._layout.fieldtypes[fielddef['type']]['Update'](value, fielddef, yo._layout.memo))
        size = fielddef['length']
        if len(update) > size:
            raise DbfError("tried to store %d bytes in %d byte field" % (len(update), fielddef['length']))
        blank = list(' ' * size)
        start = fielddef['start']
        end = start + len(update)
        target = list(yo._data)
        target[start:start+size] = blank
        target[start:end] = update
        yo._data = ''.join(target)
        yo._updateDisk(yo._recnum * yo._layout.header.recordlength + yo._layout.header.start, yo._data)
    def _updateDisk(yo, location='', data=''):
        if not yo._layout.inmemory:
            if yo._recnum < 0:
                raise DbfError("Attempted to update record that has been packed")
            if location == '':
                location = yo._recnum * yo._layout.header.recordlength + yo._layout.header.start
            if data == '':
                data = yo._data
            yo._layout.dfd.seek(location)
            yo._layout.dfd.write(data)
    def __contains__(yo, key):
        return key in yo._layout.fields
    def __iter__(yo):
        return (yo[field] for field in yo._layout.fields)
    def __getattr__(yo, name):
        if name[0:2] == '__' and name[-2:] == '__':
            raise AttributeError, 'Method %s is not implemented.' % name
        elif not name in yo._layout.fields:
            raise FieldMissing(name)
        try:
            fielddef = yo._layout[name]
            value = yo._retrieveFieldValue(yo._data[fielddef['start']:fielddef['end']], fielddef)
            return value
        except DbfError, error:
            message = "field --%s-- is %s -> %s" % (name, yo._layout.fieldtypes[fielddef['type']]['Type'], error.message)
            raise DbfError(message)
    def __getitem__(yo, item):
        if type(item) == int:
            if not -yo._layout.header.fieldcount <= item < yo._layout.header.fieldcount: 
                raise IndexError("Field offset %d is not in record" % item)
            return yo[yo._layout.fields[item]]
        elif type(item) == slice:
            sequence = []
            for index in yo._layout.fields[item]:
                sequence.append(yo[index])
            return sequence
        elif type(item) == str:
            return yo.__getattr__(item)
        else:
            raise TypeError("%s is not a field name" % item)
    def __len__(yo):
        return yo._layout.header.fieldcount
    def __new__(cls, recnum, layout, kamikaze='', _fromdisk=False):
        """record = ascii string of entire record; layout=record specification; memo = memo object for table"""
        record = object.__new__(cls)
        record._recnum = recnum
        record._layout = layout
        if layout.blankrecord == None and not _fromdisk:
            record._createBlankRecord()
        record._data = layout.blankrecord
        if recnum == -1:                    # not a disk-backed record
            return record
        elif type(kamikaze) == str:
            record._data = kamikaze
        else:
            record._data = kamikaze._data
        datalen = len(record._data)
        if datalen < layout.header.recordlength:
            record._data = record._data[:datalen] + layout.blankrecord[datalen:]
        elif datalen > layout.header.recordlength:
            record._data = record._data[:layout.header.recordlength]
        if not _fromdisk and not layout.inmemory:
            record._updateDisk()
        return record
    def __setattr__(yo, name, value):
        if name in yo.__slots__:
            object.__setattr__(yo, name, value)
            return
        elif not name in yo._layout.fields:
            raise FieldMissing(name)
        fielddef = yo._layout[name]
        try:
            yo._updateFieldValue(fielddef, value)
        except DbfError, error:
            message = "field --%s-- is %s -> %s" % (name, yo._layout.fieldtypes[fielddef['type']]['Type'], error.message)
            raise DbfError(message)
    def __setitem__(yo, name, value):
        if type(name) == str:
            yo.__setattr__(name, value)
        elif type(name) in (int, long):
            yo.__setattr__(yo._layout.fields[name], value)
        else:
            raise TypeError("%s is not a field name" % name)
    def __str__(yo):
        result = []
        for field in yo.table_fields:
            result.append("%-10s: %s" % (field, yo[field]))
        return '\n'.join(result)
    def __repr__(yo):
        return yo._data
    def _createBlankRecord(yo):
        "creates a blank record data chunk"
        layout = yo._layout
        ondisk = layout.ondisk
        layout.ondisk = False
        yo._data = ' ' * layout.header.recordlength
        layout.memofields = []
        for field in layout.fields:
            yo._updateFieldValue(layout[field], layout.fieldtypes[layout[field]['type']]['Blank']())
            if layout[field]['type'] in layout.memotypes:
                layout.memofields.append(field)
        layout.blankrecord = yo._data
        layout.ondisk = ondisk
    @property
    def record_number(yo):
        "physical record number"
        return yo._recnum
    @property
    def has_been_deleted(yo):
        "marked for deletion?"
        return yo._data[0] == '*'
    @property
    def table_fields(yo):
        "fields in table/record"
        return yo._layout.fields[:]
    def delete_record(yo):
        "marks record as deleted"
        yo._data = '*' + yo._data[1:]
        yo._updateDisk(data='*')
    def gather_fields(yo, dict, drop=False):
        "saves a dictionary into a records fields\nkeys with no matching field will raise a FieldMissing exception unless drop = True"
        for key in dict:
            if not key in yo.table_fields:
                if drop:
                    continue
                raise FieldMissing(key)
            yo.__setattr__(key, dict[key])
    def reset_record(yo, keep_fields=None):
        "blanks record"
        if keep_fields is None:
            keep_fields = []
        keep = {}
        for field in keep_fields:
            keep[field] = yo[field]
        if yo._layout.blankrecord == None:
            yo._createBlankRecord()
        yo._data = yo._layout.blankrecord
        for field in keep_fields:
            yo[field] = keep[field]
    def scatter_fields(yo, blank=False):
        "returns a dictionary of fieldnames and values which can be used with gatherFields().  if blank is True, values are empty."
        keys = yo._layout.fields
        if blank:
            values = [yo._layout.fieldtypes[yo._layout[key]['type']]['Blank']() for key in keys]
        else:
            values = [yo[field] for field in keys]
        return dict(zip(keys, values))
    def undelete_record(yo):
        "marks record as active"
        yo._data = ' ' + yo._data[1:]
        yo._updateDisk(data=' ')
    # these asignments are for backward compatibility, and will go away
    Delete = deleteRecord = delete_record
    Recall = undeleteRecord = undelete_record
    resetRecord = reset_record
    Gather = gatherFields = gather_fields
    Scatter = scatterFields = scatter_fields
class _DbfMemo(object):
    "Provides access to memo files"
    def _getMemo(yo, block):
        block = int(block)
        yo.meta.mfd.seek(block * yo.meta.memosize)
        eom = -1
        data = ''
        while eom == -1:
            newdata = yo.meta.mfd.read(yo.meta.memosize)
            if not newdata:
                return data
            data += newdata
            eom = data.find('\x1a\x1a')
        return data[:eom]
    def _init(yo):
        "dBase III specific"
        yo.meta.memosize = 512
        yo.record_header_length = 2
        if yo.meta.ondisk and not yo.meta.ignorememos:
            if yo.meta.newmemofile:
                yo.meta.mfd = open(yo.meta.memoname, 'w+b')
                yo.meta.mfd.write(_packLongInt(1) + '\x00' * 508)
            else:
                try:
                    yo.meta.mfd = open(yo.meta.memoname, 'r+b')
                    yo.meta.mfd.seek(0)
                    yo.nextmemo = _unpackLongInt(yo.meta.mfd.read(4))
                except:
                    raise DbfError("memo file appears to be corrupt")
    def _putMemo(yo, data):
        length = len(data) + yo.record_header_length  # room for two ^Z at end of memo
        blocks = length // yo.meta.memosize
        if length % yo.meta.memosize:
            blocks += 1
        thismemo = yo.nextmemo
        yo.nextmemo = thismemo + blocks
        yo.meta.mfd.seek(0)
        yo.meta.mfd.write(_packLongInt(yo.nextmemo))
        yo.meta.mfd.seek(thismemo * yo.meta.memosize)
        yo.meta.mfd.write(data)
        yo.meta.mfd.write('\x1a\x1a')
        if len(yo._getMemo(thismemo)) != len(data):
            raise DbfError("unknown error: memo not saved")
        return thismemo
    def __init__(yo, meta):
        ""
        yo.meta = meta
        yo.memory = {}
        yo.nextmemo = 1
        yo._init()
        yo.meta.newmemofile = False
    def getMemo(yo, block, field):
        "gets the memo in block"
        if yo.meta.ignorememos or not block:
            return ''
        #block = int(block)
        if yo.meta.ondisk:
            return yo._getMemo(block)
        else:
            return yo.memory[block]
    def putMemo(yo, data):
        "stores data in memo file, returns block number"
        if yo.meta.ignorememos or data == '':
            return 0
        if yo.meta.inmemory:
            thismemo = yo.nextmemo
            yo.nextmemo += 1
            yo.memory[thismemo] = data
        else:
            thismemo = yo._putMemo(data)
        return thismemo
class DbfTable(object):
    """Provides an interface for working with dBase III tables."""
    _version = 'dBase III Plus'
    _versionabbv = 'db3'
    _fieldtypes = {
            'C' : {'Type':'Character', 'Retrieve':_retrieveCharacter, 'Update':_updateCharacter, 'Blank':str, 'Init':_addCharacter},
            'D' : {'Type':'Date', 'Retrieve':_retrieveDate, 'Update':_updateDate, 'Blank':Date.today, 'Init':_addDate},
            'L' : {'Type':'Logical', 'Retrieve':_retrieveLogical, 'Update':_updateLogical, 'Blank':bool, 'Init':_addLogical},
            'M' : {'Type':'Memo', 'Retrieve':_retrieveMemo, 'Update':_updateMemo, 'Blank':str, 'Init':_addMemo},
            'N' : {'Type':'Numeric', 'Retrieve':_retrieveNumeric, 'Update':_updateNumeric, 'Blank':int, 'Init':_addNumeric} }
    _memoext = '.dbt'
    _memotypes = ('M',)
    _memoClass = _DbfMemo
    _yesMemoMask = '\x80'
    _noMemoMask = '\x7f'
    _fixedFields = ('D','L','M')
    _decimalFields = ('N',)
    _variableFields = ('C',)
    _numericFields = ('N',)
    _dbfTableHeader = ['\x00'] * 32
    _dbfTableHeader[0] = '\x03'         # version - dBase III w/o memo's
    _dbfTableHeader[10] = '\x01'        # record length -- one for delete flag
    _dbfTableHeader[29] = '\x03'        # code page -- 437 US-MS DOS
    _dbfTableHeader = ''.join(_dbfTableHeader)
    _dbfTableHeaderExtra = ''
    _supported_tables = ['\x03', '\x83']
    _readonly = False
    _metaonly = False
    useDeleted = True
    def _buildHeaderFields(yo):
        fieldblock = []
        memo = False
        yo._meta.header.version = chr(ord(yo._meta.header.version) & ord(yo._noMemoMask))
        for field in yo._meta.fields:
            fielddef = ['\x00'] * 32
            fielddef[:11] = _packStr(field)
            fielddef[11] = yo._meta[field]['type']
            fielddef[12:16] = _packLongInt(yo._meta[field]['start'])
            fielddef[16] = chr(yo._meta[field]['length'])
            fielddef[17] = chr(yo._meta[field]['decimals'])
            fielddef[18] = chr(yo._meta[field]['flags'])
            fieldblock.extend(fielddef)
            if yo._meta[field]['type'] in yo._meta.memotypes:
                memo = True
        yo._meta.header.fields = ''.join(fieldblock)
        if memo:
            yo._meta.header.version = chr(ord(yo._meta.header.version) | ord(yo._yesMemoMask))
            if yo._meta.memo is None:
                yo._meta.memo = yo._memoClass(yo._meta)
    def _checkMemoIntegrity(yo):
        "dBase III specific"
        if yo._meta.header.version == '\x83':
            try:
                yo._meta.memo = yo._memoClass(yo._meta)
            except:
                yo._meta.dfd.close()
                yo._meta.dfd = None
                raise
        if not yo._meta.ignorememos:
            for field in yo._meta.fields:
                if yo._meta[field]['type'] in yo._memotypes:
                    if yo._meta.header.version != '\x83':
                        yo._meta.dfd.close()
                        yo._meta.dfd = None
                        raise DbfError("Table structure corrupt:  memo fields exist, header declares no memos")
                    elif not os.path.exists(yo._meta.memoname):
                        yo._meta.dfd.close()
                        yo._meta.dfd = None
                        raise DbfError("Table structure corrupt:  memo fields exist without memo file")
                    break
    def _initializeFields(yo):
        "builds the FieldList of names, types, and descriptions"
        offset = 1
        fieldsdef = yo._meta.header.fields
        if len(fieldsdef) % 32 != 0:
            raise DbfError("field definition block corrupt: %d bytes in size" % len(fieldsdef))
        if len(fieldsdef) // 32 != yo._meta.header.fieldcount:
            raise DbfError("Header shows %d fields, but field definition block has %d fields" % (yo._meta.header.fieldcount, len(fieldsdef)//32))
        for i in range(yo._meta.header.fieldcount):
            fieldblock = fieldsdef[i*32:(i+1)*32]
            name = _unpackStr(fieldblock[:11])
            type = fieldblock[11]
            if not type in yo._meta.fieldtypes:
                raise DbfError("Unknown field type: %s" % type)
            start = offset
            length = ord(fieldblock[16])
            offset += length
            end = start + length
            decimals = ord(fieldblock[17])
            flags = ord(fieldblock[18])
            yo._meta.fields.append(name)
            yo._meta[name] = {'type':type,'start':start,'length':length,'end':end,'decimals':decimals,'flags':flags}
    def _fieldLayout(yo, i):
        "Returns field information Name Type(Length[.Decimals])"
        name = yo._meta.fields[i]
        type = yo._meta[name]['type']
        length = yo._meta[name]['length']
        decimals = yo._meta[name]['decimals']
        if type in yo._decimalFields:
            description = "%s %s(%d.%d)" % (name, type, length, decimals)
        elif type in yo._fixedFields:
            description = "%s %s" % (name, type)
        else:
            description = "%s %s(%d)" % (name, type, length)
        return description
    def _loadtable(yo):
        #print "loading table..."
        if yo._metaonly:
            raise DbfError("%s has been closed, records are unavailable" % yo.filename)
        dfd = yo._meta.dfd
        header = yo._meta.header
        dfd.seek(header.start)
        allrecords = dfd.read()                     # kludge to get around mysterious errno 0 problems
        dfd.seek(0)
        length = header.recordlength
        for i in range(header.recordcount):
            yo._table.append(_DbfRecord(i, yo._meta, allrecords[length*i:length*i+length], _fromdisk=True))
            yo._index.append(i)
        dfd.seek(0)
    def _updateDisk(yo, headeronly=False):
        if yo._meta.inmemory:
            return
        fd = yo._meta.dfd
        fd.seek(0)
        fd.write(yo._meta.header.data)
        if not headeronly:
            for record in yo._table:
                record._updateDisk()
            fd.flush()
            fd.truncate(yo._meta.header.start + yo._meta.header.recordcount * yo._meta.header.recordlength)
    def __contains__(yo, key):
        return key in yo._meta.fields
    def __getattr__(yo, name):
        if name in ('_index','_table'):
                yo._index = []
                yo._table = []
                yo._loadtable()
        return object.__getattribute__(yo, name)
    def __getitem__(yo, value):
        if type(value) == int:
            if not -yo._meta.header.recordcount <= value < yo._meta.header.recordcount: 
                raise IndexError("Record %d is not in table." % value)
            return yo._table[yo._index[value]]
        elif type(value) == slice:
            sequence = []
            for index in yo._index[value]:
                record = yo._table[index]
                if yo.useDeleted is True or not record.has_been_deleted:
                    sequence.append(record)
            return DbfList(sequence, desc='%s -->  %s' % (yo.filename, value))
        else:
            raise TypeError
    def __init__(yo, filename, fieldlist='', memosize=128, ignore_memos=False, 
                 readonly=False, keep_memos=False, metaonly=False):
        "open/create dbf file"
        if type(filename) != str or filename == '':
            raise TypeError("Filename must be specified")
        if filename == ':memory:' and fieldlist == '':
            raise DbfError("field list must be specified for in-memory tables")
        yo._meta = _MetaData()
        yo._meta.fields = []
        yo._meta.fieldtypes = yo._fieldtypes
        yo._meta.memotypes = yo._memotypes
        yo._meta.ignorememos = ignore_memos
        yo._meta.filename = filename
        yo._meta.memosize = memosize
        header = _TableHeader(yo._dbfTableHeader)
        header.extra = yo._dbfTableHeaderExtra
        header.data #force update of date
        yo._meta.header = header
        if filename == ':memory:':
            yo._index = []
            yo._table = []
            yo._meta.ondisk = False
            yo._meta.inmemory = True
            yo._meta.memoname = ':memory:'
        else:
            base, ext = os.path.splitext(filename)
            if ext == '':
                yo._meta.filename =  base + '.dbf'
            yo._meta.memoname = base + yo._memoext
            yo._meta.ondisk = True
            yo._meta.inmemory = False
        if fieldlist:
            if yo._meta.ondisk:
                yo._meta.dfd = open(yo._meta.filename, 'w+b')
                yo._meta.newmemofile = True
            yo.AddFields(fieldlist)
            return
        dfd = yo._meta.dfd = open(yo._meta.filename, 'r+b')
        dfd.seek(0)
        yo._meta.header = header = _TableHeader(dfd.read(32))
        if not header.version in yo._supported_tables:
            dfd.close()
            dfd = None
            raise TypeError("Unsupported dbf type: %s [%x]" % (version_map.get(yo._meta.header.version, 'Unknown: %s' % yo._meta.header.version), ord(yo._meta.header.version)))
        fieldblock = dfd.read(header.start - 32)
        for i in range(len(fieldblock)//32+1):
            fieldend = i * 32
            if fieldblock[fieldend] == '\x0d':
                break
        else:
            raise DbfError("corrupt field structure in header")
        if len(fieldblock[:fieldend]) % 32 != 0:
            raise DbfError("corrupt field structure in header")
        header.fields = fieldblock[:fieldend]
        header.extra = fieldblock[fieldend+1:]  # skip trailing \r
        yo._initializeFields()
        yo._checkMemoIntegrity()
        if header.recordcount > 0:
            yo._meta.current = 0
        else:
            yo._meta.current = -1
        dfd.seek(0)
        if metaonly:
            yo.close(keep_table=False, keep_memos=False)
        elif readonly:
            yo.close(keep_table=True, keep_memos=keep_memos)
    def __iter__(yo):
        class dbfIterator(object):
            def __init__(yo, table):
                yo.table = table
                yo.recordList = (i for i in yo.table._index)
                yo.useDeleted = table.useDeleted
            def __iter__(yo):
                return yo
            def next(yo):
                for i in yo.recordList:
                    record = yo.table._table[i]
                    if not yo.useDeleted and record.has_been_deleted:
                        continue
                    else:
                        return record
                else:
                    raise StopIteration
        return dbfIterator(yo)           
    def __len__(yo):
        return yo._meta.header.recordcount
    def __repr__(yo):
        if yo._readonly:
            return __name__ + ".Table('%s', readonly=True)" % yo._meta.filename
        elif yo._metaonly:
            return __name__ + ".Table('%s', metaonly=True)" % yo._meta.filename
        else:
            return __name__ + ".Table('%s')" % yo._meta.filename
    def __str__(yo):
        if yo._readonly:
            status = "read-only"
        elif yo._metaonly:
            status = "meta-only"
        else:
            status = "read/write"
        str =  """
        Table:         %s
        Type:          %s
        Status:        %s
        Last updated:  %s
        Record count:  %d
        Field count:   %d
        Record length: %d
        """ % (yo._meta.filename, version_map.get(yo._meta.header.version, 'unknown - ' + hex(ord(yo._meta.header.version))),
                status, yo._meta.header.update, yo._meta.header.recordcount, yo._meta.header.fieldcount, yo._meta.header.recordlength)
        str += "\n        --Fields--\n"
        for i in range(len(yo._meta.fields)):
            str += "        " + yo._fieldLayout(i) + "\n"
        return str
    def has_key(yo, key):
        return key in yo
    def keys(yo):
        "returns a copy of the list of fields defined in table"
        return yo._meta.fields[:]
    def items(yo):
        return zip(yo.keys(), yo.values())
    def iteritems(yo):
        return (item for item in yo.items())
    def iterkeys(yo):
        return (key for key in yo._meta.fields)
    def itervalues(yo):
        return (value for value in yo.values())
    def values(yo):
        "returns list of values in field order for current record"
        record = yo.current()
        return [record[field] for field in record.table_fields]
    # Properties
    @property
    def fieldcount(yo):
        "the number of fields in the table"
        return yo._meta.header.fieldcount
    @property
    def fields(yo):
        "a list of the fields in the table"
        return yo._meta.fields[:]
    @property
    def filename(yo):
        "table's file name"
        return yo._meta.filename
    @property
    def memoname(yo):
        "table's memo name"
        return yo._meta.memoname
    @property
    def record_number(yo):
        "number of the current record"
        return yo._meta.current
    @property
    def sort(yo):
        "current sort order of the table"
        return yo._meta.order
    @property
    def supported_tables(yo):
        "allowable table types"
        return yo._supported_tables
    @property
    def version(yo):
        "returns the dbf type of the table"
        return yo._version
    def add_fields(yo, fieldspec):
        "adds field(s) to the table layout; format is Name Type(Length.Decimals)[, Name Type(Length.Decimals)[...]]"
        yo._meta.blankrecord = None
        meta = yo._meta
        offset = meta.header.recordlength
        if type(fieldspec) == str:
            fields = fieldspec.replace(', ',',').split(',')
        else:
            fields = list(fieldspec)
        for field in fields:
            try:
                name, format = field.split()
                if name[0] == '_' or name[0].isdigit() or not name.replace('_','').isalnum():
                    raise DbfError("Field names cannot start with _ or digits, and can only contain the _, letters, and digits")
                name = name.lower()
                if name in meta.fields:
                    raise DbfError("Field '%s' already exists" % name)
                field_type = format[0].upper()
                if len(name) > 10:
                    raise DbfError("Maximum field name length is 10.  '%s' is %d characters long." % (name, len(name)))
                if not field_type in meta.fieldtypes.keys():
                    raise DbfError("Field types supported are (C)haracter, (D)ate, (L)ogical, (M)emo, and (N)umeric -- not (%s)" % field_type)
                length, decimals = yo._meta.fieldtypes[field_type]['Init'](format)
            except ValueError:
                raise DbfError("invalid field specifier: %s" % field)
            start = offset
            end = offset + length
            offset = end
            meta.fields.append(name)
            meta[name] = {'type':field_type, 'start':start, 'length':length, 'end':end, 'decimals':decimals, 'flags':0}
            for record in yo:
                record[name] = meta.fieldtypes[field_type]['Blank']()
        yo._buildHeaderFields()
        yo._updateDisk()
    addFields = add_fields
    def append(yo, kamikaze='', drop=False, multiple=1):
        "adds <multiple> blank records, and fills fields with dict/tuple values if present"
        if not yo._meta.header.fieldcount:
            raise DbfError("No fields defined, cannot append")
        dictdata = False
        tupledata = False
        if type(kamikaze) == dict:
            dictdata = kamikaze
            kamikaze = ''
        elif type(kamikaze) == tuple:
            tupledata = kamikaze
            kamikaze = ''
        yo._table.append(_DbfRecord(yo._meta.header.recordcount, yo._meta, kamikaze))
        yo._index.append(yo._meta.header.recordcount)
        yo._meta.header.recordcount += 1
        yo._meta.current = yo._meta.header.recordcount - 1
        newrecord = yo.current()
        if dictdata:
            newrecord.gatherFields(dictdata, drop)
        elif tupledata:
            for index, item in enumerate(tupledata):
                newrecord[index] = item
        elif kamikaze == str:
            for field in yo._meta.memofields:
                newrecord[field] = ''
        elif kamikaze:
            for field in yo._meta.memofields:
                newrecord[field] = kamikaze[field]
        if multiple > 1:
            multiple -= 1
            data = newrecord._data
            single = yo._meta.header.recordcount
            total = single + multiple
            while single < total:
                yo._table.append(_DbfRecord(single, yo._meta, kamikaze=data))
                yo._index.append(single)
                for field in yo._meta.memofields:
                    lastrecord = yo._table[-1]
                    lastrecord[field] = newrecord[field]
                single += 1
            yo._meta.header.recordcount += multiple
            yo._meta.current = yo._meta.header.recordcount - 1
        yo._updateDisk(headeronly=True)
        return newrecord
    def bottom(yo):
        """sets record pointer to last (non-deleted) record; raises DbfError if table is empty,
        Bof if all records deleted and useDeleted is False"""
        #if yo._meta.header.recordcount == 0:
        #    raise DbfError('Table is empty')
        yo._meta.current = yo._meta.header.recordcount
        try:
            return yo.prev()
        except Bof:
            yo._meta.current = yo._meta.header.recordcount
            raise Eof()
    def close(yo, keep_table=False, keep_memos=False):
        """closes disk files
        ensures table data is available if keep_table
        ensures memo data is available if keep_memos"""
        if keep_table:
            yo._table   # force read of table if not already in memory
        else:
            if '_index' in dir(yo):
                del yo._table
                del yo._index
        yo._meta.inmemory = True
        if yo._meta.ondisk:
            yo._meta.dfd.close()
            yo._meta.dfd = None
            if '_index' in dir(yo):
                yo._readonly = True
            else:
                yo._metaonly = True
        if yo._meta.mfd is not None:
            if not keep_memos:
                yo._meta.ignorememos = True
            else:
                memo_fields = []
                for field in yo.fields:
                    if yo.is_memotype(field):
                        memo_fields.append(field)
                for record in yo:
                    for field in memo_fields:
                        record[field] = record[field]
            yo._meta.mfd.close()
            yo._meta.mfd = None
        yo._meta.ondisk = False
    def current(yo):
        "returns current logical record"
        if yo._meta.current < 0:
            raise Bof()
        elif yo._meta.current < yo._meta.header.recordcount:
            return yo._table[yo._index[yo._meta.current]]
        else:
            raise Eof()
    def delete_fields(yo, fields):
        "removes field(s) from the table"
        doomedfields = fields.lower().replace(', ',',').split(',')
        for victim in doomedfields:
            if victim not in yo._meta.fields:
                raise DbfError("field %s not in table -- delete aborted" % victim)
        for victim in doomedfields:
            yo._meta.fields.pop(yo._meta.fields.index(victim))
            start = yo._meta[victim]['start']
            end = yo._meta[victim]['end']
            for record in yo:
                record._data = record._data[:start] + record._data[end:]
            for field in yo._meta.fields:
                if yo._meta[field]['start'] == end:
                    end = yo._meta[field]['end']
                    yo._meta[field]['start'] = start
                    yo._meta[field]['end'] = start + yo._meta[field]['length']
                    start = yo._meta[field]['end']
            yo._buildHeaderFields()
        yo._updateDisk()
    deleteFields = delete_fields
    def export(yo, records=None, filename='', fieldlist='', format='csv', header=True):
        """writes the table using CSV or tab-delimited format, using the filename
        given if specified, otherwise the table name"""
        if filename == '':
            filename = yo.filename
        if fieldlist == '':
            fieldlist = yo.fields
        else:
            fieldlist = fieldlist.replace(', ',',').split(',')
        if records is None:
            records = yo
        format = format.lower()
        if format not in ('csv', 'tab'):
            raise DbfError("export format: csv or tab, not %s" % format)
        base, ext = os.path.splitext(filename)
        if ext.lower() in ('', '.dbf'):
            filename = base + "." + format
        fd = open(filename, 'wb')
        try:
            if format == 'csv':
                csvfile = csv.writer(fd, dialect='dbf')
                if header:
                    csvfile.writerow(fieldlist)
                for record in records:
                    fields = []
                    for fieldname in fieldlist:
                        fields.append(record[fieldname])
                    csvfile.writerow(fields)
            else:
                if header:
                    fd.write('\t'.join(fieldlist) + '\n')
                for record in records:
                    fields = []
                    for fieldname in fieldlist:
                        fields.append(str(record[fieldname]))
                    fd.write('\t'.join(fields) + '\n')
        finally:
            fd.close()
            fd = None
        return filename
    def find(yo, match, dictionary=False, recordnumber=False, contained=False):
        """searches through table looking for records that match all the criteria in match,
        which is a dictionary of fieldname, value pairs -- brute force search of whole table"""
        if dictionary and recordnumber:
            raise DbfError('cannot specify both dictionary and recordnumber togethor')
        if dictionary:
            if not dictionary in yo:
                raise DbfError('dictionary must be a fieldname, or False -- not %s' % dictionary)
            records = {}
        else:
            records = DbfList(desc="%s -->  find(%s)" % (yo.filename, match))
        i = 0
        for record in yo:                           #i in range(yo._recordCount):
            for fieldname in match.keys():
                value = match[fieldname]
                if type(value) == str:
                    if contained:
                        if value not in record[fieldname]:
                            break
                    elif record[fieldname] != value:
                        break
                else:
                    if record[fieldname] != value:
                        break
            else:
                if yo.useDeleted or not record.has_been_deleted:
                    if dictionary:
                        key = record[dictionary]
                        records[key] = record.scatterFields()
                    elif recordnumber:
                        records.append(i)
                    else:
                        records.append(record)
            i += 1
        return records
    def goto(yo, match):
        """changes the record pointer to the first matching record
        match should be either a dictionary of name:value pairs, or
        an integer to go to"""
        if type(match) == int:
            if not -1 < match < yo._meta.header.recordcount:
                raise IndexError("Record %d does not exist")
            yo._meta.current = match
            record = yo.current()
            if not yo.useDeleted and record.has_been_deleted:
                return yo.next()
            else:
                return record
        for i in range(yo._meta.header.recordcount):
            for fieldname in match.keys():
                value = match[fieldname] 
                if type(value) == str:
                    if yo._table[yo._index[i]][fieldname][:len(value)] != value:
                        break
                else:
                    if yo._table[yo._index[i]][fieldname] != value:
                        break
            else:
                if yo.useDeleted or not yo._table[yo._index[i]].has_been_deleted:
                    yo._meta.current = i
                    return yo.current()
        else:
            return []
    #def has_been_deleted(yo):
    #    "returns True if record is deleted"
    #    if not -1 < yo._meta.current < yo._meta.header.recordcount:
    #        raise DbfError("No record selected")
    #    return yo.current().has_been_deleted
    #hasBeenDeleted = has_been_deleted
    def is_memotype(yo, name):
        "returns True if name is a memo type field"
        return yo._meta[name]['type'] in yo._memotypes
    isMemotype = is_memotype
    def new(yo, filename, _fieldlist=''):
        "returns a new table of the same type"
        if not _fieldlist:
            _fieldlist = yo.structure()
        if filename != ':memory:' and os.path.split(filename)[0] == "":
            filename = os.path.join(os.path.split(yo.filename)[0], filename)
        return Table(filename, _fieldlist, type=yo._versionabbv)
    def next(yo):
        "set record pointer to next (non-deleted) record"
        yo._meta.current += 1
        while yo._meta.current < yo._meta.header.recordcount:
            if yo.useDeleted or not yo.current().has_been_deleted:
                break
            else:
                yo._meta.current += 1
        if yo._meta.current >= yo._meta.header.recordcount:
            yo._meta.current = yo._meta.header.recordcount
            raise Eof()
        return yo.current()
    def order(yo, fields='ORIGINAL'):
        "orders the table using the field(s) provided; removes order if no field provided"
        if fields == 'ORIGINAL':
            yo._index = range(yo._meta.header.recordcount)
            yo._meta.order = None
            return
        fields = fields.replace(',',' ').split()
        Fields = {}
        newfields = []
        for field in fields:
            start = end = ''
            if field.find('[') > 0:
                field,slice = field.replace('[',' ').replace(']','').split()
                start, end = slice.split(':')
            try:
                Fields[field] = yo._meta[field]
            except KeyError:
                raise DbfError("field not found: %s" % field)
            Fields[field]['startslice'] = 0
            if start:
                Fields[field]['startslice'] = int(start)
            Fields[field]['endslice'] = Fields[field]['length']
            if end:
                Fields[field]['endslice'] = int(end)
            newfields.append(field)
        fields = newfields
        yo._meta.orderresults = [''] * len(yo)
        def sortme(index):
            result = []
            record = yo._table[index]
            for field in fields:
                start = Fields[field]['startslice']
                end = Fields[field]['endslice']
                length = Fields[field]['length']
                value = record[field]
                if Fields[field]['type'] in yo._numericFields:                                #('N','I','F'):
                    result.append(value)
                else:
                    result.append(("%-*s" % (length, value))[start:end].rstrip())
            record._layout.orderresults[record._recnum] = result
            return result
        yo._index.sort(key=sortme)
        yo._meta.order = fields
    def pack(yo):
        "physically removes all deleted records"
        newtable = []
        newindex = []
        i = 0
        for record in yo._table:
            if record.has_been_deleted:
                record._recnum = -1
            else:
                record._recnum = i
                newtable.append(record)
                newindex.append(i)
                i += 1
        yo._table = newtable
        yo._index = newindex
        yo._meta.header.recordcount = i
        yo._current = -1
        yo._meta.order = ''
        yo._updateDisk()
    def prev(yo):
        "set record pointer to previous (non-deleted) record"
        yo._meta.current -= 1
        while yo._meta.current >= 0:
            if yo.useDeleted or not yo.current().has_been_deleted:
                break
            else:
                yo._meta.current -= 1
        if yo._meta.current < 0:
            yo._meta.current = -1
            raise Bof
        return yo.current()
    def query(yo, sql=None, python=None):
        if python is None:
            raise DbfError("query: python parameter must be specified")
        possible = DbfList(desc="%s -->  %s" % (yo.filename, python))
        query_result = {}
        select = 'query_result["keep"] = %s' % python
        g = {}
        for record in yo:
            query_result['keep'] = False
            g['fld'] = record
            g['query_result'] = query_result
            exec select in g
            if query_result['keep'] is True:
                possible.append(record)
        return possible
    def rename_field(yo, oldname, newname):
        "renames an existing field"
        if not oldname in yo._meta.fields:
            raise DbfError("field --%s-- does not exist -- cannot rename it." % oldname)
        if newname[0] == '_' or newname[0].isdigit() or not newname.replace('_','').isalnum():
            raise DbfError("field names cannot start with _ or digits, and can only contain the _, letters, and digits")
        newname = newname.lower()
        if newname in yo._meta.fields:
            raise DbfError("field --%s-- already exists" % newname)
        if len(newname) > 10:
            raise DbfError("maximum field name length is 10.  '%s' is %d characters long." % (newname, len(newname)))
        yo._meta[newname] = yo._meta[oldname]
        yo._meta.fields[yo._meta.fields.index(oldname)] = newname
        yo._buildHeaderFields()
        yo._updateDisk(headeronly=True)
    renameField = rename_field
    def search(yo, match, dictionary=False, recordnumber=False, startswith=False):
        """searches using a binary algorythm looking for records that match the criteria in match,
        which is a list with a data item per ordered field.  table must be sorted.
        """
        if not yo._meta.order:
            raise DbfError('table must be ordered to use Search')
        if dictionary and recordnumber:
            raise DbfError('cannot specify both dictionary and recordnumber togethor')
        if dictionary:
            if not dictionary in yo:
                raise DbfError('dictionary must be a fieldname, or False -- not %s' % dictionary)
            records = {}
        else:
            records = DbfList(desc="%s -->  search: order=%s, match=%s)" % (yo.filename, yo.sort, match))
        if type(match) != list:
            match = [match]
        if startswith and yo._meta[yo.sort[-1]]['type'] != 'C':
            raise DbfError("startswith only valid for C type fields -- %s is %s" % (yo.sort[-1], yo._meta[yo.sort[-1]]['type']))
        segment = len(yo)
        current = 0
        toosoon = True
        notFound = True
        matchlen=len(match)
        try:
            lastlen = len(match[-1])
        except TypeError:
            lastlen = False
        while notFound:
            segment = segment // 2
            if toosoon:
                current += segment
            else:
                current -= segment
            if current % 2:
                segment += 1
            if current == len(yo) or segment == 0:
                break
            if matchlen:
                value = yo._meta.orderresults[yo[current].record_number][:matchlen]
            else:
                value = yo._meta.orderresults[yo[current].record_number]
            if startswith:
                value[-1] = value[-1][:lastlen]
            if value < match:
                toosoon = True
            elif value > match:
                toosoon = False
            else:
                notFound = False
                break
            if current == 0:
                break
        if notFound:
            return records
        while current > 0:
            current -= 1
            if matchlen:
                value = yo._meta.orderresults[yo[current].record_number][:matchlen]
            else:
                value = yo._meta.orderresults[yo[current].record_number]
            if startswith:
                value[-1] = value[-1][:lastlen]
            if value != match:
                current += 1
                break
        while True:
            if matchlen:
                value = yo._meta.orderresults[yo[current].record_number][:matchlen]
            else:
                value = yo._meta.orderresults[yo[current].record_number]
            if startswith:
                value[-1] = value[-1][:lastlen]
            if value != match:
                break
            if yo.useDeleted or not yo[current].has_been_deleted:
                if dictionary:
                    key = yo[current][dictionary]
                    records[key] = yo[current].scatterFields()
                elif recordnumber:
                    records.append(current)
                else:
                    records.append(yo[current])
            current += 1
            if current == len(yo):
                break
        return records
    def size(yo, field):
        "returns size of field as (length, decimals)"
        if field in yo:
            return (yo._meta[field]['length'], yo._meta[field]['decimals'])
        raise DbfError("%s is not a field in %s" % (field, yo.filename))
    def structure(yo, field=None):
        "return character list of fields suitable for creating same table layout"
        fieldlist = []
        try:
            if field is None:
                for i in range(len(yo._meta.fields)):
                    fieldlist.append(yo._fieldLayout(i))
            else:
                for name in field.replace(' ','').split(','):
                    fieldlist.append(yo._fieldLayout(yo.fields.index(name)))
        except ValueError:
            raise DbfError("field --%s-- does not exist" % name)
        return ','.join(fieldlist)
    def top(yo):
        """sets record pointer to first (non-deleted) record; raises DbfError if table is empty,
        Eof if all records are deleted and useDeleted is True"""
        #if yo._meta.header.recordcount == 0:                         # Error if no records exist
        #    raise DbfError('Table is empty')
        yo._meta.current = -1
        try:
            return yo.next()
        except Eof:
            yo._meta.current = -1
            raise Bof()
    def type(yo, field):
        "returns type of field"
        if field in yo:
            return yo._meta[field]['type']
        raise DbfError("%s is not a field in %s" % (field, yo.filename))
    def zap(yo, areyousure=False):
        """removes all records from table -- this cannot be undone!
        areyousure must be True, else error is raised"""
        if areyousure:
            yo._table = []
            yo._index = []
            yo._meta.header.recordcount = 0
            yo._current = -1
            yo._meta.order = ''
            yo._updateDisk()
        else:
            raise DbfError("You must say you are sure to wipe the table")
    # these asignments are for backward compatibility, and will go away
    AddFields = addFields
    Append = append
    Bottom = bottom
    Current = current
    DeleteFields = deleteFields
    Fields = keys
    Find = find
    Goto = goto
    ListFields = structure
    New = new
    Next = next
    Order = order
    Prev = prev
    RenameField = renameField
    SaveCsv = export
    Top = top
    Type = type
    Zap = zap
class _VfpMemo(_DbfMemo):
    def _init(yo):
        "Visual Foxpro 6 specific"
        if yo.meta.ondisk and not yo.meta.ignorememos:
            yo.record_header_length = 8
            if yo.meta.newmemofile:
                if yo.meta.memosize == 0:
                    yo.meta.memosize = 1
                elif 1 < yo.meta.memosize < 33:
                    yo.meta.memosize *= 512
                yo.meta.mfd = open(yo.meta.memoname, 'w+b')
                nextmemo = 512 // yo.meta.memosize
                if nextmemo * yo.meta.memosize < 512:
                    nextmemo += 1
                yo.nextmemo = nextmemo
                yo.meta.mfd.write(_packLongInt(nextmemo, bigendian=True) + '\x00\x00' + \
                        _packShortInt(yo.meta.memosize, bigendian=True) + '\x00' * 504)
            else:
                try:
                    yo.meta.mfd = open(yo.meta.memoname, 'r+b')
                    yo.meta.mfd.seek(0)
                    header = yo.meta.mfd.read(512)
                    yo.nextmemo = _unpackLongInt(header[:4], bigendian=True)
                    yo.meta.memosize = _unpackShortInt(header[6:8], bigendian=True)
                except:
                    raise DbfError("memo file appears to be corrupt")
    def _getMemo(yo, block):
        yo.meta.mfd.seek(block * yo.meta.memosize)
        header = yo.meta.mfd.read(8)
        length = _unpackLongInt(header[4:], bigendian=True)
        return yo.meta.mfd.read(length)
    def _putMemo(yo, data):
        yo.meta.mfd.seek(0)
        thismemo = _unpackLongInt(yo.meta.mfd.read(4), bigendian=True)
        yo.meta.mfd.seek(0)
        length = len(data) + yo.record_header_length  # room for two ^Z at end of memo
        blocks = length // yo.meta.memosize
        if length % yo.meta.memosize:
            blocks += 1
        #blocks = ((len(data)+yo.record_header_length) // yo.meta.memosize) + 1
        yo.meta.mfd.write(_packLongInt(thismemo+blocks, bigendian=True))
        yo.meta.mfd.seek(thismemo*yo.meta.memosize)
        yo.meta.mfd.write('\x00\x00\x00\x01' + _packLongInt(len(data), bigendian=True) + data)
        return thismemo
class VfpTable(DbfTable):
    version = 'Visual FoxPro 6'
    _versionabbv = 'vfp'
    _fieldtypes = {
            'C' : {'Type':'Character', 'Retrieve':_retrieveCharacter, 'Update':_updateCharacter, 'Blank':str, 'Init':_addCharacter},
            'Y' : {'Type':'Currency', 'Retrieve':_retrieveCurrency, 'Update':_updateCurrency, 'Blank':Decimal(), 'Init':_addVfpCurrency},
            'B' : {'Type':'Double', 'Retrieve':_retrieveDouble, 'Update':_updateDouble, 'Blank':float, 'Init':_addVfpDouble},
            'F' : {'Type':'Float', 'Retrieve':_retrieveNumeric, 'Update':_updateNumeric, 'Blank':float, 'Init':_addVfpNumeric},
            'N' : {'Type':'Numeric', 'Retrieve':_retrieveNumeric, 'Update':_updateNumeric, 'Blank':int, 'Init':_addVfpNumeric},
            'I' : {'Type':'Integer', 'Retrieve':_retrieveInteger, 'Update':_updateInteger, 'Blank':int, 'Init':_addVfpInteger},
            'L' : {'Type':'Logical', 'Retrieve':_retrieveLogical, 'Update':_updateLogical, 'Blank':bool, 'Init':_addLogical},
            'D' : {'Type':'Date', 'Retrieve':_retrieveDate, 'Update':_updateDate, 'Blank':Date.today, 'Init':_addDate},
            'T' : {'Type':'DateTime', 'Retrieve':_retrieveDateTime, 'Update':_updateDateTime, 'Blank':DateTime.now, 'Init':_addVfpDateTime},
            'M' : {'Type':'Memo', 'Retrieve':_retrieveVfpMemo, 'Update':_updateVfpMemo, 'Blank':str, 'Init':_addVfpMemo},
            'G' : {'Type':'General', 'Retrieve':_retrieveVfpMemo, 'Update':_updateVfpMemo, 'Blank':str, 'Init':_addVfpMemo},
            'P' : {'Type':'Picture', 'Retrieve':_retrieveVfpMemo, 'Update':_updateVfpMemo, 'Blank':str, 'Init':_addVfpMemo},
            '0' : {'Type':'_NullFlags', 'Retrieve':_unsupportedType, 'Update':_unsupportedType, 'Blank':int, 'Init':None} }
    _memoext = '.fpt'
    _memotypes = ('G','M','P')
    _memoClass = _VfpMemo
    _yesMemoMask = '\x30'               # 0011 0000
    _noMemoMask = '\x30'                # 0011 0000
    _fixedFields = ('B','D','G','I','L','M','P','T','Y')
    _decimalFields = ('F','N')
    _variableFields = ('C',)
    _numericFields = ('B','F','I','N','Y')
    _supported_tables = ('\x30',)
    _dbfTableHeader = ['\x00'] * 32
    _dbfTableHeader[0] = '\x30'         # version - Foxpro 6  0011 0000
    _dbfTableHeader[10] = '\x01'        # record length -- one for delete flag
    _dbfTableHeader[29] = '\x03'        # code page -- 437 US-MS DOS
    _dbfTableHeader = ''.join(_dbfTableHeader)
    _dbfTableHeaderExtra = '\x00' * 263
    useDeleted = True
    def _checkMemoIntegrity(yo):
        if os.path.exists(yo._meta.memoname):
            try:
                yo._meta.memo = yo._memoClass(yo._meta)
            except:
                yo._meta.dfd.close()
                yo._meta.dfd = None
                raise
        if not yo._meta.ignorememos:
            for field in yo._meta.fields:
                if yo._meta[field]['type'] in yo._memotypes:
                    if not os.path.exists(yo._meta.memoname):
                        yo._meta.dfd.close()
                        yo._meta.dfd = None
                        raise DbfError("Table structure corrupt:  memo fields exist without memo file")
                    break
    def _initializeFields(yo):
        "builds the FieldList of names, types, and descriptions"
        offset = 1
        fieldsdef = yo._meta.header.fields
        for i in range(yo._meta.header.fieldcount):
            fieldblock = fieldsdef[i*32:(i+1)*32]
            name = _unpackStr(fieldblock[:11])
            type = fieldblock[11]
            if not type in yo._meta.fieldtypes:
                raise DbfError("Unknown field type: %s" % type)
            elif type == '0':
                return          # ignore nullflags
            start = _unpackLongInt(fieldblock[12:16])
            length = ord(fieldblock[16])
            offset += length
            end = start + length
            decimals = ord(fieldblock[17])
            flags = ord(fieldblock[18])
            yo._meta.fields.append(name)
            yo._meta[name] = {'type':type,'start':start,'length':length,'end':end,'decimals':decimals,'flags':flags}
class DbfList(object):
    "list of Dbf records"
    _desc = ''
    def __init__(yo, new_records=None, desc=None):
        if new_records is not None:
            yo._list_of_records = new_records
            yo._current_record = 0
        else:
            yo._list_of_records = []
            yo._current_record = -1
        if desc is not None:
            yo._desc = desc
    def __delitem__(yo, key):
        if inlist(type(key), int, slice):
            return yo._list_of_records.__delitem__[key]
        else:
            raise TypeError
    def __getitem__(yo, key):
        if type(key) == int:
            count = len(yo._list_of_records)
            if not -count <= key < count:
                raise IndexError("Record %d is not in list." % key)
            return yo._list_of_records[key]
        elif type(key) == slice:
            return DbfList(yo._list_of_records[key])
        else:
            raise TypeError
    def __iter__(yo):
        return (record for record in yo._list_of_records)
    def __len__(yo):
        return len(yo._list_of_records)
    def __nonzero__(yo):
        return len(yo) > 0
    def __repr__(yo):
        if yo._desc:
            return "DbfList(%s - %d records)" % (yo._desc, len(yo._list_of_records))
        else:
            return "DbfList(%d records)" % len(yo._list_of_records)
    def __setitem__(yo, key, value):
        if inlist(type(key), int, slice):
            return yo._list_of_records.__setitem__(key, value)
        else:
            raise TypeError
    def append(yo, new_record):
        yo._list_of_records.append(new_record)
        yo._current_record = len(yo._list_of_records) - 1
    def bottom(yo):
        if yo._list_of_records:
            yo._current_record = 0
            return yo._list_of_records[0]
        raise DbfError("DbfList is empty")
    def current(yo):
        if yo._current_record < 0:
            raise Bof()
        elif yo._current_record == len(yo._list_of_records):
            raise Eof()
        return yo._list_of_records[yo._current_record]
    def count(yo, record):
        return yo._list_of_records.count(record)
    def extend(yo, new_records):
        yo._list_of_records.extend(new_records)
        yo._current_record = len(yo._list_of_records) - 1
    def goto(yo, index_number):
        if yo._list_of_records:
            record = yo[index_number]
            yo._current_record = index_number
            return yo._list_of_records[yo._current_record]
        raise DbfError("DbfList is empty")
    def index(yo, record, i=None, j=None):
        if i is None:
            i = 0
        if j is None:
            j = len(yo)
        return yo._list_of_records.index(record, i, j)
    def insert(yo, i, record):
        return yo._list_of_records.insert(i, record)
    def next(yo):
        if yo._current_record < len(yo._list_of_records):
            yo._current_record += 1
            if yo._current_record < yo._list_of_records:
                return yo._list_of_records[yo._current_record]
        raise Eof()
    def pop(yo, index=None):
        if index is None:
            return yo._list_of_records.pop()
        else:
            return yo._list_of_records.pop(index)
    def prev(yo):
        if yo._current_record > 0:
            yo._current_record -= 1
            if yo._current_record > -1:
                return yo._list_of_records[yo._current_record]
        raise Bof()
    def remove(yo, record):
        return yo._list_of_records.remove(record)
    def reverse(yo):
        return yo._list_of_records.reverse()
    def top(yo):
        if yo._list_of_records:
            yo._current_record = len(yo._list_of_records) - 1
            return yo._list_of_records[yo._current_record]
        raise DbfError("DbfList is empty")
    def sort(yo, cmp=None, key=None, reverse=None):
        if reverse is not None:
            return yo._list_of_records.sort(cmp, key, reverse)
        elif key is not None:
            return yo._list_of_records.sort(cmp, key)
        elif cmp is not None:
            return yo._list_of_records.sort(cmp)
        else:
            return yo._list_of_records.sort()
class Db4Table(DbfTable):
    version = 'dBase IV w/memos (non-functional)'
    _versionabbv = 'db4'
    _fieldtypes = {
            'C' : {'Type':'Character', 'Retrieve':_retrieveCharacter, 'Update':_updateCharacter, 'Blank':str, 'Init':_addCharacter},
            'Y' : {'Type':'Currency', 'Retrieve':_retrieveCurrency, 'Update':_updateCurrency, 'Blank':Decimal(), 'Init':_addVfpCurrency},
            'B' : {'Type':'Double', 'Retrieve':_retrieveDouble, 'Update':_updateDouble, 'Blank':float, 'Init':_addVfpDouble},
            'F' : {'Type':'Float', 'Retrieve':_retrieveNumeric, 'Update':_updateNumeric, 'Blank':float, 'Init':_addVfpNumeric},
            'N' : {'Type':'Numeric', 'Retrieve':_retrieveNumeric, 'Update':_updateNumeric, 'Blank':int, 'Init':_addVfpNumeric},
            'I' : {'Type':'Integer', 'Retrieve':_retrieveInteger, 'Update':_updateInteger, 'Blank':int, 'Init':_addVfpInteger},
            'L' : {'Type':'Logical', 'Retrieve':_retrieveLogical, 'Update':_updateLogical, 'Blank':bool, 'Init':_addLogical},
            'D' : {'Type':'Date', 'Retrieve':_retrieveDate, 'Update':_updateDate, 'Blank':Date.today, 'Init':_addDate},
            'T' : {'Type':'DateTime', 'Retrieve':_retrieveDateTime, 'Update':_updateDateTime, 'Blank':DateTime.now, 'Init':_addVfpDateTime},
            'M' : {'Type':'Memo', 'Retrieve':_retrieveMemo, 'Update':_updateMemo, 'Blank':str, 'Init':_addMemo},
            'G' : {'Type':'General', 'Retrieve':_retrieveMemo, 'Update':_updateMemo, 'Blank':str, 'Init':_addMemo},
            'P' : {'Type':'Picture', 'Retrieve':_retrieveMemo, 'Update':_updateMemo, 'Blank':str, 'Init':_addMemo},
            '0' : {'Type':'_NullFlags', 'Retrieve':_unsupportedType, 'Update':_unsupportedType, 'Blank':int, 'Init':None} }
    _memoext = '.dbt'
    _memotypes = ('G','M','P')
    _memoClass = _VfpMemo
    _yesMemoMask = '\x8b'               # 0011 0000
    _noMemoMask = '\x04'                # 0011 0000
    _fixedFields = ('B','D','G','I','L','M','P','T','Y')
    _decimalFields = ('F','N')
    _variableFields = ('C',)
    _numericFields = ('B','F','I','N','Y')
    _supported_tables = ('\x04', '\x8b')
    _dbfTableHeader = ['\x00'] * 32
    _dbfTableHeader[0] = '\x8b'         # version - Foxpro 6  0011 0000
    _dbfTableHeader[10] = '\x01'        # record length -- one for delete flag
    _dbfTableHeader[29] = '\x03'        # code page -- 437 US-MS DOS
    _dbfTableHeader = ''.join(_dbfTableHeader)
    _dbfTableHeaderExtra = ''
    useDeleted = True
    def _checkMemoIntegrity(yo):
        "dBase III specific"
        if yo._meta.header.version == '\x8b':
            try:
                yo._meta.memo = yo._memoClass(yo._meta)
            except:
                yo._meta.dfd.close()
                yo._meta.dfd = None
                raise
        if not yo._meta.ignorememos:
            for field in yo._meta.fields:
                if yo._meta[field]['type'] in yo._memotypes:
                    if yo._meta.header.version != '\x8b':
                        yo._meta.dfd.close()
                        yo._meta.dfd = None
                        raise DbfError("Table structure corrupt:  memo fields exist, header declares no memos")
                    elif not os.path.exists(yo._meta.memoname):
                        yo._meta.dfd.close()
                        yo._meta.dfd = None
                        raise DbfError("Table structure corrupt:  memo fields exist without memo file")
                    break
def add_fields(table, newfielddesc):
    table = Table(table)
    try:
        table.addFields(newfielddesc)
    finally:
        table.close()
def delete_fields(table, fielddesc):
    table = Table(table)
    try:
        table.deleteFields(fielddesc)
    finally:
        table.close()
def export(table, filename='', fieldlist='', format='csv', header=True):
    table = Table(table)
    try:
        table.export(filename, fieldlist, format, header)
    finally:
        table.close()
def first_record(table):
    table = Table(table)
    try:
        print str(table[0])
    finally:
        table.close()
def from_csv(csvfile, to_disk=False, diskname=None, fieldnames=None):
    reader = csv.reader(open(csvfile))
    if fieldnames is None:
        fieldnames = ['f0']
    else:
        fieldnames = fieldnames.replace(', ',',').split(',')
    mtable = Table(':memory:', '%s M' % fieldnames[0])
    field_count = 1
    for row in reader:
        while field_count < len(row):
            if field_count == len(fieldnames):
                fieldnames.append('f%d' % field_count)
            mtable.addFields('%s M' % fieldnames[field_count])
            field_count += 1
        mtable.append(tuple(row))
    if to_disk:
        if diskname is None:
            diskname = os.path.splitext(csvfile)[0]
        length = [1] * field_count
        for record in mtable:
            for i in range(field_count):
                length[i] = max(length[i], len(record[i]))
        fields = mtable.fields
        fielddef = []
        for i in range(field_count):
            if length[i] < 255:
                fielddef.append('%s C(%d)' % (fields[i], length[i]))
            else:
                fielddef.append('%s M' % (fields[i]))
        csvtable = Table(diskname, ','.join(fielddef))
        for record in mtable:
            csvtable.append(record.scatterFields())
    return mtable
def get_fields(table):
    table = Table(table)
    return table.fields
def info(table):
    table = Table(table)
    print str(table)
def rename_field(table, oldfield, newfield):
    table = Table(table)
    try:
        table.renameField(oldfield, newfield)
    finally:
        table.close()
def structure(table, field=None):
    table = Table(table)
    return table.structure(field)

