'''
constants.py
Shaper Rigs / Burlington Interactive Solutions
Matt Riche 2021

Python constants idiom.  These are the node names common to Shaper Rigs biped products.

'''


# SSC default bone names
INTERNAL_DEF_FK_JNTS = (
    { 'shoulder':'armUprFK_drv', 
    'elbow':'armLwrFK_drv', 
    'wrist':'armWristFK_drv' 
    }
    )

INTERNAL_DEF_IK_JNTS = (
    {'shoulder':'armUprIK_drv', 
    'elbow':'armLwrIK_drv', 
    'wrist':'armWristIK_drv' }
    )

# SSC default controls names
INTERNAL_DEF_FK_CTRLS = (
    { 'shoulder':'armUprFK_Ctrl', 
        'elbow':'armLwrFK_Ctrl', 
        'wrist':'armWristFK_Ctrl' }
        )

INTERNAL_DEF_IK_CTRLS = (
    { 'shoulder':'armUprIK_Ctrl', 
        'elbow':'ArmPV_Ctrl', 
        'wrist':'armWristIK_Ctrl', 
        'pv_offset':'ArmPV_nOffset' }
        )

INTERNAL_SIDE_TOKENS = { 'left':'L_', 'right':'R_' }
