# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import sys, os, inspect
from string import find, join, lower, split, strip, rfind, rstrip
from pydoc import pathdirs, ispackage, synopsis, Scanner

class ModuleScanner(Scanner):
    """A modified version of the ModuleScanner from pydoc.
    This version only scan files whose top-level directory has a 'opus_package_info.py'.
    
    An interruptible scanner that searches module synopses."""
    def __init__(self):
        roots = [(dir, '') for dir in pathdirs()]
        Scanner.__init__(self, roots, self.submodules, self.isnewpackage)
        self.inodes = [os.stat(dir_pkg[0]).st_ino for dir_pkg in roots]

    def submodules(self, xxx_todo_changeme):
        (dir, package) = xxx_todo_changeme
        children = []
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if ispackage(path):
                children.append((path, package + (package and '.') + file))
            else:
                children.append((path, package))
        children.sort() # so that spam.py comes before spam.pyc or spam.pyo
        return children

    def isnewpackage(self, xxx_todo_changeme1):
        (dir, package) = xxx_todo_changeme1
        inode = os.path.exists(dir) and os.stat(dir).st_ino
        if not (os.path.islink(dir) and inode in self.inodes):
            self.inodes.append(inode) # detect circular symbolic links
            return ispackage(dir)
        return False

    def run(self, callback, key=None, completer=None):
        if key: key = lower(key)
        self.quit = False
        seen = {}

        for modname in sys.builtin_module_names:
            if modname != '__main__':
                seen[modname] = 1
                if key is None:
                    callback(None, modname, '')
                else:
                    desc = split(__import__(modname).__doc__ or '', '\n')[0]
                    if key in lower('%s - %s' % (modname, desc)):
                        callback(None, modname, desc)

        while not self.quit:
            node = next(self)
            if not node: break
            path, package = node
            path_parts = split(path, os.sep)
            
            build_path = ''
            
            found_package_info = False
            for path in path_parts:
                if path.endswith(':'): path = os.path.join(path, os.sep)
                
                build_path = os.path.join(build_path, path)
                
                if os.path.exists(os.path.join(build_path, 'opus_package_info.py')):
                    found_package_info = True
                    break
            
            if not found_package_info: continue
            
            modname = inspect.getmodulename(path)
            if os.path.isfile(path) and modname:
                modname = package + (package and '.') + modname
                if not modname in seen:
                    seen[modname] = 1 # if we see spam.py, skip spam.pyc
                    if key is None:
                        callback(path, modname, '')
                    else:
                        desc = synopsis(path) or ''
                        if key in lower('%s - %s' % (modname, desc)):
                            callback(path, modname, desc)
        if completer: completer()

