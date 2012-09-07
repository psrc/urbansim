#!/bin/bash

# the MTC model relies on a python virtualenv with numpy and scipy optimized
# for linear algebra, and non-free dependencies.  These components are system
# specific.  So for the MTC model to run on multiple systems, we need a way to
# maintain multiple python virtual envs.  We achive this by storing the
# separate virtualenvs in separate branches of a git tree.  The branches are
# named by reading /etc/issue and replacing ' ' and '\' with '_'.  This script
# fetches the correct branch of the git tree using this convention.  If the
# target git tree already exists, it will be updated with the latest from the
# correct branch.

# Note that this scheme implies some maintenance headaches.  Specifically, if
# you must make changes that DO NOT require updating existing binary files to
# all of the virtualenvs, you must make the changes in master and rebase all of
# the branches.  If you must update existing binary files, you must commit them
# in each branch independently.  Painful.

set -e
U=$USER
DEST=pyatlas

while getopts ":d:u:" opt; do
  case $opt in
    d)
      DEST=$OPTARG
      ;;
    u)
      U=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

GIT_URL="ssh://$U@paris.urbansim.org/var/git/pyatlas"
GIT_BRANCH=`cat /etc/issue`
GIT_BRANCH=`echo ${GIT_BRANCH} | sed 's/[\\ ]/_/g'`

BRANCHES=`git ls-remote --heads ${GIT_URL}`
set +e
echo $BRANCHES | grep -w ${GIT_BRANCH} > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "pyatlas does not currently support " ${GIT_BRANCH}
    exit 1
fi
set -e

if [ -e ${DEST} ]; then
    cd ${DEST} && git reset --hard HEAD && git pull -f
else
    git clone -b ${GIT_BRANCH} ${GIT_URL} ${DEST}
fi
