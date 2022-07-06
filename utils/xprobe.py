import requests, json, threading, time, sys, getopt
from ping3 import ping


# Helper class
class Target:

    def __init__(self, name, proto, address):
        self._name = name
        self._proto = proto
        self._address = address
        self._pinged = False
        self._ping_min = None
        self._ping_max = None
        self._ping_avg = None
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
    def ping_loss(self):
        return self._ping_loss

    def ping(self, count, delay):
        rtt = [None]*count
        for i in range(count):
            rtt[i] = ping(self._address, unit="ms")
            time.sleep(delay/1000.0)

        # check for packet loss
        lost = 0
        (min, max, sum) = (100000.0, .0, .0)
        for ms in rtt:
            if not ms:
                lost += 1
            else:
                if ms > max:
                    max = ms
                if ms < min:
                    min = ms
                sum += ms

        packet_loss = float(lost)/float(count) * 100.0
        avg = sum/float(count)
        self._ping_min = min
        self._ping_max = max
        self._ping_avg = avg
        self._ping_loss = packet_loss
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
            "ping_loss": self._ping_loss
        }
        return result

    @classmethod
    def make_from_json(cls, jdata):
        return cls(jdata['name'],
                   jdata['proto'],
                   jdata['address'])

# APP FUNCTIONS
def ping_target(target, count, delay):
    target.ping(count, delay)

def load_targets_from_server(remote):
    result = []
    url = requests.get(f"https://{remote}/api/v1/targets")
    data = json.loads(url.text)
    for t in data['targets']:
        result.append(Target.make_from_json(t))
    return result

def usage():
    print("Usage: utils -n name [-k key] [-r address] [-d delay] [-c count]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "k:n:r:c:d:", ["key=", "name=", "remote=", "count=", "delay="])

        (key, name, remote) = (None, None, None)
        count = 10
        delay = 50.0
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
            assert False, "mandatory utils name missing"

    except Exception as err:
        print(err)
        usage()
        sys.exit(2)

    targets = load_targets_from_server(remote)
    threads = []
    for t in targets:
        if name != t.name:
            th = threading.Thread(target=ping_target, args=(t,count,delay,))
            threads.append(th)
            th.start()

    for th in threads:
        th.join()

    jtargets = []
    for t in targets:
        if name != t.name:
            jtargets.append(t.to_dict())

    jresult = {
        "source": name,
        "targets": jtargets
    }

    response = requests.post(f"https://{remote}/api/v1/result", json=jresult)
    if response.status_code == 200:
        exit(0)
    else:
        data = response.json()
        print(f"ERROR: {data['error']}", file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    main()