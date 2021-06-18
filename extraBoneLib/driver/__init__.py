from maya import cmds

from . import quatDriver


def create(*args, **kwargs):
    driver_type = args[0]
    target = kwargs.get('target', None)

    if driver_type == 'mayaQuatDriver':
        return quatDriver.create(target, **kwargs)
