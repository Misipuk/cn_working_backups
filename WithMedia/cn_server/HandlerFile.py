import json
import time
from typing import Union, Optional

from CafesFile import Cafe, Cafes
from HTTPErrorFile import HTTPError
from MediaFileClass import MediaFile, MediaFiles
from RequestFile import Request
from ResponseFile import Response
from ReviewsFile import Review, Reviews, now
from TokenFile import Token
from UsersFile import User, Users


class Handler:

    def __init__(self, users: Users, cafes: Cafes, media_files: MediaFiles, cafes_reviews: Reviews):
        self._cafes_reviews = cafes_reviews
        self._media_files = media_files
        self._users = users
        self._cafes = cafes

    def handle_request(self, req: Request):
        user_login = None
        if "Authorization" in req.headers:
            try:
                user_login = Token.as_token(req.headers["Authorization"])
            except KeyError as ke:
                return HTTPError(403, "Forbidden", body=("token must have key " + str(ke)).encode())
            except Exception as e:
                return HTTPError(403, "Forbidden", body=str(e).encode())

        print(req.path, req.query, req.url)

        if req.path == '/users' and req.method == 'POST':#REGISTRATION
            return self.handle_post_users(req)

        if req.path == '/login' and req.method == 'POST':#LOGIN
            return self.handle_login_user(req)

        if req.path == '/users' and req.method == 'GET': #GET ALL USERS LIST
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_users(req, user_login)


        if req.path == '/cafes' and req.method == 'GET': #TODO # withMeanStars
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_cafes(req)

        if req.path == '/cafe/media' and req.method == 'GET': #TODO
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_cafe_media(req)

        if req.path == '/cafe/media' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_add_cafe_media(req, user_login)

        if req.path == '/cafe/media' and req.method == 'DELETE': #TODO
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_del_cafe_media(req)

        if req.path == '/cafe' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_put_cafe(req, user_login)

        # if req.path == '/cafe' and req.method == 'POST':
        #     if user_login is None:
        #         return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
        #     return self.handle_edit_cafe(req)

        if req.path == '/cafe/review' and req.method == 'GET':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_reviews(req)

        if req.path == '/cafe/review' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_add_review(req, user_login)

        if req.path == '/cafe/review' and req.method == 'DELETE': #TODO
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_del_review(req, user_login)

        """if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)"""

        raise HTTPError(404, 'Not found')

    def handle_get_reviews(self, req):
        cafe_id = req.query["cafe_id"][0]
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps([v.__dict__ for v in self._cafes_reviews._cafe_reviews.get(int(cafe_id))])
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    def handle_get_cafes(self, req):
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps([v.__dict__ for (k, v) in self._cafes._cafes.items()])
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    #TODO
    def handle_get_cafe_media(self, req):
        cafe_id = req.query["cafe_id"][0]
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps([v.__dict__ for v in self._media_files.get(int(cafe_id))])
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    def handle_put_cafe(self, req: Request, login: str):
        cafe = Handler.read_cafe_from_req_body(req)
        cafe.owner = login
        id_check = self._cafes._owner_login.get(login)
        # print("id = "+str(id_check))
        if id_check != None:
            cafe.id = id_check
        b = self._cafes.put(cafe)
        #if b == -1:
           # return HTTPError(403, 'Forbidden')
        return Response(204, 'Created', body=cafe)

    #TODO
    def handle_del_cafe_media(self, req):
        pass

    def handle_add_review(self, req, login: str):
        review = Handler.read_cafe_review_from_req_body(req)
        review.owner = login
        self._cafes_reviews.put(review)
        return Response(204, 'Created', body=review)

    #TODO
    def handle_del_review(self, req, login: str):
        rev_id = req.query["rev_id"][0]
        us_log = login
        self._cafes_reviews.del_by_userlogin(us_log, int(rev_id))
        #mf = MediaFile(int(cafe_id), tp)
        #mf = self._media_files.put(mf, req.body())
        return Response(204, 'Deleted')

    def handle_add_cafe_media(self, req, login: str):
        tp = req.query["type"][0]
        cafe_id = req.query["cafe_id"][0]
        id_check = self._cafes._owner_login.get(login)
        #print("id = "+str(id_check))
        if id_check != int(cafe_id):
            return HTTPError(403, 'Forbidden')
        mf = MediaFile(int(cafe_id), tp)
        mf = self._media_files.put(mf, req.body())
        return Response(204, 'Created', body=mf)

    def handle_post_users(self, req):
        user = self.read_user_from_request_body(req)
        _ = self._users.put(user)
        user = user.copy()
        if _ == -1:
            return HTTPError(403, 'Forbidden')
        user.password = None
        return Response(204, 'Created', body=user)

    def handle_get_users(self, req, user_login: str):
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps([v.__dict__ for (k, v) in self._users._users.items()])
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    def handle_get_user(self, req, user_id):
        user = self._users.get(int(user_id))
        if not user:
            raise HTTPError(404, 'Not found')

        accept = req.headers.get('Accept')
        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(user)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return HTTPError(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    def handle_login_user(self, req: Request) -> Union[Response, HTTPError]:
        user_from_req = self.read_user_from_request_body(req)
        user_from_db = self._users.get_by_login(user_from_req.login)

        if user_from_db is None:
            # user not found, 404
            return HTTPError(404, 'Not Found')

        if user_from_db.password != user_from_req.password:
            # forbidden, 403
            return HTTPError(403, 'Forbidden')

        ts = int(time.time())
        token = Token.as_authorization(user_from_db.login, ts + 3600)
        return Response(200, 'OK', headers={"Authorization": token})

    @staticmethod
    def read_user_from_request_body(req) -> User:
        body = json.loads(req.body())
        user = User()
        user.id = None
        user.login = body["login"]
        user.password = body["password"]
        return user

    @staticmethod
    def read_cafe_from_req_body(req) -> Cafe:
        body = json.loads(req.body())
        return Cafe(
            body["owner"],
            body["name"],
            body["des"],
            body["city"],
            id=Handler.get_int_or_none(body, "id"),
        )

    @staticmethod
    def read_cafe_review_from_req_body(req) -> Review:
        body = json.loads(req.body())
        return Review(
            body["owner"],
            int(body["cafe_id"]),
            int(body["stars"]),
            now(),
            body["description"],

        )

    @staticmethod
    def get_or_none(body, key: str) -> Optional[str]:
        try:
            return body[key]
        except KeyError:
            return None

    @staticmethod
    def get_int_or_none(body, key: str) -> Optional[int]:
        try:
            return int(body[key])
        except KeyError:
            return None
