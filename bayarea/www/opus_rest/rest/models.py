# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ComputedIndicators(models.Model):
    id = models.IntegerField(primary_key=True)
    indicator_name = models.TextField(blank=True)
    dataset_name = models.TextField(blank=True)
    expression = models.TextField(blank=True)
    run_id = models.IntegerField(null=True, blank=True)
    data_path = models.TextField(blank=True)
    processor_name = models.TextField(blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    project_name = models.TextField(blank=True)
    class Meta:
        db_table = u'computed_indicators'

class RunActivity(models.Model):
    run_id = models.IntegerField(primary_key=True)
    run_name = models.TextField(blank=True)
    run_description = models.TextField(blank=True)
    scenario_name = models.TextField(blank=True)
    cache_directory = models.TextField(blank=True)
    processor_name = models.TextField(blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    status = models.TextField(blank=True)
    resources = models.TextField(blank=True)
    project_name = models.TextField(blank=True)
    class Meta:
        db_table = u'run_activity'

