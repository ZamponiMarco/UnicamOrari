import threading
import time


class Cache:
    """
    A cached function
    https://code.activestate.com/recipes/442513-caching-decorator-with-timeout-selective-invalidat/
    """

    #   a dict of sets, one for each instance of this class
    __allInstances = set()  # where the cached values are actually kept

    maxAge = 3600  # the default max allowed age of a cache entry (in seconds)
    collectionInterval = 2  # how long to wait between collection events
    __stopCollecting = False

    def __init__(self, func):
        Cache.__allInstances.add(self)
        self._store = {}
        self.__func = func

    def __del__(self):
        if self in Cache.__allInstances:
            Cache.__allInstances.remove(self)

    def __call__(self, *args, **kw):
        key = (args, tuple(sorted(kw.items())))
        if key in self._store:
            return self._store[key][1]

        result = self.__func(*args, **kw)
        self._store[key] = (time.time(), result)
        return result

    def invalidate(self):
        """Invalidate all cache entries for this function"""
        self._store.clear()

    def invalidate_one(self, *args, **kw):
        """Invalidate the cache entry for a particular set of arguments for this function"""
        key = (args, tuple(sorted(kw.items())))
        if key in self._store:
            del self._store[key]

    def collect(self):
        """Clean out any cache entries in this store that are currently older than allowed"""
        now = time.time()
        for key, v in self._store.items():
            t, value = v  # creation time, function output
            if 0 < self.maxAge < now - t:  # max ages of zero mean don't collect
                del self._store[key]

    @classmethod
    def collect_all(cls):
        """Clean out all old cache entries in all functions being cached"""
        for instance in cls.__allInstances:
            instance.collect()

    @classmethod
    def _start_collection(cls):
        """Periodically clean up old entries until the stop flag is set"""

        while cls.__stopCollecting is not True:
            time.sleep(cls.collectionInterval)
            cls.collect_all()

    @classmethod
    def start_collection(cls):
        """Start the automatic collection process in its own thread"""

        cls.collectorThread = threading.Thread(target=cls._start_collection)
        cls.collectorThread.setDaemon(False)
        cls.collectorThread.start()

    @classmethod
    def stop_collection(cls):
        cls.__stopCollecting = True

# -------------------
