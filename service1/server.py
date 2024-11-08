import http.server
import subprocess
import socket
import json
import http
import requests
import os
import time
from http.server import BaseHTTPRequestHandler
__serviceName = os.environ.get("SERVICE_NAME")
_service2 = "service2"
_service2Port = 8200
def getIp():
    return socket.gethostbyname(__serviceName)

def runShellCommand(command):
    output = subprocess.run(str.split(command, " "), capture_output=True)
    out_ = output.stdout.decode("utf-8")
    return out_

def getSystemInfo():
    data = {
        "ip": getIp(),
        "processes": runShellCommand("ps -ax"),
        "diskspace": runShellCommand("df"),
        "reboottime": runShellCommand("uptime -p")
    }
    return data

def getSystem2Info(address):
    res = requests.get(f'http://{address}')
    return res.json()

class WebRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == "/shutdown":
            self.send_response(200)
            getSystem2Info(f'{_service2}:{_service2Port}/shutdown/')
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        service1data = getSystemInfo()
        service2data = getSystem2Info(f"{_service2}:{_service2Port}")
        obj = {"service1": service1data,
               "service2": service2data}
        self.wfile.write(json.dumps(obj).encode("utf-8"))
        self._handled = True
        return


class MyServer(http.server.HTTPServer):
    def process_request(self, request, client_address):
        super().process_request(request, client_address)
        time.sleep(2)


def startServer(host, port):
    server = MyServer((host, port), WebRequestHandler)
    server.serve_forever()
    
startServer("0.0.0.0", 8199)