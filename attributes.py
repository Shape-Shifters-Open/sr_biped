'''
attributes.py

Module for manipulating attributes,
macros, converting attribute types between picker and channel box, etc.
'''

from inspect import Attribute
import pymel.core as pm

def multi_as_enum(node=None, switch_on=None, attr_list=None):
    '''
    space_as_enum

    Take multiple attributes, floats or bools and treats them like they are all part of a single
    enum, by switching a given attr to "1" and others to zero.
    Space switches on the Shaper Rig are multiple-floats, but for pickers that want to treat the
    system as though it uses enum, we can simply pick the attr we want to turn on and interatively
    turn off the rest.

    usage:
    multi_as_enum()
    '''

    if(node == None):
        pm.warning("Must specify a node.")
        return
    elif(switch_on == None):
        pm.warning ("Nothing to switch to 'on' was specified.")
        return
    elif(attr_list == None):
        pm.warning ("No list of attrs was specified.")
        return

    # Just in case node came in as a PyNode, reduce to a string name.
    if(isinstance(node, pm.PyNode)):
        node_string = node.name()
    else:
        node_string = node

    # Run through all attrs provided in list, switching them all off except desired one.
    for attribute in attr_list:
        if(attribute != switch_on):
            pm.setAttr("{}.{}".format(node_string, attribute), 0)
            print ("Set {}.{} to 0.".format(node_string, attribute))
        else:
            pm.setAttr("{}.{}".format(node_string, attribute), 1)
            print ("Set {}.{} to 1.".format(node_string, attribute))

    return


def zero_attributes(node, ignore_list=[]):
    '''
    Zero's out the relevant-to-animation attributes that exist on the given control of a rig.
    
    node - transform node of the control to operate on.
    '''

    attr_list = pm.listAttr(node, v=True, u=True, k=True,)

    for attr in attr_list:
        if(attr == "index"):
            continue
        if(attr in ignore_list):
            continue

        attribute = eval("node.{}".format(attr))
        # Some attributes are not-zero as a default ('zero out' is an industry wide misnomer!)
        default_value = pm.attributeQuery(attr, n=node, listDefault=True)[0]
        attribute.set(default_value)
        print("resetting {} to {}.".format(attribute, default_value))
        
# EOF