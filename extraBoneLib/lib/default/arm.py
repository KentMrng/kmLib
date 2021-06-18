from maya import cmds

from extraBoneLib import libParts
from extraBoneLib.utils import node


arm_driven_info = [
    {
        'driver': 'armRoot_{}0_jnt',
        'behavior': 'arm_L0_0_jnt',
        'drivenkeys': [
            {
                'driver_attr': 'yaw',
                'driven_attr': 'tz',
                'driver_value': [-45, 0, 45],
                'driven_value': [0.4, 0, -0.3],
            },
            {
                'driver_attr': 'yaw',
                'driven_attr': 'sz',
                'driver_value': [-65, -45],
                'driven_value': [1.38, 1],
            },
            {
                'driver_attr': 'pitch',
                'driven_attr': 'ty',
                'driver_value': [-90, 0],
                'driven_value': [-0.668, 0],
            },
            {
                'driver_attr': 'pitch',
                'driven_attr': 'sy',
                'driver_value': [-90, 0, 90],
                'driven_value': [1.238, 1, 1.238],
            }
        ]
    }
]

parts_info = {
    'base_joint': 'arm_{}0_0_jnt',
    'joint_radius': 1.4,
    'arm_driven_info': arm_driven_info
}


class Main(libParts.Main):

    def __init__(self):
        self.parts_info = parts_info

    def has_reference(self):
        self.log.info('=== partLib : [{0}] ==='.format(__name__))
        self.log.info('# parts_info values')
        self.pprint(self.parts_info)

        node = self.parts_info.get('base_joint')
        for side in 'LR':
            if not cmds.objExists(node.format(side)):
                self.log.warning('SKIP : not found "{0}".'.format(node.format(side)))
                return False
            else:
                self.log.info('has required node : {0}.'.format(node.format(side)))
        return True

    def execute(self):
        base_joint = self.parts_info.get['base_joint']
        arm_driven_info = self.parts_info['arm_driven_info']

        for side in 'LR':
            joint = base_joint.format(side)
            bend_joint = node.create_bend_joint(joint, name=joint.replace('jnt', 'bendJnt'))
            blend_joint = node.add_blended_joint(bend_joint, name=joint.replace('jnt', 'bendBldJnt'))
            joints = node.driven_joint_key(arm_driven_info, side, joint, blend_joint)
            node.add_objectSet(joints, objextSet='rig_deformers_grp')
            self.log.info('# create influences : ' + str(joints))
            self.set_radius(joints)
    
    def set_radius(self, nodes):
        value = self.parts_info.get('joint_radius')

        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            if cmds.objExists(node + '.radius'):
                cmds.setAttr(node + '.radius', value)