from ixpqos.app.api import api
from ixpqos.app.logger import Logger
from ixpqos.app.api.auth import api_auth
from ixpqos.app.services import CollectorSrv as SRV
from flask import jsonify, request


@api.route('/conf/probes', methods=['GET'])
@api_auth
def API_list_probes():
    try:
        probes = SRV.list_probes()
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to retrieve list of probes"}), 404
    else:
        return jsonify({ 'probes': [t for t in probes] }), 200


@api.route('/data/probe-result', methods=['POST'])
@api_auth
def API_store_result():
    try:
        data = request.json
        source = data['source']
        probes = data['probes']
        SRV.store_result(source, probes)
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to store probe result"}), 500
    else:
        return jsonify({'status': 'ok'}), 200

@api.route('/data/probe/:sid/last', methods=['GET'])
@api_auth
def API_get_last(tid):
    try:
        result = SRV.get_last(sid)
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to retrieve probe"}), 404
    else:
        return jsonify({ "result": result })