from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from functions import *

app = Flask(__name__)
api = Api(app)


class GrabMetaData(Resource):
    def get(self, timestamp):
        ts = convert_ts(timestamp)
        ts_str = format_datetime(ts)
        meta = get_meta(ts_str)
        # print(meta)
        return meta, 200

class PostMetaData(Resource):
    def post(self):
        re_run = None
        data = request.form['data']
        script_name = request.form['script_name']
        if 're_run' in request.form:
            re_run = request.form['re_run']
        ts, dt = convert_pd_tuple(data)
        print(f'timestamp: {ts}')
        rtn = insert_meta(dt)
        # print(data)
        output = run_script_ssh(script_name, ts, re_run)
        return {'input_postgres': rtn, 'output' : output}, 201

api.add_resource(GrabMetaData, '/meta1/<string:timestamp>')
api.add_resource(PostMetaData, '/meta1/post')

@app.route("/")
def test():
    return jsonify(hello="testing")

@app.route("/sshtest")
def ssh_cmdtest():
    output = run_script_ssh("test")
    return jsonify(output=output)
