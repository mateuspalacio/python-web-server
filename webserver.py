import socket
from threading import Thread
from pathlib import Path
from datetime import date, datetime
import os

class WebServer:

    def __init__(self, address='0.0.0.0', port=6789):
        self.port = port
        self.address = address

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.address, self.port))
            s.listen(10)

            while True:
                print('Waiting connections...')
                conn, addr = s.accept()
                req = HttpRequest(conn, addr)
                req.start()



class HttpRequest(Thread):

    def __init__(self, conn, addr):
        super(HttpRequest, self).__init__()
        self.conn = conn
        self.addr = addr
        self.CRLF = '\r\n'
        self.buffer_size = 4096

    def run(self):
        request = self.conn.recv(self.buffer_size)
        print(request)

        response = HttpResponse(self.conn, self.addr, '', request)
        response.processRespose()

        self.conn.close()


class HttpResponse:

    def __init__(self, conn, addr, file, req):
        self.conn = conn
        self.addr = addr
        self.file = file
        self.req = req

    def processRespose(self):
        message = self.req
        part = message.split(b" ")
        test = part[1].decode('utf-8')
        verSeExiste = Path(f"files/{test}")
        today = datetime.now()
        responseDate = today.strftime("%a, %d %b %Y %H:%M:%S %Z")
        try:
        # vendo se a pessoa pediu um arquivo...        
            if test == "/":
                    fileToRead=open('files/index.html','r')
                    s = fileToRead.read()
                    self.conn.sendall(
                    f'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nDate: {responseDate}\r\nAccept-Encoding: gzip\r\nAccept: */*\r\nContent-Type: text/html\r\n\r\n{s}'.encode(
                        'utf-8'))
            elif verSeExiste.is_file():
                splitFileName = test.split(".")
                fileExtension = splitFileName[1]
                if fileExtension == "html":              
                        fileToRead=open(f'files/{test}','r')
                        s = fileToRead.read()
                        self.conn.sendall(
                        f'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nDate: {responseDate}\r\nAccept-Encoding: gzip\r\nAccept: */*\r\nContent-Type: text/html\r\n\r\n{s}'.encode(
                            'utf-8'))
                elif fileExtension == "js":
                    fileToRead=open(f'files/{test}','r')
                    s = fileToRead.read()
                    self.conn.send(
                     f'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nDate: {responseDate}\r\nAccept-Encoding: gzip\r\nAccept: */*\r\nContent-Type: text/javascript\r\n\r\n<html><meta charset="UTF-8"/><body><script src="{s}"></script></body></html>'.encode(
                         'utf-8'))
                    # self.conn.send(
                    # f'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nContent-Type: text/javascript\r\n\r\n'.encode(
                    #     'utf-8'))
                elif fileExtension == "jpg" or fileExtension == "jpeg":                
                        s = open(f'files/{test}', 'rb').read()
                        HTTP_RESPONSE = b'\r\n'.join([
                                b"HTTP/1.0 200 OK",
                                b"Connection: keep-alive",
                                b"Accept-Encoding: gzip\r\nAccept: */*",
                                b"Content-Type: image/jpeg",
                                b'', s 
                                ] )
                        self.conn.sendall(HTTP_RESPONSE) 
                elif fileExtension == "png":
                        s = open(f'files/{test}', 'rb').read()
                        HTTP_RESPONSE = b'\r\n'.join([
                                b"HTTP/1.0 200 OK",
                                b"Connection: keep-alive",
                                b"Accept-Encoding: gzip\r\nAccept: */*",
                                b"Content-Type: image/png",
                                b'', s 
                                ] )
                        self.conn.sendall(HTTP_RESPONSE)                 
            else:
                fileToRead=open('files/error.html','r')
                s = fileToRead.read()
                self.conn.sendall(
                f'HTTP/1.0 404 Not Found\r\nConnection: close\r\nDate: {responseDate}\r\nAccept-Encoding: x-gzip\r\nAccept: */*\r\nContent-Type: text/html\r\n\r\n{s}'.encode(
                    'utf-8'))
        except:
            print("Unknown error")
            self.conn.sendall(
                f'HTTP/1.0 404 Not Found\r\nConnection: close\r\nDate: {responseDate}\r\nAccept-Encoding: x-gzip\r\nAccept: */*\r\nContent-Type: text/html\r\n\r\n<html><p>Unknown error</p></html>'.encode(
                    'utf-8'))
        # jpg/png
        # js 
        # Writing the HTML contents with UTF-8
        

