import json
import socket
import threading
import traceback

from HandlerFile import Handler
from TokenFile import b64_encode
from RequestParserFile import RequestParser
from ResponseFile import Response

MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class MyHTTPServer:
    def __init__(self, host, port, server_name, handler: Handler):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._handler = handler

    def handle(self, conn, addr):
        print("addr " + str(addr))
        try:
            # Client connected
            self.serve_client(conn)
        except Exception as e:
            print('Client serving failed', e)

    # Socket creating, give conn to serve_client
    def serve_forever(self):
        # Socket creating
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            print("bind pre")
            serv_sock.bind((self._host, self._port))
            print("bind post")
            serv_sock.listen()
            print("bind listening")

            while True:
                print("accept pre")
                conn, addr = serv_sock.accept()
                print("accept post")
                threading.Thread(target=self.handle, args=(conn, addr,)).start()
        finally:
            serv_sock.close()

    # Just call parse, handle, send_resp
    def serve_client(self, conn):
        # TODO
        req = None
        try:
            reqParser = RequestParser(conn, self._server_name, self._port)
            req = reqParser.parse_request()
            resp = self._handler.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            traceback.print_exc()
            self.send_error(conn, e)
        finally:
            if conn:
                # TODO: Client serving failed local variable 'req' referenced before assignment
                req.rfile.close()
                conn.close()


    #Makes headers and sends response
    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers.items():
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)
