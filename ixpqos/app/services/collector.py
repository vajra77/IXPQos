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
        db = InfluxRepo(APP_CONFIG['url'],
                        APP_CONFIG['token'],
                        APP_CONFIG['org'])
        for t in probes:
            result = ProbeResult(
                t['name'],
                t['proto'],
                t['address'],
                "ok",
                t['ping_min'],
                t['ping_max'],
                t['ping_avg'],
                t['ping_jitter'],
                t['ping_loss'],
                timestamp
            )
            db.store_point(APP_CONFIG['bucket'], APP_CONFIG['org'], source, result)
        db.close()
