from .probed_target import ProbedTarget
from influxdb import InfluxDBClient


class InfluxRepo:

    def __init__(self, hostname, port, dbname, dbuser, dbpass):
        self._client = InfluxDBClient(hostname, port, dbuser, dbpass)
        self._client.switch_database(dbname)

    def store_point(self, source, target: ProbedTarget):
        jpoint = {
            "measurement": "Ping",
            "tags": {
                "source": source,
                "target": target.name,
                "status": target.status
            },
            "time": target.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "min": target.ping_min,
                "max": target.ping_max,
                "avg": target.ping_avg,
                "loss": target.ping_loss
            }
        }
        self._client.write_points([jpoint])

    def close(self):
        pass