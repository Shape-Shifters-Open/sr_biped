'''
humanik.py

For automated interactions between HumanIK and our rigging standard.
'''

import pymel.core as pm
import pymel.core.datatypes as dt
import constants as cns
import namespaces as nm
import maya.mel as mel


def duplicate_skeleton(prefix='hik_', ns=''):
    '''
    Duplicates the entire skeleton of the in-scene rig with new prefixes. (Initially for the purpose
    of making HIK-characterizable skeletons.
    '''

    # Adjust namespace as a string.
    if(ns == ''):
        if(len(pm.ls(sl=True)) == 1):
            if(':' not in pm.ls(sl=True)[0]):
                pm.warning("You are working without a namespace right now...")
            else:
                ns = pm.ls(sl=True)[0].name().split(':')[0] + ':'
                print('name space is:{}'.format(ns))
        else:
            pm.error('A selection is required to isolate the rig we are running on.')
            return

    
    # Grab the top of the SHJnt chain and duplicate from there
    to_dupe = ([node for node in pm.listRelatives(ns + cns.TOP_JOINT, ad=True) 
        if(('RbnSrf' not in node.name()) and node.type() == 'joint')]) + [ns + cns.TOP_JOINT]
    dup_joints = pm.duplicate(to_dupe, ic=False, rc=True, un=False, rr=True, po=True)

    # Clean up the string names of the duplicated skeleton.
    for joint in dup_joints:
        old_name = joint.name()
        suffix = old_name.split('_')[-1]
        new_name = (cns.HIK_PREFIX + old_name.replace('_' + suffix, ""))
        joint.rename(new_name)

    # Bring the top of the newly duplicate hiearachy out of the group into world-parentage.
    # Search for the top first to do this:
    for joint in dup_joints:
        if(pm.listRelatives(joint, p=True)[0].type() == 'transform'):
            pm.parent(joint, w=True)

    return


def characterize_skeleton():
    '''
    HIK_characterize(namespace="")
    
    Builds a separate skeleton that can safely be characterized and used with HIK.
    
    usage:
    HIK_characterize(namespace={namespace as string})
    an sr_biped must be in scene.
    '''

    # Evaluate the following mel:
    # loadPlugin "MayaHIK";
    # ToggleCharacterControls;
    # hikCreateDefinition;
    # hikOnSwitchContextualTabs;
    mel.eval ('loadPlugin "mayaHIK";ToggleCharacterControls;hikCreateDefinition;'
        'hikOnSwitchContextualTabs;')

    for joint_name, fbIkIndex in cns.HIK_CHARACTERIZE_MAP.iteritems():
        print("joint name: {}\nfbIkIndex: {}\nCurrent Character:{}".format(
            joint_name, fbIkIndex, mel.eval('hikGetCurrentCharacter();')))
        mel.eval('setCharacterObject("{}","{}",{},0);'.format(
            cns.HIK_PREFIX + joint_name, mel.eval('hikGetCurrentCharacter();'), fbIkIndex))

    
def constrain_skeleton(ns=''):
    '''
    constrain the existing HIK skeleton (likely created from a duplication.)

    Constraint mapping is data driven, function runs in place.
    '''

    # First do a quick check to see if at least a trajectory joint exists with the prefix.
    hik_joints = [jnt for jnt in pm.ls(type='joint') if(cns.HIK_PREFIX in jnt.name())]

    if(len(hik_joints) < 1):
        pm.error("sr_biped error: Zero joints with the prefix {} exist in the scene. Skeleton "
        "probably was not characterized first.".format(cns.HIK_PREFIX))
        return

    constraints_list = []

    for body_part in cns.CONSTRAINT_MAPPING.items():
        mirror = False
        print("Setting up constraints on {}...".format(body_part[0]))
        if(body_part[0] in ['arm', 'leg']):
            print("{} is a mirrored bodypart.".format(body_part[0]))
            mirror = True
        else:
            print("{} is not a mirrored body part.".format(body_part[0]))
            mirror = False
        
        if(mirror):
            for side in ['L_', 'R_']:
                for ctrl in body_part[1].items():
                    constraints_list.append(constraint_by_mapping(ctrl, side=side, ns=ns))
        else:
            for ctrl in body_part[1].items():
                constraints_list.append(constraint_by_mapping(ctrl, side='C_', ns=ns))

    return constraints_list
                    

def constraint_by_mapping(map_dict, side='', ns=''):
    '''
    Takes a piece of the "mapping dict" found in constants.
    '''

    c_type = map_dict[1]['type']
    ctrl = (ns + side + map_dict[0])

    # Brief hack for Cogs, they don't have a prefix in our standard.
    if(ctrl == (ns + 'C_Cog_Ctrl')):
        ctrl = (ns + 'Cog_Ctrl')

    # A not great hack to deal with the fact that controls have a C_ but SHJnts do not.
    if(side == "C_"):
        side = ''
    target = (cns.HIK_PREFIX + side + map_dict[1]['target'])

    print('c_type is {} from {} to {}.  Building...'.format(c_type, ctrl, target))

    if(c_type == 'parent'):
        new_constraint = pm.parentConstraint(target, ctrl, mo=False)
    elif(c_type == 'parent_offset'):
        new_constraint = pm.parentConstraint(target, ctrl, mo=True)
    elif(c_type == 'orient'):
        new_constraint = pm.orientConstraint(target, ctrl, mo=True)
    elif(c_type == 'point'):
        new_constraint = pm.pointConstraint(target, ctrl)
    elif(c_type == 'point_offset'):
        new_constraint = pm.pointConstraint(target, ctrl, mo=True)
    else:
        pm.error("A bad type value was given: {}".format(c_type))
        return

    print("Controls constrained.")

    return new_constraint


def setup():
    '''
    set up the HIK bind process.
    '''

    ns = nm.from_selection()

    # Change the rig attrs:
    for attr in cns.HIK_ATTRIBUTE_SETTINGS.items():
        pm.setAttr(ns + attr[0], attr[1])

    print('Making a duplicate skeleton...')
    duplicate_skeleton(ns=ns)
    print('Duplicate has been created in scene.')
    print('Characterizing skeleton...')
    characterize_skeleton()
    print('Duplicate skeleton has been characterized for HIK.\nBring in your animation FBX and '
        'position it now.')

    return


def bake():
    '''
    Bake the HIK animation onto the controllers of the rig selected.
    '''

    ns = nm.from_selection()
    constraints_list = constrain_skeleton(ns=ns)

    playBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    frame_range = pm.timeControl(playBackSlider, q=True, ra=True)

    # Move the time slider to the beginning of the selected range.
    pm.currentTime(frame_range[0], edit=True)

    ctrl_to_key = []
    mirror = False
    for body_part in cns.CONSTRAINT_MAPPING.items():
        mirror = False
        if(body_part[0] in ['arm', 'leg']):
            print("{} is a mirrored bodypart.".format(body_part[0]))
            mirror = True
        else:
            print("{} is not a mirrored body part.".format(body_part[0]))
            mirror = False
        
        if(mirror):
            for side in ['L_', 'R_']:
                for ctrl in body_part[1].items():
                    ctrl_to_key.append(ns + side + ctrl[0])
        else:
            for ctrl in body_part[1].items():
                if(ctrl[0] != 'Cog_Ctrl'):
                    ctrl_to_key.append(ns + "C_" + ctrl[0])
                else:
                    ctrl_to_key.append(ns + ctrl[0])
                
    print("Control list: {}".format(ctrl_to_key))

    # Iterate through the frame range selected.
    while(pm.currentTime(q=True) < frame_range[1]):

        for ctrl in ctrl_to_key:
            # Key things!
            pm.setKeyframe(ctrl_to_key, at=['translate', 'rotate'])

        next_frame = (pm.currentTime(q=True) + 1)
        pm.currentTime(next_frame, edit=True)
        pm.refresh(cv=True)

    print("Deleting constraints: {}".format(constraints_list))
    pm.delete(constraints_list)

    


