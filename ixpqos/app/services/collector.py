from ixpqos.app import APP_CONFIG
from ixpqos.core import ProbeResult, InfluxRepo
from datetime import datetime
import json


class CollectorSrv:

    @classmethod
    def list_probes(cls):
        with open(APP_CONFIG["probes"]) as f:
            data = json.load(f)
        probes = data['probes']
        return probes

    @classmethod
    def store_result(cls, source, probes):
        timestamp = datetime.now()
        db = InfluxRepo(APP_CONFIG['dbhost'],
                      APP_CONFIG['dbport'],
                      APP_CONFIG['dbname'],
                        APP_CONFIG['dbuser'],
                        APP_CONFIG['dbpass'])
        for t in probes:
            result = ProbeResult(
                t['name'],
                t['proto'],
                t['address'],
                "ok",
                t['ping_min'],
                t['ping_max'],
                t['ping_avg'],
                t['ping_loss'],
                timestamp
            )
            db.store_point(source, result)
        db.close()