import locale
class BackendBase:
    def __init__(self, encoding = locale.getpreferredencoding()):
        self.encoding = encoding
