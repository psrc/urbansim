#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os
import re
import sys

#
# Update the build number in the build number file.  Run by Fireman.
# Required:
#    First argument is the path to the build_number.py file for this Opus package.
#    Second argument is the build number (from Fireman)
#
build_number_file_path = sys.argv[1]
build_number = sys.argv[2]

build_line_pattern = re.compile("""^(\s*build\s*=\s*)('[^']+'|"[^"]+")(.*)$""")

f = open(build_number_file_path, 'r')
new_lines = []
for line in f:
    match = build_line_pattern.match(line)
    if match:
        updated_line = "%s'%s'%s\n" % (match.group(1), build_number, match.group(3))
        new_lines.append(updated_line)
        print "In file '%s'\nchanged line %s from:\n%sto:\n%s" % (build_number_file_path, len(new_lines), line, updated_line)
    else:
        new_lines.append(line)
f.close()

f = open(build_number_file_path, 'w')
f.writelines(new_lines)
f.close()

