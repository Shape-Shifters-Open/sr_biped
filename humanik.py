'''
humanik.py

For automated interactions between HumanIK and our rigging standard.
'''

import pymel.core as pm
import pymel.core.datatypes as dt
import constants as cns
import maya.mel as mel


def HIK_characterize(ns=""):
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
    mel.eval ('loadPlugin "MayaHIK";ToggleCharacterControls;hikCreateDefinition;'
        'hikOnSwitchContenxtualTabs;')

    for joint_name, fbIkIndex in cns.HIK_CHARACTERIZE_MAP.iteritems():
        print("joint name: {}\nfbIkIndex: {}\nCurrent Character:{}".format(
            joint_name, fbIkIndex, mel.eval('hikGetCurrentCharacter();')))
        mel.eval('setCharacterObject("{}","{}",{},0);'.format(
            cns.HIK_PREFIX + joint_name, mel.eval('hikGetCurrentCharacter();'), fbIkIndex)

    # next up, constraints!