from .probe_result import ProbeResult
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxRepo:

    def __init__(self, url, token, org):
        self._org = org
        self._client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._client.query_api()


    def store_point(self, bucket, source, result: ProbeResult):
        p = influxdb_client.Point("Ping").tag("source", source). \
                tag("target", result.name).                 \
                tag("status", result.status).               \
                field("min", result.ping_min).              \
                field("max", result.ping_max).              \
                field("avg", result.ping_avg).              \
                field("jitter", result.ping_jitter).        \
                field("loss", result.ping_loss)
        self._write_api.write(bucket=bucket, org=self._org, record=p)


    def retrieve_point(self, bucket, source, target):
        query_str = f"from(bucket: \"{bucket}\") \
            |> range(start: -10m) \
            |> filter(fn:(r) => r._measurement == \"Ping\")\
            |> filter(fn:(r) => r.source == \"{source}\")\
            |> filter(fn:(r) => r.target == \"{target}\")\
            |> last()"
        result = self._query_api.query(org=self._org, query=query_str)
        point = {}
        for table in result:
            for record in table.records:
                point[record.get_field()] = record.get_value()
        return point


    def close(self):
        pass
