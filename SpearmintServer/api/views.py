from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from . import queue
from SpearmintServer.app.models import MongoDB

import spearmint
import json
import time


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


def get_db_uri():
    datum=MongoDB.objects.first()
    db_uri = 'mongodb://' + datum.username + ':' + datum.password + '@' + datum.db_address + '/spearmint'
    return db_uri


def get_db_address():
    datum=MongoDB.objects.first()
    db_address = datum.db_address
    return db_address

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
    db_uri = get_db_uri()
    spearmint.create_experiment(username, name, parameters, outcome, db_uri)
    response_data = {'name': name, 'username': username}
    return response_data


@login_required
@error_check
def find_experiment(request):
    name = request.GET['name']
    username = request.user.username
    db_uri = get_db_uri()
    found = spearmint.find_experiment(username, name, db_uri)
    response_data = {'name': name, 'result': found, 'username': username}
    return response_data

@login_required
@error_check
def find_jobs(request):
    name = request.GET['name']
    username = request.user.username
    db_uri = get_db_uri()
    jobs = spearmint.find_jobs(username, name, db_uri)
    response_data = {'name': name, 'jobs': jobs}
    return response_data

@login_required
@error_check
def get_mongodb_uri(request):
    db_uri = get_db_uri()
    response_data = {'db_uri': db_uri}
    return response_data

@login_required
@error_check
def find_all_experiments(request):
    username = request.user.username
    db_uri = get_db_uri()
    names = spearmint.find_all_experiments(username, db_uri)
    response_data = {'names': names}
    return response_data

@csrf_exempt
@login_required
@error_check
def delete_experiment(request):
    name = request.POST['name']
    username = request.user.username
    db_uri = get_db_uri()
    deleted = spearmint.delete_experiment(username, name, db_uri)
    response_data = {'name': name, 'result': deleted}
    return response_data

@login_required
@error_check
def get_suggestion(request):
    name = request.GET['name']
    username = request.user.username
    db_uri = get_db_uri()
    verbose = True

    # use queue for concurrency control
    queue_id = queue.enqueue('s')
    if verbose:
        print('>>> enqueued queue id = {0}'.format(queue_id))

    time_limit = 60 * 60 * 2 # 2 hours in seconds
    total_elapsed = 0 # seconds
    interval = 5 # seconds
    while True:
        if queue.peek('s',queue_id, upto_first_n=1):
            start_time = time.time()
            params = spearmint.get_suggestion(username, name, db_uri)
            elapsed_time = time.time() - start_time
            if verbose:
                print('*** took {0} sec. to get suggestion.'.format(elapsed_time))
            if params:
                response_data = {'name': name, 'params': params}
            else:
                response_data = {'name': name, 'params': None}
            queue.dequeue(queue_id)
            if verbose:
                print('<<< dequeued queue id = {0}'.format(queue_id))
            return response_data
        else:
            time.sleep(interval)
            total_elapsed += interval
            if verbose:
                print('--- been waiting {0} sec for queue_id = {1}'.format(total_elapsed, queue_id))
            if total_elapsed > time_limit:
                queue.dequeue(queue_id)
                raise Exception('timed out while getting suggestion')

@login_required
@error_check
def get_next_job_id(request):
    name = request.GET['name']
    username = request.user.username
    db_uri = get_db_uri()
    verbose = True

    # use queue for concurrency control
    queue_id = queue.enqueue('j')
    if verbose:
        print('>>> enqueued queue id = {0}'.format(queue_id))

    time_limit = 60 * 3 # 3 minutes in seconds
    total_elapsed = 0 # seconds
    interval = 1 # seconds
    while True:
        if queue.peek('j',queue_id, upto_first_n=1):
            start_time = time.time()
            job_id = spearmint.get_next_job_id(username, name, db_uri)
            elapsed_time = time.time() - start_time
            if verbose:
                print('*** took {0} sec. to get suggestion.'.format(elapsed_time))
            if job_id:
                response_data = {'name': name, 'job_id': job_id}
            else:
                response_data = {'name': name, 'job_id': None}
            queue.dequeue(queue_id)
            if verbose:
                print('<<< dequeued queue id = {0}'.format(queue_id))
            return response_data
        else:
            time.sleep(interval)
            total_elapsed += interval
            if verbose:
                print('--- been waiting {0} sec for queue_id = {1}'.format(total_elapsed, queue_id))
            if total_elapsed > time_limit:
                queue.dequeue(queue_id)
                raise Exception('timed out while getting suggestion')



@csrf_exempt
@login_required
@error_check
def post_update(request):
    data = json.loads(request.body)
    name = data['name']
    param_values = data['param_values']
    outcome_val = data['outcome_val']
    username = request.user.username
    spearmint.post_update(username, name, param_values, outcome_val, get_db_uri())
    response_data = {'name': name}
    return response_data
