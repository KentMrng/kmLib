from maya import cmds


def undo(func):
    def _undofunc(*args, **kwargs):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
    return _undofunc


def load_plugins(*plugins):
    if not isinstance(plugins, (list, tuple)):
        plugins = [plugins]
    
    for plugin in plugins:


def flags(long_name='', short_name='', default_value=None, kwargs_dict={}):
    value = kwargs.get(long_name, default_value)
    value = kwargs.get(short_name, long_name)
    return value
