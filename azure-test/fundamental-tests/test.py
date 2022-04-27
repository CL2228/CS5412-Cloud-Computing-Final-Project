import logging
import json
import datetime
import flask

import json
from numpy import reshape

from flask import Flask, Request, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET', 'POST'])
def func():
    form = request.form
    files = request.files
    print(form.keys())
    print(request.headers)
    print(files)

    res_headers = { 'Content-Type': 'application/json' }
    res_body = {}
    return Response(json.dumps({"msg": "hi"}), status=200, headers=res_headers)


if __name__ == "__main__":
    app.run()



















