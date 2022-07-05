from influxdb import InfluxDBClient


def test_influx_write():
    client = InfluxDBClient('sys.namex.it', 8086)
    client.switch_database('ixpqos_devel')
    jpoint = {
        "measurement": "Test",
        "tags": {
            "source": "rom1-ixpqos",
            "target": "rom2-ixpqos",
            "status": "ok"
        },
        "time": "2018-03-29T8:05:00Z",
        "fields": {
            "min": 0.2,
            "max": 2.1,
            "avg": 1.7,
            "loss": 0.8
        }
    }
    assert client.write_points([jpoint])