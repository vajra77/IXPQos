from .probe_result import ProbeResult
from influxdb import InfluxDBClient


class InfluxRepo:

    def __init__(self, hostname, port, dbname, dbuser, dbpass):
        self._client = InfluxDBClient(hostname, port, dbuser, dbpass)
        self._client.switch_database(dbname)

    def store_point(self, source, result: ProbeResult):
        jpoint = {
            "measurement": "Ping",
            "tags": {
                "source": source,
                "target": result.name,
                "status": result.status
            },
            "time": result.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "min": result.ping_min,
                "max": result.ping_max,
                "avg": result.ping_avg,
                "loss": result.ping_loss
            }
        }
        self._client.write_points([jpoint])

    def close(self):
        pass