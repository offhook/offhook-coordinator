import sched
import threading
import time

import requests
from requests.compat import urljoin
from flask import Flask, request, abort, Response
from models import DownloadSpec, DownloadRequest


REQUEST_KEEPING_TIMEOUT_SEC = 30  # 60 * 60 * 12  # 12 hours


app = Flask(__name__)
app.url_map.strict_slashes = False
request_id_to_agent = {}
scheduler = sched.scheduler(time.time, time.sleep)


def _get_agent_by_spec(spec):
    """ Returns the hostname and port for the agent which is able to serve the given spec """
    return 'localhost', 8081


def _build_url(host, port, path, protocol='http'):
    return urljoin(f'{protocol}://{host}:{port}', path)


def _build_new_response_from_agent_response(agent_response):
    return Response(response=agent_response.content,
                    status=agent_response.status_code,
                    headers=dict(agent_response.headers))


def _forward_request_by_id(request_id):
    if request_id not in request_id_to_agent:
        abort(404)

    agent_host, agent_port = request_id_to_agent[request_id]
    agent_url = _build_url(agent_host, agent_port, request.path)
    agent_response = requests.request(request.method, agent_url, headers=request.headers, data=request.data)

    return _build_new_response_from_agent_response(agent_response)


def _delete_request(request_id):
    del request_id_to_agent[request_id]


def _schedule_request_deletion(request_id):
    scheduler.enter(REQUEST_KEEPING_TIMEOUT_SEC, 1, _delete_request, (request_id,))
    scheduler.run()


@app.route('/search', methods=['POST'])
def search():
    spec = DownloadSpec.from_dict(request.json)
    agent_host, agent_port = _get_agent_by_spec(spec)
    agent_url = _build_url(agent_host, agent_port, request.path)
    agent_response = requests.request(request.method, agent_url, headers=request.headers, data=request.data)

    return _build_new_response_from_agent_response(agent_response)


@app.route('/download', methods=['POST'])
def submit_download_request():
    dl_req = DownloadRequest.from_dict(request.json)
    agent_host, agent_port = _get_agent_by_spec(dl_req.spec)
    agent_url = _build_url(agent_host, agent_port, request.path)
    agent_response = requests.request(request.method, agent_url, headers=request.headers, data=request.data)

    resp_json = agent_response.json()
    returned_dl_req = DownloadRequest.from_dict(resp_json)
    request_id_to_agent[returned_dl_req.id] = (agent_host, agent_port)

    job_thread = threading.Thread(target=_schedule_request_deletion, args=(returned_dl_req.id,))
    job_thread.start()

    return _build_new_response_from_agent_response(agent_response)


@app.route('/download/<string:request_id>', methods=['GET'])
def get_download_request(request_id):
    return _forward_request_by_id(request_id)


@app.route('/download/<string:request_id>/files', methods=['GET'])
def get_download_files(request_id):
    return _forward_request_by_id(request_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
