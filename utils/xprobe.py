import requests
import json
import threading
import time
import sys
import getopt
import math
from ping3 import ping


DEFAULT_DELAY = 1000.00  # milliseconds
DEFAULT_COUNT = 10


# Helper class
class Probe:

    def __init__(self, name, proto, address):
        self._name = name
        self._proto = proto
        self._address = address
        self._pinged = False
        self._ping_min = None
        self._ping_max = None
        self._ping_avg = None
        self._ping_jitter = None
        self._ping_loss = None

    @property
    def pinged(self):
        return self._pinged

    @property
    def name(self):
        return self._name

    @property
    def proto(self):
        return self._proto

    @property
    def address(self):
        return self._address

    @property
    def ping_min(self):
        return self._ping_min

    @property
    def ping_max(self):
        return self._ping_max

    @property
    def ping_avg(self):
        return self._ping_avg

    @property
    def ping_jitter(self):
        return self._ping_jitter

    @property
    def ping_loss(self):
        return self._ping_loss

    def ping(self, count, delay):
        rtt = []
        for i in range(count + 1):
            rtt.append(ping(self._address, unit="ms"))
            time.sleep(delay/1000.0)

        # we clean up the first ping which is usually an outlier
        clean_rtt = rtt[1:count+1]
        plost = 0
        (pmin, pmax, psum, pavg, psdev) = (100000.0, .0, .0, .0, .0)
        for ms in clean_rtt:
            if not ms:
                plost += 1
            else:
                if ms > pmax:
                    pmax = ms
                if ms < pmin:
                    pmin = ms
                psum += ms
        pavg = psum/float(count - plost)
        for ms in clean_rtt:
            psdev += (ms - pavg) ** 2
        pjit = math.sqrt(psdev/float(count))
        self._ping_min = pmin
        self._ping_max = pmax
        self._ping_avg = pavg
        self._ping_jitter = pjit
        self._ping_loss = float(plost)/float(count)
        self._pinged = True

    def to_dict(self):
        result = {
            "name": self._name,
            "proto": self._proto,
            "address": self._address,
            "pinged": self._pinged,
            "ping_min": self._ping_min,
            "ping_max": self._ping_max,
            "ping_avg": self._ping_avg,
            "ping_jitter": self._ping_jitter,
            "ping_loss": self._ping_loss
        }
        return result

    @classmethod
    def make_from_json(cls, jdata):
        return cls(jdata['name'],
                   jdata['proto'],
                   jdata['address'])


# APP FUNCTIONS
def ping_probe(probe, count, delay):
    probe.ping(count, delay)


def load_probes_from_server(remote, api_key):
    result = []
    url = requests.get(f"https://{remote}/backend/api/v1/conf/probes", headers={"X-API-Key": api_key})
    data = json.loads(url.text)
    for t in data['probes']:
        result.append(Probe.make_from_json(t))
    return result


def usage():
    print("Usage: xprobe -n name -k key -r address [-d delay] [-c count]")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "k:n:r:c:d:", ["key=", "name=", "remote=", "count=", "delay="])

        (key, name, remote) = ("", None, None)
        count = DEFAULT_COUNT
        delay = DEFAULT_DELAY
        for o, a in opts:
            if o in ("-c", "--count"):
                count = int(a)
            elif o in ("-d", "--delay"):
                delay = float(a)
            elif o in ("-r", "--remote"):
                remote = a
            elif o in ("-n", "--name"):
                name = a
            elif o in ("-k", "--key"):
                key = a
            else:
                assert False, "unrecognized option"

        if not remote:
            assert False, "no remote ixpqos address specified"

        if not name:
            assert False, "mandatory probe name missing"

    except Exception as err:
        print(err, file=sys.stderr)
        usage()
        sys.exit(2)

    try:
        probes = load_probes_from_server(remote, key)
    except Exception as e:
        print(f"error while getting probes: {e}", file=sys.stderr)
        sys.exit(2)

    threads = []
    
    for t in probes:
        if name != t.name:
            th = threading.Thread(target=ping_probe, args=(t, count, delay,))
            threads.append(th)
            th.start()

    for th in threads:
        th.join()

    jprobes = []
    for t in probes:
        if name != t.name:
            jprobes.append(t.to_dict())

    jresult = {
        "source": name,
        "probes": jprobes
    }

    response = requests.post(f"https://{remote}/backend/api/v1/data/probe-result",
                             json=jresult,
                             headers={'X-API-Key': key})
    if response.status_code == 200:
        exit(0)
    else:
        data = response.json()
        print(f"ERROR: {data['error']}", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
