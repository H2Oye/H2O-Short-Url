from typing import Any
from flask import request, jsonify, make_response, Response

def getRequestParameter(request: request) -> dict:
    result = {}
    if request.method == 'GET':
        result = request.args
    elif request.method == 'POST':
        result = request.form
        if not result:
            result = request.get_json()
    return dict(result)

class GenerateResponse:
    def generate(self) -> Response:
        responseJson = jsonify({
            'code': self.code,
            'message': self.message,
            'data': self.data
        })
        response_ = make_response(responseJson)
        response_.status_code = self.httpCode
        response_.mimetype = 'application/json; charset=utf-8'
        return response_

    def error(self, code: int, message: str, httpCode=200) -> Response:
        self.code = code
        self.message = message
        self.data = None
        self.httpCode = httpCode
        return self.generate()

    def success(self, data: Any) -> Response:
        self.code = 200
        self.message = 'success'
        self.data = data
        self.httpCode = 200
        return self.generate()