from ixpqos.app import APP_CONFIG
from ixpqos.lib import ProbedTarget. InfluxDB
from datetime import datetime
import json


class CollectorSrv:

    @classmethod
    def list_targets(cls):
        with open(APP_CONFIG["targets"]) as f:
            data = json.load(f)
        targets = data['targets']
        return targets

    @classmethod
    def store_result(cls, source, targets):
        timestamp = datetime.now()
        db = InfluxDB(APP_CONFIG['dbhost'],
                      APP_CONFIG['dbport'],
                      APP_CONFIG['dbname'])
        for t in targets:
            probed_target = ProbedTarget(
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
            db.store_point(source, probed_target)
        db.close()
