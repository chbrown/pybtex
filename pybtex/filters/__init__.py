class FindFilterError(Exception):
    pass


def find_filter(type, name = None):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
	try:
	   return getattr(m, s)
	except AttributeError:
	   raise ImportError('s')

    if name is None:
        name = import_('default')
    try:
        f = import_(name)
    except ImportError:
        try:
            f= import_(import_('filetypes')[name])
        except IndexError:
            raise FindFilterError('filter %s not found', name)
    return f.Filter()
