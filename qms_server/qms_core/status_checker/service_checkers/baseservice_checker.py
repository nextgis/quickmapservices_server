

class BaseServiceChecker(object):
    def __init__(self, service, timeout=10):
        self.service = service
        self.timeout = timeout

    def check(self):
        raise NotImplementedError("Should be implemented in subclass")

    def ping(self):
        raise NotImplementedError('Should be implemented in subclass')
