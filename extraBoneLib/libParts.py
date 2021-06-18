import maya.cmds as cmds

from extraBoneLib import utils
from extraBoneLib import logging_util as log


top_log = log.Logger('EBL')


class Main():

    log = top_log.getLogger()

    def __init__(self):
        self.parts_info = {}
    
    def create(self, override_info={}):
        self.set_override_info(override_info)
        if not self.has_reference():
            return None
        return self.execute()
    
    def set_override_info(self, override_info):
        for info in self.parts_info:
            if info in override_info:
                self.parts_info[info] = override_info[info]
        
    def has_reference(self):
        return True
    
    def execute(self):
        return []

    def pprint(self, comment):
        printer = pprint.PrettyPrinter()
        printer.format = my_safe_repr
        self.log.info(printer.pprint(comment))


def my_safe_repr(object, context, maxlevelx, level):
    _type = pprint._type(object)
    if _type is unicode:
        object = str(object)
    return pprint._safe_repr(object, context, maxlevel, level)
