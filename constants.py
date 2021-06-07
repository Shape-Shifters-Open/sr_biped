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
    'elbow':'ArmPV_Ctrl', 
    'wrist':'armWristIK_Ctrl', 
    'pv_offset_elbow':'ArmPV_nOffset',
    'hip':'legUprIK_Ctrl',
    'knee':'LegPV_Ctrl',
    'ankle':'legAnkleIK_Ctrl'
    }
    )

INTERNAL_SIDE_TOKENS = { 'left':'L_', 'right':'R_' }
