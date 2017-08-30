from orchestrator.apiendpoints.constants import Constants
import socket
import json


def send_data_to_socket(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((Constants.TCP_IP, Constants.TCP_PORT))
    data = json.dumps(data, ensure_ascii=False)
    sock.sendall(data)
    result = sock.recv(1024)
    sock.close()
    return result
