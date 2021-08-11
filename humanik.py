'''
humanik.py

For automated interactions between HumanIK and our rigging standard.
'''

import pymel.core as pm
import pymel.core.datatypes as dt
import constants as cns
import maya.mel as mel


def duplicate_skeleton(prefix='hik_'):
    '''
    Duplicates the entire skeleton of the in-scene rig with new prefixs. (Initially for the purposes
    of making HIK-characterizable skeletons.
    
    '''
    
    # Grab the top of the SHJnt chain and duplicate from there
    to_dupe = ([node for node in pm.listRelatives(cns.TOP_JOINT, ad=True) 
        if(('RbnSrf' not in node.name()) and node.type() == 'joint')]) + [cns.TOP_JOINT]
    dup_joints = pm.duplicate(to_dupe, ic=False, rc=True, un=False, rr=True, po=True)

    # Clean up the string names of the duplicated skeleton.
    for joint in dup_joints:
        old_name = joint.name()
        suffix = old_name.split('_')[-1]
        new_name = (cns.HIK_PREFIX + old_name.replace('_' + suffix, ""))
        joint.rename(new_name)


def characterize_skeleton(ns=""):
    '''
    HIK_characterize(namespace="")
    
    Builds a separate skeleton that can safely be characterized and used with HIK.
    
    usage:
    HIK_characterize(namespace={namespace as string})
    an sr_biped must be in scene.
    '''

    # Name space will be prefix string and nothing more so we groom it with a colon.
    if(ns != ""):
        namespace = (ns + ':')

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

    
def constrain_skeleton():
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
                    constraint_by_mapping(ctrl, side=side)
        else:
            for ctrl in body_part[1].items():
                constraint_by_mapping(ctrl, side='C_')

                    

def constraint_by_mapping(map_dict, side=''):
    '''
    Takes a piece of the "mapping dict" found in constants.
    '''

    c_type = map_dict[1]['type']
    ctrl = (side + map_dict[0])

    # Brief hack for Cogs, they don't have a prefix in our standard.
    if(ctrl == 'C_Cog_Ctrl'):
        ctrl = 'Cog_Ctrl'

    # A not great hack to deal with the fact that controls have a C_ but SHJnts do not.
    if(side == "C_"):
        side = ''
    target = (cns.HIK_PREFIX + side + map_dict[1]['target'])

    print('c_type is {} from {} to {}.  Building...'.format(c_type, ctrl, target))

    if(c_type == 'parent'):
        pm.parentConstraint(target, ctrl, mo=False)
    elif(c_type == 'parent_offset'):
        pm.parentConstraint(target, ctrl, mo=True)
    elif(c_type == 'orient'):
        pm.orientConstraint(target, ctrl, mo=True)
    elif(c_type == 'point'):
        pm.pointConstraint(target, ctrl)
    elif(c_type == 'point_offset'):
        pm.pointConstraint(target, ctrl, mo=True)
    else:
        pm.error("A bad type value was given: {}".format(c_type))
        return

    print("Controls constrained.")

    return