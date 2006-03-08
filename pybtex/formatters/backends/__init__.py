import locale
class BackendBase:
    def __init__(self, encoding = None):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        self.encoding = encoding
