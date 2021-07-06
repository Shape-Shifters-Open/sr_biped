'''
scene.py
Module of sr_biped.  
Matt Riche 2021

Checks the contents of the scene for certain things that need to be there if we are going to run
sr_biped stuff.  Proper err-checking for things that should be there will make mis-use more 
graceful.
'''

import pymel.core as pm

def rig_in_scene(mode=0):
    '''
    Verify if a few particularly named nodes are in the scene. Use this as a sign we have a 
    shaper-rig in scene.

    mode : [0|1] 0 for check that there's a single rig.  1 for check for any in scene, positive if
    there's one or more.
    '''

    dnt_groups = pm.ls("*DO_NOT_TOUCH_GRP*")

    if(mode == 0):
        if(len(dnt_groups) == 1):
            return True
        else:
            pm.warning("There should be exactly 1 shaper-rig biped in this scene.")
            return False
    elif(mode == 1):
        if(len(dnt_groups) > 0):
            return True
        else:
            pm.warning("There needs to be at least one shaper-rig biped in this scene.")
    else:
        pm.error("rig_in_scene() was passed an invalid mode number.")

