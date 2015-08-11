from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import spearmint
import json

# Spearmint web API set

@login_required
def index(request):
    return HttpResponse('api root accessed by ' + request.user.username)

def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

# decorator to provide exception handling to api methods
def error_check(api):
    def error_checked(request):
        try:
            response = api(request)
        except Exception as e:
            response = {'error': str(e)}
        return json_response(response)
    return error_checked

@csrf_exempt
@login_required
@error_check
def create_experiment(request):
    if request.method != 'POST':
        raise ValueError('unexpected request method.')
    data = json.loads(request.body)
    name = data['name']
    parameters = data['parameters']
    outcome = data['outcome']
    username = request.user.username
    spearmint.create_experiment(username, name, parameters, outcome)
    response_data = {'name': name}
    return response_data

@login_required
@error_check
def find_experiment(request):
    name = request.GET['name']
    username = request.user.username
    found = spearmint.find_experiment(username, name)
    response_data = {'name': name, 'result': found}
    return response_data

@login_required
@error_check
def find_jobs(request):
    name = request.GET['name']
    username = request.user.username
    jobs = spearmint.find_jobs(username, name)
    response_data = {'name': name, 'jobs': jobs}
    return response_data

@login_required
@error_check
def find_all_experiments(request):
    username = request.user.username
    names = spearmint.find_all_experiments(username)
    response_data = {'names': names}
    return response_data

@csrf_exempt
@login_required
@error_check
def delete_experiment(request):
    name = request.POST['name']
    username = request.user.username
    deleted = spearmint.delete_experiment(username, name)
    response_data = {'name': name, 'result': deleted}
    return response_data

@login_required
@error_check
def get_suggestion(request):
    name = request.GET['name']
    username = request.user.username
    params = spearmint.get_suggestion(username, name)
    if params:
        response_data = {'name': name, 'params': params}
    else:
        response_data = {'name': name, 'params': None}
    return response_data

@csrf_exempt
@login_required
@error_check
def post_update(request):
    data = json.loads(request.body)
    name = data['name']
    username = request.user.username
    outcome_val = data['outcome_val']
    spearmint.post_update(username, name, outcome_val)
    response_data = {'name': name}
    return response_data
