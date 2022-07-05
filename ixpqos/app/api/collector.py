from ixpqos.app.api import api
from ixpqos.app.logger import Logger
from ixpqos.app.services import CollectorSrv as SRV
from flask import jsonify, request


@api.route('/targets', methods=['GET'])
#@api_auth_read
def API_list_targets():
    try:
        targets = SRV.list_targets()
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to retrieve list of targets"}), 404
    else:
        return jsonify({ 'targets': [t for t in targets] }), 200


@api.route('/result', methods=['POST'])
#@api_auth_write
def API_store_result():
    try:
        data = request.json
        source = data['source']
        targets = data['targets']
        SRV.store_result(source, targets)
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to store ping result"}), 404
    else:
        return jsonify({'status': 'ok'}), 200
