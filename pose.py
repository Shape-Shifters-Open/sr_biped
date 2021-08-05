'''
pose.py

Module for adopting particular poses for puporses of binding HIK, etc.
'''

import pymel.core as pm
import pymel.core.datatypes as dt


def controls_to_t_pose(z_up=False, arm_targets=None, leg_targets={}):
    '''
    Set the rig in-scene to t-pose
    '''
    # Need to check if there's a rig in the scene.

    # First straighten arms
    print("Straightening Arms...")
    straighten_arm(side='L_', z_up=z_up, arm_targets=arm_targets)
    straighten_arm(side='R_', z_up=z_up, arm_targets=arm_targets)

    # ... then legs...

    return


def limb_measure(first_joint, middle_joint, last_joint):
    '''
    Given the three joints of a limb, get distance vectors between them and add them up to find what
    the total length of the limb is.  Returns dt.Vector of the total length.
    
    first_joint : PyNode of the topmost joint
    middle_joint : PyNode of the middle joint (elbow or knee joint)
    last_joint : PyNode of the end joint 
    '''

    first_pos = dt.Vector(pm.xform(first_joint, q=True, t=True, ws=True))
    middle_pos = dt.Vector(pm.xform(middle_joint, q=True, t=True, ws=True))
    last_pos = dt.Vector(pm.xform(last_joint, q=True, t=True, ws=True))
    limb_length = ((first_pos - middle_pos) + (middle_pos - last_pos))

    return limb_length.length()


def straighten_arm(side=None, z_up=False, arm_targets=None):
    '''
    straighten_arm

    Generally called by 'controls_to_t_pose()' but it's accessible outside.
    '''
    if(arm_targets == None):
        arm_targets = { 
            'shoulder_ctrl':cns.INTERNAL_DEF_IK_CTRLS['shoulder'],
            'elbow_pv_ctrl':cns.INTERNAL_DEF_IK_CTRLS['elbow'],
            'wrist_ctrl':cns.INTERNAL_DEF_IK_CTRLS['wrist'],
            'shoulder_joint':cns.INTERNAL_DEF_FK_JNTS['shoulder'],
            'elbow_joint':cns.INTERNAL_DEF_FK_JNTS['elbow'],
            'wrist_joint':cns.INTERNAL_DEF_FK_JNTS['wrist']
        }


    if(side == None):
        pm.error("No arm given to 'straighten_arm()'.")
        return

    # PyNodify the joints:
    shoulder_joint = pm.PyNode(side + arm_targets['shoulder_joint'])
    elbow_joint = pm.PyNode(side + arm_targets['elbow_joint'])
    wrist_joint = pm.PyNode(side + arm_targets['wrist_joint'])

    # Getting total length of the arm:
    arm_length = limb_measure(shoulder_joint, elbow_joint, wrist_joint)
    # Flip this if right-side:
    if(side == 'R_'):
        arm_length = -arm_length


    # PyNodify the targets
    elbow_pv = pm.PyNode(side + arm_targets['elbow_pv_ctrl'])
    wrist_ctrl = pm.PyNode(side + arm_targets['wrist_ctrl'])
    shoulder_ctrl = pm.PyNode(side + arm_targets['shoulder_ctrl'])

    # Reset shoulder before the remaining calculations
    shoulder_ctrl.translate.set(0,0,0)
 
    # Move controls to align on appropriate axis.
    if(z_up):
        # Find the point in space where the wrist should go and move it there.
        shoulder_pos = dt.Vector(pm.xform(shoulder_joint, q=True, t=True, ws=True))
        wrist_pos = shoulder_pos + dt.Vector(0, arm_length, 0) # arm_length for Y in Z up.
        pm.xform(wrist_ctrl, t=wrist_pos, ws=True)

        # todo - align elbow pv.


    else:
        # Find the point in space where the wrist should go and move it there.
        shoulder_pos = dt.Vector(pm.xform(shoulder_joint, q=True, ws=True))
        wrist_pos = shoulder_pos + dt.Vector(arm_length, 0, 0) # arm_length for Y in Z up.
        pm.xform(wrist_ctrl, p=wrist_pos, ws=True, t=True)

    return


def straighten_leg(side=None, z_up=False, leg_targets=None):
    '''
    straighten_leg

    Generally called by 'controls_to_t_pose()' but it's accessible outside.
    '''
    
    if(side == None):
        pm.error("No arm given to 'straighten_arm()'.")
        return

    # PyNodify the joints:
    hip_joint = pm.PyNode(side + leg_targets['shoulder_joint'])
    knee_joint = pm.PyNode(side + leg_targets['elbow_joint'])
    ankle_joint = pm.PyNode(side + leg_targets['wrist_joint'])

    # Getting total length of the arm:
    arm_length = limb_measure(hip_joint, knee_joint, ankle_joint)

    # PyNodify the targets
    knee_pv = pm.PyNode(side + leg_targets['elbow_pv_ctrl'])
    ankle_ctrl = pm.PyNode(side + leg_targets['wrist_ctrl'])
    hip_ctrl = pm.PyNode(side + leg_targets['shoulder_ctrl'])

    # Reset shoulder before the remaining calculations
    hip_ctrl.translate.set(0,0,0)
    # Move wrist to the distance vector we identified earlier:
    ankle_ctrl.translate.set(hip_ctrl.translate.get() + arm_length)

    # Move controls to align on appropriate axis.
    if(z_up):
        # Aligned vertically (Z-up mode)
        knee_pv.translate.z.set(hip_ctrl.translate.z.get())
        ankle_ctrl.translate.z.set(hip_ctrl.translate.z.get())

    else:
        # Aligned vertically (Y-up mode)
        knee_pv.translate.y.set(hip_ctrl.translate.z.get())
        ankle_ctrl.translate.y.set(hip_ctrl.translate.z.get())

    return

