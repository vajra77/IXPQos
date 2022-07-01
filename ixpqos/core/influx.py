from .probed_target import ProbedTarget
from influxdb import InfluxDBClient


class InfluxDB:

    def __init__(self, hostname, port, dbname):
        self._client = InfluxDBClient(hostname, port)
        self._client.switch_database(dbname)

    def store_point(self, source, target: ProbedTarget):
        jpoint = {
            "measurement": "Ping",
            "tags": {
                "source": source,
                "target": target.name,
                "status": target.status
            },
            "time": target.timestamp,
            "fields": {
                "min": target.ping_min,
                "max": target.ping_max,
                "avg": target.ping_avg,
                "loss": target.ping_loss
            }
        }
        self._client.write(data=jpoint, protocol='json')

    def close(self):
        pass