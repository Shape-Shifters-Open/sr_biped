'''
spaces.py
Matt Riche
2021

For matching spaces on switching between perceived parent spaces.
'''

import pymel.core as pm
import pymel.core.datatypes as dt


def get_world_space(node):
    '''
    Get a vector representing the world-space of a node, return it.

    node - Any node with a transform.

    Return value: dt.Vector
    '''

    pos = dt.Vector(pm.xform(node, q=True, t=True, ws=True))

    return pos


def match_and_key(node, pos):
    '''
    Given a node and a vector to match to, match the node to the vector and key it.
    
    node - A transform node.
    '''

    pm.match(node, ws=True, t=pos)
    pm.setKeyframe(node, at=['translate', 'rotate'])

    print("{} keyed to {} in worldspace.".format(node.name(), pos))

    return
