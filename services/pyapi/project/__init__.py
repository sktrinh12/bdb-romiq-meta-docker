from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from functions import *
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)
app = Flask(__name__)
api = Api(app)


class GrabMetaData(Resource):
    def get(self, barcode):
        # ts = convert_ts(timestamp)
        # ts_str = format_datetime(ts)
        meta = get_meta(barcode)
        # print(meta)
        return meta, 200

class PostMetaData(Resource):
    def post(self):
        re_run = None
        data = request.form['data']
        script_name = request.form['script_name']
        barcode = request.form['barcode']
        if 're_run' in request.form:
            re_run = request.form['re_run']
        ts, dt = convert_pd_tuple(data, barcode)
        print(f'timestamp: {ts}')
        print(f'barcode: {barcode}')
        print(f'length of datalist: {len(dt)}')
        rtn = insert_meta(dt)
        # print(data)
        executor.submit(run_script_ssh, script_name, barcode=barcode, re_run=re_run)
        # output = 'test'
        output = f'{barcode} running in OmiqPipeline in background'
        return {'input_postgres': rtn, 'output' : output}, 201

api.add_resource(GrabMetaData, '/meta1/<string:barcode>')
api.add_resource(PostMetaData, '/meta1/post')

@app.route("/")
def test():
    return jsonify(hello="testing")

@app.route("/sshtest")
def ssh_cmdtest():
    output = run_script_ssh("test")
    return jsonify(output=output)
