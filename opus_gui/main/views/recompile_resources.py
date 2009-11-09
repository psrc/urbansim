# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# ABOUT THIS SCRIPT
# - This scripts updates the resource files for UrbanSim based on the content
# - of the Images sub folder. It both generates a qrc files and runs pyrcc4
# - on it.

import os

if __name__ == "__main__":

    RCFILE = 'opusmain.qrc'
    OUTFILE = 'opusmain_rc.py'

    files = os.listdir('./Images')
    images = [f for f in files if f.endswith('.png')]
    rcfile = open('./%s' %RCFILE, 'w')
    rcfile.write('<RCC>\n')
    rcfile.write('    <qresource prefix="/Images" >\n')
    for image in images:
        rcfile.write('        <file>Images/%s</file>\n' %image)
    rcfile.write('    </qresource>\n')
    rcfile.write('</RCC>')
    rcfile.close()
    print 'Wrote %d images to %s' %(len(images), RCFILE)
    os.system('pyrcc4 %s -o %s' %(RCFILE, OUTFILE))
    print 'Compiled to %s' %OUTFILE

