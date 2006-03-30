class FindPluginError(Exception):
    pass
def find_plugin(type, name):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
        try:
            return getattr(m, s)
        except AttributeError:
            return None

    f = import_(name)
    if f is None:
        raise FindPluginError('plugin %s not found in %s' % (name, type))
    return f
