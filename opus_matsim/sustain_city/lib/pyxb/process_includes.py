# Opus/UrbanSim urban simulation software
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#!/opt/local/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python
# -*- mode: pymode; coding: latin1; -*-
"""
Synopsis:
    Recusively process the include elements in an XML Schema file.
    Produce a single file that contains all included content.
    Input is read either from a file or from stdin.
    Output is written either to a file or to stdout.
Usage:
    python process_includes.py [options] [ infile [ outfile ] ]
Options:
    -h, --help      Display this help message.
    -f, --force     Force.  If outfile exists, overwrite without asking.
    -s, --search    Search path for schemas.  Colon separated list of directorys where schemas may be found.
    
Examples:
    python process_includes.py infile.xsd
    python process_includes.py infile.xsd outfile.xsd
    python process_includes.py infile.xsd > outfile.xsd
    cat infile.xsd | python process_includes.py > outfile.xsd
"""

#
# Imports

import copy
import sys
import os
import getopt
import re
import urllib

#
# Try to import lxml first, and if that fails try ElementTree.
# lxml preserves namespace prefixes, but ElemenTree does not.
#
WhichElementTree = ''
try:
    from lxml import etree
    WhichElementTree = 'lxml'
except ImportError, e:
    from xml.etree import ElementTree as etree
    WhichElementTree = 'elementtree'
if WhichElementTree != 'lxml' or etree.LXML_VERSION[0] < 2:
    print '***'
    print '*** Error: Must install lxml (v. >= 2.0) or use "--no-process-includes".'
    print '***     Override this error by modifying the above test.'
    print '***     But, see the docs before doing so:'
    print '***       http://www.rexx.com/~dkuhlman/generateDS.html#include-file-processing'
    print '***'
    raise RuntimeError, 'Must install lxml (v. >= 2.0) or use "--no-process-includes".'
#print WhichElementTree, etree


#
# Globals and constants

FORCE = False
NAMESPACE_PAT = re.compile(r'\{.*\}')
DIRPATH = []


#
# Classes



#
# Functions


def process_includes(inpath, outpath):
    if inpath:
        infile = open(inpath, 'r')
    else:
        infile = sys.stdin
    if outpath:
        outfile = make_file(outpath)
    else:
        outfile = sys.stdout
    process_include_files(infile, outfile)
    if inpath:
        infile.close()
    if outpath:
        outfile.close()


def process_include_files(infile, outfile):
    doc = etree.parse(infile)
    root = doc.getroot()
    process_include_statements(root)
    doc.write(outfile)


def process_path(root, idx, path):
    # Load the schema from path and include all children of its root node
    # as children of the main root.
    doc = etree.parse(path)
    node = doc.getroot()
    new_path = split_base_path(path)
    children1 = reversed(node.getchildren())
    for child1 in children1:
        if child1.__class__ is etree._Element:
            child1.set('path_', new_path)
        root.insert(idx, copy.copy(child1))

def process_include_statements(root):
    alreadyProcessed = set()
    global DIRPATH
    
    idx = 0
    children = root.getchildren()
    while idx < len(children):
        child = children[idx]
        tag = child.tag
        if type(tag) == type(""):
            tag = NAMESPACE_PAT.sub("", tag)
        else:
            tag = None
##         if tag == 'include' and 'schemaLocation' in child.attrib:
##             idx += 1
##             locn = child.attrib['schemaLocation']
##             path = child.attrib['schemaLocation']
##             if path in alreadyProcessed:
##                 root.remove(child)
##                 continue
##             repl = etree.Comment(etree.tostring(child))
##             root.replace(child, repl)
##             path1 = make_path(root, path)
##             if os.path.exists(path1):
##                 process_path(root, idx, path1)
##             else:
##                 for d in DIRPATH:
##                     path = make_path(root, path)
##                     path1 = os.path.join(d,locn)
##                     if os.path.exists(path1):
##                         process_path(root, idx, path1)
##                         break
##                 else:
##                     msg = "Can't find include file %s.  Aborting." % (path, )
##                     raise IOError(msg)
##             alreadyProcessed.add(path)
##         elif ((tag == 'include' or tag == 'import') and
        if ((tag == 'include' or tag == 'import') and
            'schemaLocation' in child.attrib):
            idx += 1
            locn = child.attrib['schemaLocation']
            if locn in alreadyProcessed:
                root.remove(child)
                continue
            repl = etree.Comment(etree.tostring(child))
            root.replace(child, repl)
            if locn.startswith('ftp:') or locn.startswith('http:'):
                try:
                    path, msg = urllib.urlretrieve(locn)
                    process_path(root, idx, path)
                except:
                    msg = "Can't retrieve import file %s.  Aborting." % (locn, )
                    raise IOError(msg)
            else:
                path1 = make_path(child, locn)
                if os.path.exists(path1):
                    process_path(root, idx, path1)
                else:
                    for d in DIRPATH:
                        path = make_path(root, locn)
                        path1 = os.path.join(d,locn)
                        if os.path.exists(path1):
                            process_path(root, idx, path1)
                            break
                    else:
                        msg = "Can't find import file %s.  Aborting." % (locn, )
                        raise IOError(msg)
            alreadyProcessed.add(locn)
        else:
            idx += 1
        children = root.getchildren()

def make_file(outFileName):
    global FORCE
    outFile = None
    if (not FORCE) and os.path.exists(outFileName):
        reply = raw_input('File %s exists.  Overwrite? (y/n): ' % outFileName)
        if reply == 'y':
            outFile = open(outFileName, 'w')
    else:
        outFile = open(outFileName, 'w')
    return outFile


def split_base_path(path):
    path1 = os.path.split(path)[0]
    return path1


def make_path(root, path):
    path1 = root.get('path_', '.')
    path2 = os.path.join(path1, path)
    return path2


USAGE_TEXT = __doc__

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    global FORCE
    global DIRPATH
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'hfs:', ['help', 'force', 'search=',])
    except:
        usage()
    name = 'nobody'
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-f', '--force'):
            FORCE = True
        elif opt in ('-s', '--search'):
            DIRPATH = val.split(':')
    if len(args) == 2:
        inpath = args[0]
        outpath = args[1]
    elif len(args) == 1:
        inpath = args[0]
        outpath = None
    elif len(args) == 0:
        inpath = None
        outpath = None
    else:
        usage()
    process_includes(inpath, outpath)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


