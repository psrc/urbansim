#
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


import platform, sys

"""
Replacements is a dictionary to be used in % formatting expressions, to generate
file extensions for file caches.  These will depend on whether the architecture is
32 or 64 bit, and whether it is little-endian or big-endian.
"""
   
replacements = {}

if sys.byteorder=='little':
    replacements['endian'] = 'l'
    replacements['numpy_endian'] = '<'
else:
    replacements['endian'] = 'b'
    replacements['numpy_endian'] = '>'
    
if platform.architecture()[0]=='64bit':
    replacements['bytes'] = 8
else:
    replacements['bytes'] = 4
