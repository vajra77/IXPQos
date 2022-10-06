from .probe_result import ProbeResult
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxRepo:

    def __init__(self, url, token, org):
        self._client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)

    def store_point(self, bucket, org, source, result: ProbeResult):
        p = influxdb_client.Point("Ping").tag("source", source). \
                tag("target", result.name).                 \
                tag("status", result.status).               \
                field("min", result.ping_min).              \
                field("max", result.ping_max).              \
                field("avg", result.ping_avg).              \
                field("jitter", result.ping_jitter).        \
                field("loss", result.ping_loss)
        self._write_api.write(bucket=bucket, org=org, record=p)

    def close(self):
        pass
