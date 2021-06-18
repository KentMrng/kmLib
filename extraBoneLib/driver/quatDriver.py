from maya import cmds

from extraBoneLib import utils


def create(*args, **kwargs):
    utils.load_plugins('quatNodes')

    target = args[0]

    rv = kwargs.get('rv', (1, 0, 0))
    yv = kwargs.get('yv', (0, 1, 0))
    yaw = kwargs.get('yaw_axis', 'Y')
    pitch = kwargs.get('pitch_axis', 'Z')
    roll = kwargs.get('roll_axis', 'X')

    add_attr_if_not_exists(target, 'yaw', 'doubleAngle')
    add_attr_if_not_exists(target, 'pitch', 'doubleAngle')
    add_attr_if_not_exists(target, 'roll', 'doubleAngle')

    rtm = cmds.createNode('composeMatrix', name=target + '_rotToMatrix', ss=1)
    mtq = cmds.createNode('decomposeMatrix', name=target + '_matrixToQuat', ss=1)
    qtr = cmds.createNode('quatToEuler', name=target + '_quatToRoll', ss=1)
    qri = cmds.createNode('quatInvert', name=target + '_quatInv', ss=1)
    qap = cmds.createNode('quatProd', name=target + '_quatAngleProd', ss=1)
    qtb = cmds.createNode('quatToEuler', name=target + '_quatToBend', ss=1)

    if roll == 'X':
        cmds.setAttr(qtr + '.inputRotateOrder', 1)  # yzx, zyx
        cmds.setAttr(qtb + '.inputRotateOrder', 2)  # zxy, yxz
    elif roll == 'Y':
        cmds.setAttr(qtr + '.inputRotateOrder', 3)  # xzy, zxy
        cmds.setAttr(qtb + '.inputRotateOrder', 0)  # xyz, zyx
    elif roll == 'Z':
        cmds.setAttr(qtr + '.inputRotateOrder', 0)  # xyz, yxz
        cmds.setAttr(qtb + '.inputRotateOrder', 1)  # yzx, zyx

    cmds.connectAttr(target + '.rotate', rtm + '.inputRotate')
    cmds.connectAttr(rtm + '.outputMatrix', mtq + '.inputMatrix')

    cmds.connectAttr(mtq + '.outputQuat' + roll, qtr + '.inputQuat' + roll)
    cmds.connectAttr(mtq + '.outputQuat' + roll, qri + '.inputQuat' + roll)

    cmds.connectAttr(mtq + '.outputQuatW', qtr + '.inputQuatW')
    cmds.connectAttr(mtq + '.outputQuatW', qri + '.inputQuatW')

    cmds.connectAttr(qri + '.outputQuat', qap + '.input1Quat')
    cmds.connectAttr(mtq + '.outputQuat', qap + '.input2Quat')
    cmds.connectAttr(qap + '.outputQuat', qtb + '.inputQuat')

    cmds.connectAttr(qtb + '.outputRotate' + yaw, target + '.yaw')
    cmds.connectAttr(qtb + '.outputRotate' + pitch, target + '.pitch')
    cmds.connectAttr(qtr + '.outputRotate' + roll, target + '.roll')

    return target


def add_attr_if_not_exists(node, attr, attributeType):
    if not cmds.objExists('{0}.{1}'.format(node, attr)):
        cmds.addAttr(node, longname=attr, attributeType=attributeType, keyable=True)
