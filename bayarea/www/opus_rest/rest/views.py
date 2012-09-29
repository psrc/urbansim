from django.http import HttpResponse
from rest.models import RunActivity
import simplejson as json
from django.shortcuts import get_object_or_404
import zlib, pickle
from django.conf import settings

def run_to_dict(r):
    d = {
        "run_id": r.run_id,
        "run_name": r.run_name,
        "run_description": r.run_description,
        "scenario_name": r.scenario_name,
        "cache_directory": r.cache_directory,
        "processor_name": r.processor_name,
        "date_time": str(r.date_time),
        "status": r.status,
        "project_name": r.project_name,
    }
    # Augment this with some data from resources.  Note that resources may or
    # may not be compressed.  The run manager determines this based on his
    # config file.  We just guess.
    try:
        c = pickle.loads(zlib.decompress(str(r.resources)))
    except zlib.error:
        c = pickle.loads(str(r.resources))

    # we have to be careful only to add serializable elements to the dictionary
    for k in ['project_name', 'hudson_details', 'models', 'years', 'base_year',
              'models_configuration', 'travel_model_configuration', 'models_in_year']:
        d[k] = c[k]
    return d

def add_headers(r):
    r['Access-Control-Allow-Origin']  = settings.XS_SHARING_ALLOWED_ORIGINS
    return r

def index(request):
    recent_runs = RunActivity.objects.all().order_by('-date_time')
    recent_run_jsons = map(run_to_dict, recent_runs)
    return add_headers(HttpResponse(json.dumps(recent_run_jsons), mimetype="application/json"))

def run(request, run_id):
    r = get_object_or_404(RunActivity, pk=run_id)
    j = run_to_dict(r)
    return add_headers(HttpResponse(json.dumps(j), mimetype="application/json"))
