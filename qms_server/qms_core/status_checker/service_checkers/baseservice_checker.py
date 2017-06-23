

class BaseServiceChecker(object):
    def __init__(self, service):
        self.service = service

    def check(self):
        raise NotImplementedError("Should be implemented in subclass")

    def ping(self):
        raise NotImplementedError('Should be implemented in subclass')
