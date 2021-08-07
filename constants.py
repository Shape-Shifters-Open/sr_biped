'''
constants.py
Shaper Rigs / Burlington Interactive Solutions
Matt Riche 2021

Python constants idiom.  These are the node names common to Shaper Rigs biped products.
'''


# SSC default bone names
INTERNAL_DEF_FK_JNTS = (
    { 
        'shoulder':'armUprFK_drv', 
        'elbow':'armLwrFK_drv', 
        'wrist':'armWristFK_drv',
        'hip':'legUprFK_drv',
        'knee':'legLwrFK_drv',
        'ankle':'legAnkleFK_drv',
        }
    )

INTERNAL_DEF_IK_JNTS = (
    {
        'shoulder':'armUprIK_drv', 
        'elbow':'armLwrIK_drv', 
        'wrist':'armWristIK_drv',
        'hip':'legUprIK_drv',
        'knee':'legLwrIK_drv',
        'ankle':'legAnkleIK_drv'
        }
    )

# SSC default controls names
INTERNAL_DEF_FK_CTRLS = (
    { 
        'shoulder':'armUprFK_Ctrl', 
        'elbow':'armLwrFK_Ctrl', 
        'wrist':'armWristFK_Ctrl',
        'hip':'legUprFK_Ctrl',
        'knee':'legLwrFK_Ctrl',
        'ankle':'legAnkleFK_Ctrl'
        }
    )

INTERNAL_DEF_IK_CTRLS = (
    { 
        'shoulder':'armUprIK_Ctrl',
        'elbow':'ArmElbow_Ctrl', 
        'elbow_pv':'ArmPV_Ctrl', 
        'wrist':'armWristIK_Ctrl', 
        'pv_offset_elbow':'ArmPV_nOffset',
        'hip':'legUprIK_Ctrl',
        'knee_pv':'LegPV_Ctrl',
        'knee':'LegKnee_Ctrl',
        'ankle':'legAnkleIK_Ctrl',
        'toe':'toe_Ctrl',
        'ball':'ball_Ctrl',
        'heel':'heel_Ctrl'
        }
    )

# Naming convention tokens
INTERNAL_SIDE_TOKENS = { 'left':'L_', 'right':'R_' }


# Attribute names of space-switch targets:
INTERNAL_SPACE_SWITCH_ATTRS = (
    {
        'wrist':[
            'neckHeadTip_Space', 
            'spineChestTip_Space', 
            'shoulder_Space', 
            'spineHip_Space',
            'cog_Space',
            'world_Space',
            ],
        'head':[
            'spineChestTip_Space',
            'cog_Space',
            'neckBase_Space',
            'world_space'
            ],
        'foot':[
            'spineHip_Space',
            'cog_Space'
            ],
        'knee':[
            'spineHip_Space',
            'cog_Space',
            'IK_Foot_Crl_space',
        ],
        'elbow':[
            'spineChestTip_Space',
            'shoulder_Space',
            'IK_Hand_Crl_space',
        ],
        'fk_shoulder':[
            'cog_Space',    
            'spineChestTip_Space',
            'shoulder_Space',
        ]
        }
    )


# HIK constants:
# HIK uses arbitrary indices like so for each body part.
HIK_CHARACTERIZE_MAP = {
    'neckHead':15,
    'spineHip':1,
    'L_armUpr':9,
    'L_legAnkle':4,
    'L_armLwr':10,
    'L_armWrist':11,
    'L_legUpr':3,
    'L_shoulder':18,
    'L_footMid':16,
    'L_legUpr':2,
    'neckBase':20,
    'R_armUpr':12,
    'R_legAnkle':7,
    'R_armLwr':13,
    'R_armWrist':14,
    'R_legUpr':6,
    'R_shoulder':19,
    'R_footMid':17,
    'R_legUpr':5,
    'spineChest':8,
    'spineChestTip':23
}


# "Data Driven" instructions for the characterize/constrain operation.
HIK_PREFIX = 'fbIk_'

# TODO some of the values are from the data acquired from out client.
HIK_JOINT_DATA = {
    'leg': {
        'hip': {
            'label': 'UpLeg',
            'fromControl': 'hip_fkControl',
            'parent': 'pelvis'
        },
        'knee': {
            'label': 'Leg',
            'fromControl': 'knee_fkControl',
            'parent': 'hip',
        },
        'ankle': {
            'label':'Foot',
            'fromControl': 'ankle_fkControl',
            'parent': 'knee',
        },
        'ball': {
            'label': 'ToeBase',
            'fromControl': 'ball_fkControl',
            'parent': 'ankle'
        }, 
    },

    'arm': {
        'clavicle': {
            'label': 'Shoulder',
            'fromControl': 'clavicle_control',
            'parent': 'torso'
        },
        'shoulder': {
            'label': 'Arm',
            'fromControl:': 'shoulder_fkControl',
            'parent': 'clavicle',
        },
        'elbow':{
            'label': 'ForeArm',
            'fromControl': 'elbow_fkControl',
            'parent': 'shoulder',
        },
        'wrist':{
            'label': 'Hand',
            'fromControl': 'wrist_fkControl',
            'parent': 'elbow',
        },
    },

    'spine':{
        'pelvis':{
            'label': 'Hips',
            'fromControl': 'pelvis_control',
            'parent': None,
        },
        'midriff': {
            'label': 'Spine',
            'fromControl': 'midriff_control',
            'parent': 'pelvis',
        },
        'torso':{
            'label': 'Spine1',
            'fromControl': 'torso_control',
            'parent': 'midriff',
        },
        'neck':{
            'label': 'Neck',
            'fromControl': 'neck_control',
            'parent': 'torso',
        },
        'head':{
            'label':'Head',
            'fromControl': 'head_control',
            'parent': 'neck'
        }
    }
}

# SHJnts in the rig to find for the duplication purpose:
TOP_JOINT='trajectory_SHJnt'