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
    url = requests.get(f"http://{remote}:5000/api/v1/collector/targets")
    data = json.loads(url.text)
    for t in data['targets']:
        result.append(Target.make_from_json(t))
    return result

def load_targets_from_file(local_file):
    result = []
    with open(local_file) as f:
        data = json.load(f)
        for t in data['targets']:
            result.append(Target.make_from_json(t))
        f.close()
    return result

def usage():
    print("Usage: xprobe [-r address | -l file] [-d delay] [-c count]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:l:c:d:", ["remote=", "local=", "count=", "delay="])

        (remote, local) = (None, None)
        count = 10
        delay = 50.0
        for o, a in opts:
            if o in ("-c", "--count"):
                count = int(a)
            elif o in ("-l", "--local"):
                local = a
            elif o in ("-d", "--delay"):
                delay = float(a)
            elif o in ("-r", "--remote"):
                remote = a
            else:
                assert False, "unrecognized option"

        if not local and not remote:
            assert False, "no remote address nor local file specified"

    except Exception as err:
        print(err)
        usage()
        sys.exit(2)

    if local:
        targets = load_targets_from_file(local)
    else:
        targets = load_targets_from_server(remote)

    threads = []
    for t in targets:
        th = threading.Thread(target=ping_target, args=(t,count,delay,))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    for t in targets:
        if t.pinged:
            print(f"Ping result [{t.address}]: {t.ping_min:.3f}ms/{t.ping_max:.3f}ms/{t.ping_avg:.3f}ms (min/max/avg) loss: {t.ping_loss:.1f}%")

if __name__ == '__main__':
    main()