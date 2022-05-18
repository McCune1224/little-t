from flask import Flask, jsonify, make_response, request
from mongo_database.MongoWriter import MongoWriter
app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route("/callback")
def callback():
    mw = MongoWriter()
    args = request.args
    if 'code' in args:
         mw.insert_callback_token(code=args['code'], state=args['state'])
         return jsonify(message="Got State and Code Tokens")
    else:
         return jsonify(args)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error=f'Not found!{e}'), 404)
