from app.api import api
from app.logger import Logger
from app.config import APP_CONFIG
import json
from flask import jsonify, request


@api.route('/collector/targets', methods=['GET'])
#@api_auth_read
def API_list_targets():
    try:
        with open(APP_CONFIG["targets"]) as f:
           data = json.load(f)
        targets = data['targets']
    except Exception as e:
        Logger.crit(__name__ + ' : ' + str(e))
        return jsonify({"error": "unable to retrieve list of targets"}), 404
    else:
        return jsonify({ 'targets': [ t for t in targets ] }), 200
