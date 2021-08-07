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

    # next up, constraints!