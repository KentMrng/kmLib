from maya import cmds


driven_curve_types = ['animCurveUA', 'animCurveUL', 'animCurveUT', 'animCurveUU']




def set_drivenKeys(driver_attr, driven_attr, 
                   driver_values, driven_values, 
                   driver_ctrl_attrs=[], **kwargs):
    if not driver_ctrl_attrs:
        driver_ctrl_attrs = [driver_attr]
    
    if isinstance(driver_ctrl_attrs, list):
        driver_ctrl_attrs = [driver_ctrl_attrs]

    values = [cmds.getAttr(attr) for attr in driver_ctrl_attrs]
    init_value = cmds.getAttr(driven_attr)

    for driver_value, driven_value in zip(driver_values, driven_values):
        for driver_ctrl_attr in driver_ctrl_attrs:
            set_attr_if_settable(driver_ctrl_attr, driver_value)
        cmds.setAttr(driven_attr, driven_value)
        cmds.setDrivenKeyframe(driven_attr, 
                               currentDriver=driver_attr, 
                               driverValue=driver_value, 
                               value=driven_value)
    
    for driver_ctrl_attr, value in zip(driver_ctrl_attrs, values):
        set_attr_if_settable(driver_ctrl_attr, value)
    cmds.setAttr(driven_attr, init_value)

    connections = get_source_connections(driven_attr)
    driver_curves = cmds.ls(connections, type=driven_curve_types)
    if driver_curves:
        for attr_name, value in kwargs.items():
            attr = '{0}.{1}'.format(driver_curves[0], attr_name)
            if not cmds.objExists(attr):
                continue
            cmds.setAttr(attr, value)            

    return driver_curves[0]


def set_attr_if_settable(attr, value):
    if cmds.getAttr(attr, settable=True):
        cmds.setAttr(attr, value)


def get_source_connections(node):
    connections = cmds.listConnections(node, destination=False)
    return connections


def delete_drivenKey(*nodes):
    for node in nodes:
        connections = get_source_connections(node)
        for anim_curve in cmds.ls(connections, type=driven_curve_types)
            cmds.delete(anim_curve)
