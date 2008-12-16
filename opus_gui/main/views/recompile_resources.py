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

# ABOUT THIS SCRIPT
# - This scripts updates the resource files for UrbanSim based on the content
# - of the Images sub folder. It both generates a qrc files and runs pyrcc4
# - on it.

import os

if __name__ == "__main__":

    TMPFILE = '_tmp_resource.qrc'
    OUTFILE = 'opusmain_rc.py'

    files = os.listdir('./Images')
    images = [f for f in files if f.endswith('.png')]
    rcfile = open('./%s' %TMPFILE, 'w')
    rcfile.write('<RCC>\n')
    rcfile.write('    <qresource prefix="/Images" >\n')
    for image in images:
        rcfile.write('        <file>Images/%s</file>\n' %image)
    rcfile.write('    </qresource>\n')
    rcfile.write('</RCC>')
    rcfile.close()
    print 'Wrote %d images to %s' %(len(images), TMPFILE)
    os.system('pyrcc4 %s -o %s' %(TMPFILE, OUTFILE))
    print 'Compiled to %s' %OUTFILE
    os.remove(TMPFILE)

