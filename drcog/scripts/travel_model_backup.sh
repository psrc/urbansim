#! /bin/sh

set -e

# Simple stupid backup for travel model on detroit
# Expects detroit to be mounted in /mnt
DATE_STRING=$(date +%Y%m%d)

cd /var/backups/mtc_travel_model_backups/
tar czf travel_model_$DATE_STRING.tar.gz "/mnt"

#Remove backup older than 4 weeks
OLD_DATE=$(date --date="4 weeks ago" +%Y%m%d)
if [ `ls | grep travel_model_$OLD_DATE.tar.gz | wc -l` > 0 ]; then
	rm travel_model_$OLD_DATE.tar.gz
fi
