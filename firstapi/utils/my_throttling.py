from rest_framework.throttling import BaseThrottle
import time

VERIFY_THROTTLING = {}
VISITE_TIME = 10

class DefineThrottling(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        ipaddr = request.META.get("REMOTE_ADDR")
        ctime = time.time()
        if ipaddr not in VERIFY_THROTTLING:
            VERIFY_THROTTLING[ipaddr] = [ctime,]
            return True
        history = VERIFY_THROTTLING.get(ipaddr)
        self.history = history
        while history and history[-1] < ctime - VISITE_TIME:
            history.pop()
        if len(history) < 3:
            history.insert(0,ctime)
            print(history)
            return True

    def wait(self):
        ctime = time.time()
        wait_time = VISITE_TIME - (ctime - self.history[-1])
        return wait_time