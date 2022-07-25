

class ProbeResult:

    def __init__(self, name, proto, address, status, pmin, pmax, avg, jitter, loss, timestamp):
        self._name = name
        self._proto = proto
        self._address = address
        self._status = status
        self._ping_min = pmin
        self._ping_max = pmax
        self._ping_avg = avg
        self._ping_jitter = jitter
        self._ping_loss = loss
        self._timestamp = timestamp

    @property
    def timestamp(self):
        return self._timestamp

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
    def status(self):
        return self._status

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
