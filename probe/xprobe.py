import getopt
import sys
import json
import threading
import time
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
def ping_target(target):
    target.ping(10,50)

def load_targets_from_collector(collector):
    pass

def load_targets_from_file(target_file):
    result = []
    with open(target_file) as f:
        data = json.load(f)
        for t in data['targets']:
            result.append(Target.make_from_json(t))
        f.close()
    return result

def usage():
    print("Usage: xprobe [-c <collector_address> | -t <target_file>]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:t:", ["collector=", "target="])

        (collector, target_file) = (None, None)

        for o, a in opts:
            if o in ("-c", "--collector"):
                collector = a
            elif o in ("-t", "--target"):
                target_file = a
            else:
                assert False, "unhandled option"

    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    if target_file:
        targets = load_targets_from_file(target_file)
    else:
        targets = load_targets_from_collector(collector)

    threads = []
    for t in targets:
        th = threading.Thread(target=ping_target, args=(t,))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    for t in targets:
        if t.pinged:
            print(f"Ping result [{t.address}]: {t.ping_min:.3f}ms/{t.ping_max:.3f}ms/{t.ping_avg:.3f}ms (min/max/avg) loss: {t.ping_loss:.2f}%")

if __name__ == '__main__':
    main()