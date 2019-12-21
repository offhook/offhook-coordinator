import requests
from requests.compat import urljoin
from flask import Flask, request, abort, Response
from models import DownloadSpec


app = Flask(__name__)
app.url_map.strict_slashes = False


def _get_agent_by_spec(spec):
    """ Returns the hostname and port for the agent which is able to serve the given spec """
    return 'localhost', 8081


def _build_url(host, port, path, protocol='http'):
    return urljoin(f'{protocol}://{host}:{port}', path)


@app.route('/search', methods=['POST'])
def search():
    spec = DownloadSpec.from_dict(request.json)
    agent_host, agent_port = _get_agent_by_spec(spec)
    agent_url = _build_url(agent_host, agent_port, request.path)
    agent_response = requests.request(request.method, agent_url, headers=request.headers, data=request.data)
    return Response(response=agent_response.content,
                    status=agent_response.status_code,
                    headers=dict(agent_response.headers))


@app.route('/download', methods=['POST'])
def submit_download_request():
    pass


@app.route('/download/<string:request_id>', methods=['GET'])
def get_download_request(request_id):
    pass


@app.route('/download/<string:request_id>/files', methods=['GET'])
def get_download_files(request_id):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
