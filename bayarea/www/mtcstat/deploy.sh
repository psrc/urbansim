# Simple script to deploy mtcstat to proper test directory

TOMCAT_ROOT=/var/lib/tomcat6/webapps

if [ "$USER" = "" ]; then
	echo "USER variable not set!"
	exit 1
fi

if [ ! -d "${TOMCAT_ROOT}" ]; then
	echo "I couldn't find a tomcat root dir.  Are you on the right machine?"
	exit 1
fi

if [ ! -d ${TOMCAT_ROOT}/${USER} ]; then
	echo "You ($USER) don't seem to have a tomcat test dir."
	echo "Please ask someone to create it for you."
	exit 1
fi

rsync -r --delete --exclude=.svn `dirname $0`/ ${TOMCAT_ROOT}/${USER}/
