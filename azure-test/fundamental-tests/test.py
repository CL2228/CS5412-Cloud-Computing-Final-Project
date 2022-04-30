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
    print(form)
    print(files)


    res_headers = { 'Content-Type': 'application/json' }
    res_body = {"msg": "hi"}
    return Response(json.dumps(res_body), status=200, headers=res_headers)


if __name__ == "__main__":
    app.run()



















