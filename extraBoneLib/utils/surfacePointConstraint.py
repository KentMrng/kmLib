import maya.api.OpenMaya as om
from maya import cmds

from extraBoneLib import utils


def create(target, surface):
    utils.load_plugins('matrixNodes')

    position = cmds.xform(target, q=True, worldSpace=True, translate=True)
    closest_point, parameter_u, parameter_v = get_closest_point(position)

    posi = cmds.createNode('pointOnSurfaceInfo', name=target + '_posi')
    fbyf = cmds.createNode('fourByFourMatrix', name=target + '_fbfm')
    mltm = cmds.createNode('multMatrix', name=target + 'mltm')
    decm = cmds.createNode('decomposeMatrix', name=target + '_decm')

    cmds.connectAttr(surface + '.worldSpace[0]', posi + '.inputSurface')
    cmds.connectAttr(fbyf + '.output', mltm + '.matrixIn[0]')
    cmds.connectAttr(target + '.parentInverseMatrix[0]', mltm + '.matrixIn[1]')
    cmds.connectAttr(mltm + '.matrixSum', decm + '.inputMatrix')

    out_attrs = [
        ['.normalizedTangentUX', '.normalizedTangentUY', '.normalizedTangentUZ'],
        ['.normalizedNormalX', '.normalizedNormalY', '.normalizedNormalZ'],
        ['.normalizedTangentVX', '.normalizedTangentVY', '.normalizedTangentVZ'],
        ['.positionX', '.positionY', '.positionZ']
    ]

    in_attrs = [
        ['.in00', '.in01', '.in02'],
        ['.in10', '.in11', '.in12'],
        ['.in20', '.in21', '.in22'],
        ['.in30', '.in31', '.in32'],
    ]

    for out_attr, in_attr in zip(out_attrs, in_attrs):
        cmds.connectAttr(posi + out_attr, fbyf + in_attr)

    cmds.connectAttr(decm + '.outputTranslate', target + '.translate')
    cmds.connectAttr(decm + '.outputRotate', target + '.rotate')

    if not cmds.objExists(target + '.parameterU'):
        cmds.addAttr(target, longname='parameterU', attributeType='double', keyable=True)    
    if not cmds.objExists(target + '.parameterV'):
        cmds.addAttr(target, longname='parameterV', attributeType='double', keyable=True)
    
    cmds.setAttr(target + '.parameterU', parameter_u)
    cmds.setAttr(target + '.parameterV', parameter_v)

    cmds.connectAttr(target + '.parameterU', posi + 'parameterU')
    cmds.connectAttr(target + '.parameterV', posi + 'parameterV')


def get_closest_point(surface, position):
    if not is_default_transform(surface):
        dup_surface = cmds.duplicate(furface)
        cmds.parent(dup_surface, world=True)
        cmds.makeIdentity(dup_surface[0],
                          apply=True, 
                          translate=True, 
                          rotate=True, 
                          scale=True, 
                          normal=False, 
                          preserveNormal=True)
        surface = dup_surface[0]

    slist = om.MSelectionList()
    slist.add(surface)
    dagPath = slist.getDagPath(0)
    surfaceFn = om.MFnNurbsSurface(dagPath)
    point = om.MPoint(position)
    closest_point, parameter_u, parameter_v = surfaceFn.closestPoint(point)

    return closest_point, parameter_u, parameter_v


def is_default_transform(node):
    translate = cmds.xform(node, q=True, worldSpace=True, translate=True)
    rotate = cmds.xform(node, q=True, worldSpace=True, rotate=True)
    scale = cmds.xform(node, q=True, worldSpace=True, scale=True)
    if translate != (0.0, 0.0, 0.0):
        return False
    if rotate != (0.0, 0.0, 0.0):
        return False
    if scale != (1.0, 1.0, 1.0):
        return False
    return True
    
    