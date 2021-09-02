'''
suite.py

This module controls and reads the state of the Maya suite for when we need artists to automate it's
state-changed, or piggy back on values determined by the suite's UI.
'''

import pymel.core as pm
import maya.mel as mel

def frame_selection():
    '''
    Function to test what frame-selection of the time slider the user has set.
    Returns False if there's none at all, returns a tuple of stand and end otherwise.

    Usage:
    frame_range() # No args.
    '''

    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    # Frame range is found and cast as tuple due to paranoia.
    frame_range = tuple(pm.timeControl(playback_slider, q=True, ra=True))

    print(type(frame_range))
    if(frame_range[1] - frame_range[0] <= 1.0):
        return False
    else:
        return frame_range