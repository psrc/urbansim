# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


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
