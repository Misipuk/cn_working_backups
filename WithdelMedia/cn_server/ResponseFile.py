import json
from typing import Dict


class Response:
    def __init__(self, status, reason, headers: Dict = None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        if body is not None and body is not bytes and type(body) is not bytes:
            body = json.dumps(body.__dict__).encode()
        self.body = body
