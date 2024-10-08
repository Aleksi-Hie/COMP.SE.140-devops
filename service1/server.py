import http.server
import subprocess
import socket
import json
import http
import requests
from http.server import BaseHTTPRequestHandler
__serviceName = "service1"
_service2 = "service2"
_service2Port = 8198
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
    res = requests.get(f"http://{address}:{_service2Port}")
    return res.json()

class WebRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        service1data = getSystemInfo()
        service2data = getSystem2Info(_service2)
        obj = {"service1": service1data,
               "service2": service2data}
        self.wfile.write(json.dumps(obj).encode("utf-8"))

def startServer(host, port):
    server = http.server.HTTPServer((host, port), WebRequestHandler)
    server.serve_forever()
    
startServer("0.0.0.0", 8199)