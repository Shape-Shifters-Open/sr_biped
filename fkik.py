'''
fkik.py
Shaper Rigs / Burlington Interactive Solutions
Matt Riche 2021

FK / IK match tools.  By default will serve Shaper Rigs biped products.  When given different dicts
can be customized to work on (most) any rig with the pole-vector aligned to the plane defined by 
upper arm and lower-arm.

For format requirements of the dict, see constants.py
'''

from attributes import multi_as_enum
import pymel.core as pm
import pymel.core.datatypes as dt
import constants as cons
import maya.cmds as cmds
import suite as su

def fk_to_ik(side=None, limb=None, ik_bones_dict=None, fk_ctrls_dict=None, key=True, namespace=""):
    '''
    Match fk controls to ik, but executing match xforms of the controllers to the bones.  Generic
    and ready to receive rig info for any rig with a 'copied arm' set up for fk/ik.  Assuming that
    the rig is well build and controller xforms match these bone xforms, result will be accurate.
    
    ik_bones_dict - dictionary containing keys 'shoulder' and 'elbow', etc, listing the ik bones.
    fk_ctrls_dict - dictionary containing keys 'shoulder' and 'elbow' etc, listing fk controls.
    '''

    # Prep the namespace
    if(namespace != ""):
        namespace = (namespace + ":")

    # Based on the limb string incoming, the following keys will be used in the dictionary.
    if(limb == 'leg'):
        targets_list = ['hip', 'knee', 'ankle']
    elif(limb == 'arm'):
        targets_list = ['shoulder', 'elbow', 'wrist']
    else:
        pm.warning("Must specific a limb with either 'leg' or 'arm'.")
        return

    # Assign defaults like so to dodge the mutable default argument issue:
    if(ik_bones_dict == None):
        local_ik_bones_dict = cons.INTERNAL_DEF_IK_JNTS.copy()
    else:
        local_ik_bones_dict = ik_bones_dict.copy()
    
    if(fk_ctrls_dict == None):
        local_fk_ctrls_dict = cons.INTERNAL_DEF_FK_CTRLS.copy()
    else:
        local_fk_ctrls_dict = fk_ctrls_dict.copy()

    if(side != None):
        if(side.upper() in ['L', 'LEFT', 'L_', 'LFT', 'LT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['left']
        elif(side.upper() in ['R', 'RIGHT', 'R_', 'RGT', 'RT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['right']
        elif(side.upper() in ['C', 'CENTRE', 'CENTER', 'C_', 'CNT', 'CT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['centre']
    else:
        print("No side token given, assuming this is a centre-positioned or asymmetrical limb.")
        side_token = ''

    print ("working with namespace {}".format(namespace))
    # Append the side token to all strings.
    for bone in local_ik_bones_dict:
        local_ik_bones_dict[bone] = (namespace + side_token + local_ik_bones_dict[bone])
    print ("Side tokens added, joint references are:\n {}".format(local_ik_bones_dict))

    for ctrl in local_fk_ctrls_dict:
        local_fk_ctrls_dict[ctrl] = (namespace + side_token + local_fk_ctrls_dict[ctrl])
    print ("Side tokens added, ctrl targets are:\n {}".format(local_ik_bones_dict))

    # Iterate through the list of key names, perform the xform matching.
    for target_key in targets_list:
        print("Matching transforms of {} to {}...".format(
            (namespace + side_token + local_fk_ctrls_dict[target_key]), 
            local_ik_bones_dict[target_key]
            ))
        # PyNode these up:
        target_node = pm.PyNode(local_fk_ctrls_dict[target_key])
        copy_node = pm.PyNode(local_ik_bones_dict[target_key])
        pm.matchTransform(target_node, copy_node, rot=True, pos=True, piv=True)

    # Put keyframes on all the FK controls if key is true.
    if(key==True):
        for target_key in targets_list:
            pm.setKeyframe(local_fk_ctrls_dict[target_key], at=['translate', 'rotate'])
            print ("Keying {}".format(local_fk_ctrls_dict[ctrl]))

    print ("Done.")

    return

    
def ik_to_fk(side=None, limb=None, fk_bones_dict=None, ik_ctrls_dict=None, key=True, 
    foot_rot_comp=None, amp_pv=40.0, stump=False, namespace=""):
    '''
    Move IK controls to match FK position.
    Ready to receive rig info for any rig with a 'copied arm' set up for fk/ik.  Assuming that the 
    rig is well build and controller xforms match these bone xforms, result will be accurate.
    
    usage:
    ik_to_fk(side=string, fk_bones_dict=dict, ik_controls_dict=dict)

    side - A string token to be appended to the front of the bone name.
    fk_bones_dict - dictionary containing keys 'shoulder' and 'elbow', etc, listing the fk bones.
    ik_ctrls_dict - dictionary containing keys 'shoulder' and 'elbow' etc, listing ik controls.
    key - True if you want keyframes applied to the controls in question
    foot_rot_comp - Vector to compensate for the difference between FK orientation and IK handle 
        being oriented to world space.  Shaper Rigs' node constant have something inside to account
        for this, hence the default to (0, 0, 0)
    amp_pv - How much to amplify the vector projecting the pole vector.
    namespace - Passes a string of the anticipated namespace so that the handle/joint constants can 
        have it added as a prefix
    '''

    # Prep the namespace
    if(namespace != ""):
        namespace = (namespace + ":")

    # Interally apply the constant due to the "mutable default args problem".
    if(fk_bones_dict == None):
        local_fk_bones_dict = cons.INTERNAL_DEF_FK_JNTS.copy()
    else:
        local_fk_bones_dict = fk_bones_dict.copy()

    if(ik_ctrls_dict == None):
        local_ik_ctrls_dict = cons.INTERNAL_DEF_IK_CTRLS.copy()
    else:
        local_ik_ctrls_dict = ik_ctrls_dict.copy()

    if(foot_rot_comp == None):
        foot_rot_comp = (0, 0, 90)

    # Based on the limb string incoming, the following keys will be used in the dictionary.
    if(limb == 'leg'):
        targets_list = ['hip', 'ankle', 'knee', 'knee_pv']
        clean_list = ['toe', 'ball', 'heel']
        amp_pv *= 1.2 # Little extra distance for legs.
    elif(limb == 'arm'):
        clean_list = []
        targets_list = ['shoulder', 'wrist', 'elbow', 'elbow_pv']
    else:
        pm.warning("Must specific a limb with either 'leg' or 'arm'.")
        return

    # Append the side flags

    if(side != None):
        if(side.upper() in ['L', 'LEFT', 'L_', 'LFT', 'LT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['left']
        elif(side.upper() in ['R', 'RIGHT', 'R_', 'RGT', 'RT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['right']
        elif(side.upper() in ['C', 'CENTRE', 'CENTER', 'C_', 'CNT', 'CT']):
            side_token = cons.INTERNAL_SIDE_TOKENS['centre']
    else:
        print("No side token given, assuming this is a centre-positioned or asymmetrical limb.")
        side_token = ''

    # Special check for difficult space check:
    if(limb=='arm'):
        if(pm.objExists(namespace + side_token + local_ik_ctrls_dict['wrist'])):

            wrist_node = pm.PyNode(namespace + side_token + local_ik_ctrls_dict['elbow_pv'])
            print(dir(wrist_node))
            if(wrist_node.IK_Hand_Crl_space.get() == True):

                result = pm.confirmDialog(
                                title='SR_Biped',
                                message=("When Pole Vector\'s Space is set to IK_Hand_Crl_space, "
                                "calculated result is not-exact."),
                                button=['Match Anyway', 'Cancel'],
                                defaultButton='OK',
                                cancelButton='Cancel',
                                dismissString='Cancel')

                if result == 'Match Anyway':
                    pass
                else:
                    pm.warning('User stopped the operation.')
                    return
    elif(limb=='leg'):
        toe_exists = True
        if(pm.objExists(namespace + side_token + local_ik_ctrls_dict['ankle'])):

            wrist_node = pm.PyNode(namespace + side_token + local_ik_ctrls_dict['knee_pv'])
            print(dir(wrist_node))

            # If the wrist node (in this case an ankle) has IK_Foot_Crl_space, then we warn about 
            # match accuracy:
            if(pm.hasAttr(wrist_node, 'IK_Foot_Crl')):
                if(wrist_node.IK_Foot_Crl_space.get() == True):

                    result = pm.confirmDialog(
                                    title='SR_Biped',
                                    message=("When Pole Vector\'s Space is set to IK_Foot_Crl_space, "
                                    "calculated result is not-exact."),
                                    button=['Match Anyway', 'Cancel'],
                                    defaultButton='Match Anyway',
                                    cancelButton='Cancel',
                                    dismissString='Cancel')

                    if result == 'Match Anyway':
                        pass
                    else:
                        pm.warning('User stopped the operation.')
                        return
            else:
                print("This doesn't appear to be a normal human foot.  Skipping toe alignment.")


    # If we are dealing with a 'stump' we end calculation at the wrist joint or the ankle joint, no
    # heel, toes, ball, etc.  We do this by getting rid of them from the dict so they won't be
    # iterated over.
    if(stump):
        for key in ['ball', 'toe', 'heel']:
            print("Ignoring {}".format(key))
            local_ik_ctrls_dict.pop(key)

    # Append the side token to all strings.
    for bone in local_fk_bones_dict:
        local_fk_bones_dict[bone] = (namespace + side_token + local_fk_bones_dict[bone])
    print ("Side tokens added, joint references are:\n {}".format(local_fk_bones_dict))
    for ctrl in local_ik_ctrls_dict:
        local_ik_ctrls_dict[ctrl] = (namespace + side_token + local_ik_ctrls_dict[ctrl])
    print ("Side tokens added, ctrl targets are:\n {}".format(local_ik_ctrls_dict))

    # Get our nodes prepped.
    topmost_target = pm.PyNode(local_fk_bones_dict[targets_list[0]])
    endmost_target = pm.PyNode(local_fk_bones_dict[targets_list[1]])
    middle_target = pm.PyNode(local_fk_bones_dict[targets_list[2]])

    topmost_ctrl = pm.PyNode(local_ik_ctrls_dict[targets_list[0]])
    middle_ctrl = pm.PyNode(local_ik_ctrls_dict[targets_list[2]])
    pole_vector = pm.PyNode(local_ik_ctrls_dict[targets_list[3]])
    endmost_ctrl = pm.PyNode(local_ik_ctrls_dict[targets_list[1]])

    # Step one, match ik shoulder 1:1
    pm.matchTransform(topmost_ctrl, topmost_target, pos=True, piv=True)

    # Based on the calc style chosen, calculate where the PV should go based on the position of the
    # given FK bones.

    # TODO: If our keying is going to happen, we should do shoulder and wrist here, Euler filter it
    # then do the PV last.
    
    # Get the positions of these objects as dt.Vectors.
    top_pos = dt.Vector(pm.xform(topmost_target, query=True, worldSpace=True, translation=True))
    mid_pos = dt.Vector(pm.xform(middle_target, query=True, worldSpace=True, translation=True))
    end_pos = dt.Vector(pm.xform(endmost_target, query=True, worldSpace=True, translation=True))

    # Derive PV position using two vectors crossing, added together.
    # Get directional vectors shooting from shoulder and wrist back at elbow.
    line_a = end_pos - mid_pos
    line_b = top_pos - mid_pos

    # Normalize these values:
    line_a.normalize()
    line_b.normalize()

    # Apply amplification value:
    line_a *= amp_pv
    line_b *= amp_pv

    # A good positional vector for the pv is calculated.
    pv_pos = (mid_pos - (line_a + line_b))

    # To stop these vectors from ever aiming inside by mistake, we can aim towards the middle_ctrl
    # and add some of that amplitude to make sure it moves out.
    #line_c = mid_pos - dt.Vector(pm.xform(middle_ctrl, q=True, worldSpace=True, translation=True))
    #line_c.normalize()
    #print(line_c)  '

    #pv_pos = (pv_pos + (line_c * amp_pv))
    pm.xform(pole_vector, t=(pv_pos), ws=True)

    # Last step: Put the rotation on the wrist.
    # If not a leg, regular matchTransform is safe, as rig is likely build 1:1 with the parts.
    if(limb == 'leg'):
        pm.matchTransform(endmost_ctrl, endmost_target, pos=True, rot=True)

        # Clean transforms off of toe, ball and heel, since the bones represent the match, and these
        # handles will dirty the result.  If this is a stump, we don't bother with either.

        if(stump == False):
            print('Cleaning foot IK...')
            print("clean list is {}.".format(clean_list))
            print("Ik_ctrls dict is {}".format(local_ik_ctrls_dict))
            for handle in clean_list:
                print ("Getting node {}".format(local_ik_ctrls_dict[handle]))
                clean_node = pm.PyNode(local_ik_ctrls_dict[handle])
                clean_node.translate.set(0,0,0)
                clean_node.rotate.set(0,0,0)
            

        else:
            print("This is a stump with no heel, ball or toe.")
            pm.matchTransform(endmost_ctrl, endmost_target, pos=True, rot=True)

        # Perform relative transform from new position against the joint-orient of the target, since
        # the IK foot control is likely in world-space.
        print ("Counter-rotating feet...")
        if(side_token == cons.INTERNAL_SIDE_TOKENS['left']):
            pm.xform(endmost_ctrl, r=True, os=True, ro=foot_rot_comp)
        elif(side_token == cons.INTERNAL_SIDE_TOKENS['right']):
            pass
            pm.xform(
                endmost_ctrl, r=True, os=True, 
                ro=(foot_rot_comp[0]-180, foot_rot_comp[1], foot_rot_comp[2] % 360)
                )
        else:
            pm.xform(endmost_ctrl, r=True, os=True, ro=foot_rot_comp)

    else:
        pm.matchTransform(endmost_ctrl, endmost_target, pos=True, rot=True)

    # Last step is to get the orientation of the elbow control
    pm.matchTransform(middle_ctrl, middle_target, rot=True)

    # Put keyframes on all the IK controls if key is true.
    if(key==True):
        # TODO: special case wrist/ankle keying order.
        #        for target_key in targets_list:
            pm.setKeyframe(local_ik_ctrls_dict['elbow_pv'], at=['translate'])
            pm.setKeyframe(local_ik_ctrls_dict['wrist'], at=['translate', 'rotate'])
            #pm.filterCurve(local_ik_ctrls_dict[target_key].rotate.x, local_ik_ctrls_dict[target_key].rotate.y, local_ik_ctrls_dict[target_key].rotate.z)
            print ("Keying {}".format(local_ik_ctrls_dict[ctrl]))

    print("Done.")

    return


def bake_ik_to_fk(
    side=None, limb=None, fk_bones_dict=None, ik_ctrls_dict=None, namespace="", stump=False
    ):
    '''
    bake_ik_to_fk

    Matches the ik position to the fk animation, keying it over the selected frames.

    usage:
    bake_ik_to_fk
    '''

    # Interally apply the constant due to the "mutable default args problem".
    if(fk_bones_dict == None):
        fk_bones_dict = cons.INTERNAL_DEF_FK_JNTS.copy()
    if(ik_ctrls_dict == None):
        ik_ctrls_dict = cons.INTERNAL_DEF_IK_CTRLS.copy()

    import maya.mel

    frame_range = su.frame_selection()
    if(frame_range == False):
        pm.error("Nothing was specified in the frame slider selection.")
        return

    # Move the time slider to the beginning of the selected range.
    pm.currentTime(frame_range[0], edit=True)
    
    print("DEBUG: dict is {}".format(fk_bones_dict))

    # Iterate through the frame range selected.
    while(pm.currentTime(q=True) < frame_range[1]):

        # Bake the ik controllers to the position the fk controls are on this frame:
        ik_to_fk(
            side=side, limb=limb, key=True, fk_bones_dict=fk_bones_dict, 
            ik_ctrls_dict=ik_ctrls_dict, namespace=namespace, stump=stump)
        next_frame = (pm.currentTime(q=True) + 1)
        pm.currentTime(next_frame, edit=True)
        pm.refresh(cv=True)

    print ("Done.")


def bake_fk_to_ik(
    side=None, limb=None, ik_bones_dict=None, fk_ctrls_dict=None, namespace="", stump=False
    ):
    '''
    bake_fk_to_ik

    Matches the fk position to the ik animation, keying it over the selected frames.

    usage:
    bake_fk_to_ik(side=string(token), limb=string(token))
    Use with a frame range selected.
    '''

    # Assign defaults like so to dodge the mutable default argument issue:
    if(ik_bones_dict == None):
        ik_bones_dict = cons.INTERNAL_DEF_IK_JNTS.copy()
    if(fk_ctrls_dict == None):
        fk_ctrls_dict = cons.INTERNAL_DEF_FK_CTRLS.copy()

    frame_range = su.frame_selection()
    if(frame_range == False):
        pm.error("Nothing was specified in the frame slider selection.")
        return

    # Move the time slider to the beginning of the selected range.
    pm.currentTime(frame_range[0], edit=True)
    
    # Iterate through the frame range selected.
    while(pm.currentTime(q=True) < frame_range[1]):

        # Bake the fk controllers to the position the fk controls are on this frame:
        fk_to_ik(
            side=side, limb=limb, key=True, ik_bones_dict=ik_bones_dict, 
            fk_ctrls_dict=fk_ctrls_dict, namespace=namespace, stump=stump)
        next_frame = (pm.currentTime(q=True) + 1)
        pm.currentTime(next_frame, edit=True)
        pm.refresh(cv=True)

    print ("Done.")

    return



def safe_snap(subject_node, target_node, trans=True, rot=True):
    '''
    safe_snap

    Function to snap things with trickier parentage differences by reading their absolute trans and
    performing and absolute snap.  Slower than pm.matchTransform() but will brute-force against
    complicated parentage.

    usage:
    safe_snap(subject_node=PyNode, target_node=PyNode)
    '''

    print ("Performing a hard match of {} to {}.".format(subject_node, target_node))

	# Get details from the target_node.
    target_rot = pm.xform( target_node, q=True, ws=True, ro=True )
    target_trans = pm.xform( target_node, q=True, ws=True, t=True )

    # I've been warned about the ws flags behaving deceptively.
    if(trans==True):
        pm.xform( subject_node, ws=True, t=target_trans )
    if(rot==True):
        pm.xform( subject_node, ws=True, ro=target_rot )

    return