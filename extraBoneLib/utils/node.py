import maya.api.OpenMaya as om
from maya import cmds

import extraBoneLib.utils as ut
from extraBoneLib import driver


def create_transform(**kwargs):
    name = ut.flags('name', 'n', 'null#', kwargs)
    parent = ut.flags('parent', 'p', '', kwargs)
    lock = ut.flags('lock', 'l', '', kwargs)
    non_keyable = ut.flags('nonKeyable', 'nk', '', kwargs)

    opt = {'n': name}
    if parent:
        opt['p'] = parent

    transform = cmds.create('transform', **opt)
    all_keyable = cmds.istAttr(transform, keyable=True)

    if lock:
        if lock == 'all':
            lock = all_keyable
        elif isinstance(lock, str):
            lock = lock.split('')
        for attr in lock:
            cmds.setAttr('{0}.{1}'.format(transform, attr), lock=True)
    
    if non_keyable:
        if non_keyable == 'all':
            non_keyable = all_keyable
        elif isinstance(non_keyable, str):
            non_keyable = non_keyable.split('')
        for attr in non_keyable:
            cmds.setAttr('{0}.{1}'.format(transform, attr), keyable=False)
    
    return transform


def duplicate_joint(joint, **kwargs):
    name = ut.flags('name', 'n', 'dupJnt#', kwargs)
    parent = ut.flags('parent', 'p', False, kwargs)

    dup_joint = cmds.createNode('joint', name=name, parent=joint)
    cmds.setAttr(dup_joint + '.jo', *(0, 0, 0))

    if parent:
        joint_parent = cmds.listRelatives(joint, parent=True)
        if joint_parent is not None:
            cmds.parent(dup_joint, parent)

    return dup_joint


def create_bend_joint(joint, **kwargs):
    name = ut.flags('name', 'n', 'bendJnt#', kwargs)

    dup_joint = duplicate_joint(joint, name=name)
    cmds.connectAttr(joint + '.t', dup_joint + '.t')
    cmds.connectAttr(joint + '.r', dup_joint + '.r')

    driver.create('mayaQuatDriver',
                  target=joint,
                  yaw_axis='Y',
                  pitch_axis='Z',
                  roll_axis='X')
    
    _add_non_existent_attr(dup_joint, 'yaw', 'doubleAngle', keyable=True)
    _add_non_existent_attr(dup_joint, 'pitch', 'doubleAngle', keyable=True)
    _add_non_existent_attr(dup_joint, 'roll', 'doubleAngle', keyable=True)


def _add_non_existent_attr(node, longname, attributeType, **kwargs):
    if not cmds.objExists('{0}.{1}'.format(node, attribute_name)):
        cmds.addAttr(node,
                     longname=longname,
                     attributeType=attributeType,
                     **kwargs)

def driven_joint_key(driven_info, side, driver, parent):
    joints = []

    if not driven_info:
        return joint

    for info in driven_info:
        if info.get('side', None) and info['side'] != side:
            continue

        driver = info['driver']
        joint = driver.format(side) if '{}' in driver else driver
        behavior = info.get('behavior', False)
        if behavior:
            if is_behavior(behavior, driver):
                print('# BehaviorJnt {0} >> {1}'.format(behavior, driver))
                behavior = True
        joints.append(joint)
        add_driven_joint(driver,
                         name=joint,
                         parent=parent, 
                         drivenKeys=info['drivenKeys'], 
                         behavior=behavior)
    
    return joints


def add_driven_joint(driver, **kwargs):
    name = ut.flags('name', 'n', 'driverJnt#', kwargs)
    parent = ut.flags('parent', 'p', None, kwargs)
    drivenKeys = ut.flags('drivenKeys', 'dks', [], kwargs)
    behavior = ut.flags('behavior', 'beh', False, kwargs)

    if not cmds.objExists(name):
        cmds.createNode('joint', name=name)

    cmds.setAttr(name + '.radius', 1.5)
    
    if parent and cmds.objExists(parent):
        cmds.parent(name, parent, relative=True)
    
    for drivenKey in drivenKeys:
        opt = drivenKey.get('opt', {})
        
        if behavior and not is_scale_attr(drivenKey['driven']):
            for i, value in enumerate(drivenKey['driven_value']):
                drivenKey['driven_value'][i] = value * -1
        
        driver = '{0}.{1}'.format(driver, drivenKey['driver'])
        driven = '{0}.{1}'.format(name, drivenKey['driven'])

        ut.drivenKey.set_drivenKeys(
            driver, driven,
            driver_value=drivenKey['driver_value'],
            driven_value=drivenKey['driven_value'],
            driver_ctrl_attr=drivenKey.get(['driver_ctrl_attr'], ''),
            **opt)
        print('# setDrivenKeys : {0} >> {1}'.format(driver, driven))

    return name


def is_behavior(source, target):
    src_matrix = cmds.xform(source, q=True, worldSpace=True, matrix=True)
    trg_matrix = cmds.xform(target, q=True, worldSpace=True, matrix=True)
    
    src_matrix = om.MTransformationMatrix(om.MMatrix(src_matrix))
    trg_matrix = om.MTransformationMatrix(om.MMatrix(trg_matrix))

    src_quat = src_matrix.rotation(1)
    trg_quat = trg_matrix.rotation(1)

    x = src_quat.x * trg_quat.x
    y = src_quat.y * trg_quat.y
    z = src_quat.z * trg_quat.Z

    res = 0
    for v in [x, y, z]:
        if 0 > v:
            res += 1
    return True if res == 2 else False


def is_scale_attr(attr):
    return True if attr in ['sx', 'sy', 'sz'] else False


def add_objectSet(nodes, objextSet='rig_deformers_grp'):
    if not cmds.objExists(objectSet):
        objectSet = cmds.sets(name=objectSet)
    cmds.sets(nodes, e=True, add=objectSet)


def add_blended_joint(joint_org='', **kwargs):
    joint = utils.flags('name', 'n',  joint_org + '_blendJnt', kwargs)
    component_scape = utils.flags('component_scale', 'cs', True, kwargs)
    blend = utils.flags('blend', 'bld', 0.5, kwargs)

    if not cmds.objExists(joint_org):
        return None
    
    if not cmds.objExists(joint):
        cmds.createNode('joint', name=joint, parent=joint_org)

    cmds.setAttr(joint + '.radius', 1.5)

    parent = get_parent(joint_org)
    if parent:
        cmds.parent(joint, parent, relative=True)
        joint_orient = cmds.getAttr(joint_org + '.jointOrient')
        cmds.setAttr(joint + '.jointOrient', *joint_orient[0])

    pair_blend = cmds.createNode('pairBlend')
    cmds.setAttr(pair_blend + '.rotInterpolation', 1)
    cmds.setAttr(pair_blend + '.weight', blend)

    cmds.connectAttr(joint_org + '.translate', pair_blend + '.inTranslate1')
    cmds.connectAttr(joint_org + '.translate', pair_blend + '.inTranslate2')
    cmds.connectAttr(joint_org + '.rotate', pair_blend + '.inRotate2')

    cmds.connectAttr(pair_blend + '.outTranslateX', joint + '.translateX')
    cmds.connectAttr(pair_blend + '.outTranslateY', joint + '.translateY')
    cmds.connectAttr(pair_blend + '.outTranslateZ', joint + '.translateZ')

    cmds.connectAttr(pair_blend + '.outRotateX', joint + '.rotateX')
    cmds.connectAttr(pair_blend + '.outRotateY', joint + '.rotateY')
    cmds.connectAttr(pair_blend + '.outRotateZ', joint + '.rotateZ')

    cmds.connectAttr(joint_org + '.scale', joint + '.scale')

    cmds.setAttr(joint + '.overrideEnabled', 1)
    cmds.setAttr(joint + '.overrideColor', 17)

    cmds.setAttr(joint + '.segmentScaleCompensate', component_scape)

    if not cmds.objExists(joint + '.weight'):
        cmds.addAttr(joint, longname='weight', attributeType='double', min=0, max=1, dv=0, keyable=True)
    cmds.setAttr(joint + '.weight', blend)

    if not cmds.isConnected(joint + '.weight', joint_org + '.weight'):
        cmds.connectAttr(joint + '.weight', joint_org + '.weight')
    
    return joint


def get_parent(node):
    parent = cmds.listRelatives(node, parent=True)
    return parent if parent else []
    

def add_npo(objs=None):
    npos = []

    if not objs:
        objs = cmds.ls(selection=True)
    if not isinstance(objs, list):
        objs = [objs]
    for obj in objs:
        parent = get_parent(obj)
        transform = cmds.createNode('transform', name=obj + '_npo', parent=parent, ss=True)
        matrix = cmds.xform(obj, q=True, worldSpace=True, matrix=True)
        cmds.parent(obj, tranform)
        nops.append(transform)
    
    return npos

