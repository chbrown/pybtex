class FindFilterError(Exception):
    pass


def find_filter(type, name = None):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
        try:
            return getattr(m, s)
        except AttributeError:
            return None

    if name is None:
        name = import_('default')
    f = import_(name)
    if f is None:
        try:
            newname = import_('filetypes')[name]
        except KeyError:
            newname = name
        f= import_(newname)
        if f is None:
            raise FindFilterError('input filter for %s not found' % name)
    return f.Filter()
