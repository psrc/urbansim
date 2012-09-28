from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello.  You have reached the opus rest interface.")

def run(request, run_id):
    return HttpResponse("You're looking at run %s." % run_id)

def config(request, run_id):
    return HttpResponse("You're looking at the configuration of run %s." % run_id)
