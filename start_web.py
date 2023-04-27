from flask import Flask, jsonify, request
import docker
import os
from gevent.pywsgi import WSGIServer
from run_free import start_docker_containers as startdc 


app = Flask(__name__)


@app.route('/start-new')
def start_new():
    a = request.args.get('start-port', default=18080, type=int)
    if a:
        new_ports=startdc(start_port=a) 
    else:
        new_ports=startdc() 
    return new_ports

@app.route('/docker-info')
def docker_info():
    client = docker.from_env()
    containers = client.containers.list()
    container_info = []
    for container in containers:
        
        port_info = container.ports
        if port_info:
            port_info = [f"{key}:{value[0]['HostPort']}" for key, value in port_info.items()]
        else:
            port_info = "N/A"
        info = {
            'created': container.attrs['Created'],
            'status': container.status,
            'ports': port_info
        }
        container_info.append(info)
    return jsonify(container_info)

def start_server(port):
    # Check if port is already in use
    os.system(f"fuser -k {port}/tcp > /dev/null 2>&1")
    # Start WSGI server
    print("starting WSGI server")
    http_server = WSGIServer(('localhost', port), app)
    http_server.serve_forever()

if __name__ == '__main__':
    start_server(8080)

