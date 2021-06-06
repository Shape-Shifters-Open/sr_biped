# fkik.py
# Matt Riche 2021
# sr_biped for kinematic solver related operations.

import coord_math as m
import pymel.core as pm
import numpy as np
import constants as cons
import copy


def fk_to_ik(side=None, ik_bones_dict=None, 
    fk_ctrls_dict=None):
    '''
    Match fk controls to ik, but executing match xforms of the controllers to the bones.  Generic
    and ready to receive rig info for any rig with a 'copied arm' set up for fk/ik.  Assuming that
    the rig is well build and controller xforms match these bone xforms, result will be accurate.
    
    ik_bones_dict - dictionary containing keys 'shoulder' and 'elbow', etc, listing the ik bones.
    fk_ctrls_dict - dictionary containing keys 'shoulder' and 'elbow' etc, listing fk controls.
    '''

    # Assign defaults like so to dodge the mutable default argument issue:
    if(ik_bones_dict == None):
        ik_bones_dict = cons.INTERNAL_DEF_IK_JNTS.copy()
    if(fk_ctrls_dict == None):
        fk_ctrls_dict = cons.INTERNAL_DEF_FK_CTRLS.copy()

    if(side == None):      
        pm.error("Specify a side flag (Example fk_to_ik(side='l') )")
        return

    if(side.upper() in ['L', 'LEFT', 'L_', 'LFT', 'LT']):
        side_token = cons.INTERNAL_SIDE_TOKENS['left']
    elif(side.upper() in ['R', 'RIGHT', 'R_', 'RGT', 'RT']):
        side_token = cons.INTERNAL_SIDE_TOKENS['right']
    else:
        pm.error("Given side-flag string was weird.  Try 'r' or 'l'.")
        return


    # Append the side token to all strings.
    for bone in ik_bones_dict:
        ik_bones_dict[bone] = (side_token + ik_bones_dict[bone])
    print ("Side tokens added, joint references are:\n {}".format(ik_bones_dict))

    for ctrl in fk_ctrls_dict:
        fk_ctrls_dict[ctrl] = (side_token + fk_ctrls_dict[ctrl])
    print ("Side tokens added, ctrl targets are:\n {}".format(ik_bones_dict))

    # Iterate through the list of key names, perform the xform matching.
    targets_list = ['shoulder', 'elbow', 'wrist']
    for target_key in targets_list:
        print("Matching transforms of {} to {}...".format(
            fk_ctrls_dict[target_key], ik_bones_dict[target_key]
            ))
        # PyNode these up:
        target_node = pm.PyNode(fk_ctrls_dict[target_key])
        copy_node = pm.PyNode(ik_bones_dict[target_key])
        pm.matchTransform(target_node, copy_node, pos=True, piv=True)

    print ("Done.")

    return

    
def ik_to_fk(side=None, fk_bones_dict=None, ik_ctrls_dict=None):
    '''
    Move IK controls to match FK position.
    Ready to receive rig info for any rig with a 'copied arm' set up for fk/ik.  Assuming that the 
    rig is well build and controller xforms match these bone xforms, result will be accurate.
    
    usage:
    ik_to_fk(side=string, fk_bones_dict=dict, ik_controls_dict=dict)

    side - A string token to be appended to the front of the bone name.
    fk_bones_dict - dictionary containing keys 'shoulder' and 'elbow', etc, listing the fk bones.
    ik_ctrls_dict - dictionary containing keys 'shoulder' and 'elbow' etc, listing ik controls.
    '''

    # Interally apply the constant due to the "mutable default args problem".
    if(fk_bones_dict == None):
        fk_bones_dict = cons.INTERNAL_DEF_FK_JNTS.copy()
    if(ik_ctrls_dict == None):
        ik_ctrls_dict = cons.INTERNAL_DEF_IK_CTRLS.copy()

    # Append the side flags
    if(side == None):      
        pm.error("Specify a side flag (Example fk_to_ik(side='l') )")
        return

    if(side.upper() in ['L', 'LEFT', 'L_', 'LFT', 'LT']):
        side_token = cons.INTERNAL_SIDE_TOKENS['left']
    elif(side.upper() in ['R', 'RIGHT', 'R_', 'RGT', 'RT']):
        side_token = cons.INTERNAL_SIDE_TOKENS['right']
    else:
        pm.error("Given side-flag string was weird.  Try 'r' or 'l'.")
        return

    print("request side token isn {}".format(side_token))


    # Append the side token to all strings.
    for bone in fk_bones_dict:
        fk_bones_dict[bone] = (side_token + fk_bones_dict[bone])
    print ("Side tokens added, joint references are:\n {}".format(fk_bones_dict))
    for ctrl in ik_ctrls_dict:
        ik_ctrls_dict[ctrl] = (side_token + ik_ctrls_dict[ctrl])
    print ("Side tokens added, ctrl targets are:\n {}".format(ik_ctrls_dict))



    # Step one, match ik shoulder 1:1
    shoulder_target = pm.PyNode(fk_bones_dict['shoulder'])
    shoulder_ctrl = pm.PyNode(ik_ctrls_dict['shoulder'])
    pm.matchTransform(shoulder_ctrl, shoulder_target, pos=True, piv=True)

    # Step two, match ik wrist 1:1
    wrist_target = pm.PyNode(fk_bones_dict['wrist'])
    wrist_ctrl = pm.PyNode(ik_ctrls_dict['wrist'])
    pm.matchTransform(wrist_ctrl, wrist_target, pos=True, rot=True, piv=True)

    # Step three, match the PV control 1:1 to the elbow
    elbow_target = pm.PyNode(fk_bones_dict['elbow'])
    elbow_ctrl = pm.PyNode(ik_ctrls_dict['elbow'])
    pm.matchTransform(elbow_ctrl, elbow_target, pos=True) # Ignore the piv flag, maybe locked.

    # Step three-- extend the vectors where one is a ray from the hip to the knee, and the other is
    # the ankle to the knee.  This establishes the plane whereon the PV can live.
    vector_a = m.get_vector(
        point_a=pm.xform(shoulder_target, q=True, t=True, ws=True),
        point_b=pm.xform(elbow_target, q=True, t=True, ws=True)
        )
    vector_b = m.get_vector(
        point_a=pm.xform(wrist_target, q=True, t=True, ws=True),
        point_b=pm.xform(elbow_target, q=True, t=True, ws=True)
        )

    # Combined directions of the two vectors should be "out" from the middle joint.
    out_vector = vector_a + vector_b
    # Reduce the out vector
    out_vector = (out_vector * .75)
    print (out_vector)

    # Current placement into a numpy vector
    current_pos = np.array(pm.xform(elbow_ctrl, q=True, t=True, ws=True))
    final_pos = current_pos - out_vector
    
    # Move the middle control "outward" along the out_vector.
    pm.xform(elbow_ctrl, t=(final_pos[0], final_pos[1], final_pos[2]), ws=True)

    print("Done.")
