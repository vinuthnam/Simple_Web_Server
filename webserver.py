from socket import *
import threading
from time import sleep

def onNewClient(clientsocket,addr):
    while True:
        message = clientsocket.recv(5000)
        output = parseRequest(message)
        path = output["path"][1:]
        if (path == ""): 
            path = "index"
        try:
            with open(f'{path}.html', 'rb') as file:
                html = file.read()
                sleep(20)
                clientsocket.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode())
                clientsocket.sendall(html)
        except:
            clientsocket.send('HTTP/1.1 400 Not Found\n\n'.encode())
            break
        finally:
            clientsocket.shutdown(SHUT_WR)

def parseRequest(request):
  output = {}
  r = request.decode("utf-8").split("\r\n")
  parts = r[0].split(' ')
  output["method"] = parts[0]
  output["path"] = parts[1]
  print(output["path"])
  output["protocol"] = parts[2]
  output["headers"] = { (kv.split(':')[0]): kv.split(':')[1].strip() for kv in r[1:] if (len(kv.split(':')) > 1) }
  return output


def start_server(host='localhost', port=8080):
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind((host,port))

    serversocket.listen(5)
    while True:
        clientsocket, addr = serversocket.accept()
        thread = threading.Thread(target = onNewClient,args = (clientsocket,addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")
        # print(thread.name)
        # sleep(20)

if __name__ == "__main__":
    start_server()