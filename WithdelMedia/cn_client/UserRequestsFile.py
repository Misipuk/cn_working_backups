import json
import socket
from typing import Dict

PORT = 9090


class UserRequest:

    def getCafes(self, auth_token: str):  # with Reviews
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'GET /cafes HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def getCafeMedia(self, auth_token: str, cafe_id: int):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'GET /cafe/media?cafe_id=%d HTTP/1.1 \n' % cafe_id)
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = bytes()
        while True:
            got = client_sock.recv(1024)
            if len(got) == 0:
                break
            data += got
        client_sock.close()
        print('Received', repr(data))

    def add_cafe_media(self, auth_token: str, cafe_id: int, file_to_img: str):  # with Reviews
        with open(file_to_img, mode='rb') as f:
            body = f.read()

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'POST /cafe/media?cafe_id=%d&type=photo HTTP/1.1 \n' % cafe_id)
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'Content-Length: %d\n' % len(body))
        client_sock.sendall(b'\n')
        client_sock.sendall(body)
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def getCafeReviews(self, auth_token: str, cafe_id: int):  # with Reviews
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'GET /cafe/review?cafe_id=%d HTTP/1.1 \n' % cafe_id)
        #client_sock.sendall(b'POST /cafe/media?cafe_id=%d&type=photo HTTP/1.1 \n' % cafe_id)
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def delCafeMedia(self): # TODO
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'POST /delcafemedia HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(
            b'Authorization: eyJsb2dpbiI6ICJQYW5BbGVoYSIsICJleHBpcmUiOiAxNTkwMjY2MjQyLCAia2V5IjogInJhVFVsNDV2aW0yOFpIeHBMTjl5U1hwN1o2TEU1OUF6R0MtWXFwR1Ryb3M9In0=\n')
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))


    def add_cafe_review(self, auth_token: str, review: Dict[str, str]):  # with Reviews
        body = json.dumps(review).encode()

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'POST /cafe/review HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Content-Length: %d\n' % len(body))
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        client_sock.sendall(body + b'\n')
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def delReview(self,  auth_token: str, rev_id: int, us_log: str):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'DELETE /cafe/review?rev_id=%d&us_log=PanAleha HTTP/1.1 \n' % rev_id)
        # client_sock.sendall(b'POST /cafe/media?cafe_id=%d&type=photo HTTP/1.1 \n' % cafe_id)
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def register(self, login: str, password: str):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        body = json.dumps({"login": login, "password": password})
        client_sock.sendall(b'POST /users HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Content-Length: ' + str(len(body)).encode() + b'\n')
        client_sock.sendall(b'\n')
        client_sock.sendall(body.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def login(self, login: str, password: str) -> str:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        body = json.dumps({"login": login, "password": password})
        client_sock.sendall(b'POST /login HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Content-Length: ' + str(len(body)).encode() + b'\n')
        client_sock.sendall(b'\n')
        client_sock.sendall(body.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))
        # TODO
        return "eyJsb2dpbiI6ICJQaXp6YU93bmVyIiwgImV4cGlyZSI6IDE1OTAzMDU4MTcsICJrZXkiOiAiTkNCUGk2QWxicVJtQ3AzenR3d0pCcG9CdzFNY3l2ekRXMHpScXRPVUlHND0ifQ=="

    def get_users(self, auth_token: str):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'GET /users HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def add_cafe(self, auth_token: str, cafe: Dict[str, str]):
        body = json.dumps(cafe).encode()

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'POST /cafe?kek=kek HTTP/1.1 \n')
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Content-Length: %d\n' % len(body))
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        client_sock.sendall(body + b'\n')
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))

    def delCafeMedia(self, auth_token: str, cafe_id: int):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', PORT))
        client_sock.sendall(b'DELETE /cafe/media?cafe_id=%d&file_id=1 HTTP/1.1 \n' % cafe_id)
        # client_sock.sendall(b'POST /cafe/media?cafe_id=%d&type=photo HTTP/1.1 \n' % cafe_id)
        client_sock.sendall(b'Host: MyServer\n')
        client_sock.sendall(b'Accept: application/json\n')
        client_sock.sendall(b'Authorization: %s\n' % auth_token.encode())
        client_sock.sendall(b'\n')
        data = client_sock.recv(1024)
        client_sock.close()
        print('Received', repr(data))
