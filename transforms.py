# transforms.py
# Matt Riche 2021
# Module for transform related tasks in sr_suite_utilities

import pymel.core as pm
import pymel.core.datatypes as dt


def aim_at(node, target=None, vec=None, pole_vec=(0,-1,0), axis=1, pole=2):
    '''
    Aim's a node's axis at another point in space and a "pole axis" down a normalized vector.
    Operates in place on the given node-- returns nothing.

    node - PyNode of the transform to be aimed
    target - PyNode of object to be aimed at (if vec == None)
    vec - dt.Vector of direction to aim in (if target == None)
    pole_vec - A dt.Vector that aims toward the "pole" of this aim constraint.
    axis - the axis along which to aim down. (enumated x,y,z where x=0)
    pole - the "pole" axis, which will aim at the vec (enumerated x,y,z where x=0)
    '''

    # Check for bad args:
    if(pole == axis):
        pm.error("sr_biped error: Chosen pole and aim axis can't be identical.")

    # Format this input into a dt.Vector:
    pole_vec = dt.Vector(pole_vec)

    # Sort what we are aiming at:
    # If we got a target, use it.
    if(target != None):
        target_pos = dt.Vector(pm.xform(target, q=True, ws=True, t=True))
        node_pos = dt.Vector(pm.xform(node, q=True, ws=True, t=True))
        target_vec = target_pos - node_pos
        target_vec.normalize()

        if(vec != None):
            pm.warning("Both vec and node are populated.  Node will take precidence.")

    # If we got a vec, use that instead.
    elif(vec != None):
        target_vec = vec.normal()

    else:
        pm.error("sr_biped error: Either a vector or a target is required.")
        return

    # Step two, "unconstrained" vec; cross product of normalized vector and normalized pole vector 
    # is found and stored.
    last_vec = target_vec.cross(pole_vec)

    # Step three, we "clean" the pole vector by getting the cross product of the aim and the 
    # "unconstrained" axis vector.
    clean_pole = target_vec.cross(last_vec)

    # Before we proceed, we shuffle based on the incoming arguments.  Chosen axis to aim...
    x_axis_vec = y_axis_vec = z_axis_vec = None
    if(axis == 0):
        x_axis_vec = target_vec
    elif(axis == 1):
        y_axis_vec = target_vec
    elif(axis == 2):
        z_axis_vec = target_vec

    # And unconstrained.
    if(pole == 0):
        x_axis_vec = clean_pole
    elif(pole == 1):
        y_axis_vec = clean_pole
    elif(pole == 2):
        z_axis_vec = clean_pole

    # Decide which axis gets the "last_vec" applied based on whether it still contains None
    for last_axis in ['x_axis_vec', 'y_axis_vec', 'z_axis_vec']:
        if(eval(last_axis + ' == None') == True):
            exec('{} = last_vec'.format(last_axis))
            break

    # Turn the axis vectors into lists to slot into the Matrix:
    m0 = list(x_axis_vec)
    m1 = list(y_axis_vec)
    m2 = list(z_axis_vec)

    # Fabricate a bottom row for the scale of the Matrix.
    m3 = [1, 1, 1, 1]

    # Recompose transform data here so it lands inside the matrix correctly.
    m0.append(target_pos[0])
    m1.append(target_pos[1])
    m2.append(target_pos[2])

    # Step four, apply the values of each vector to the correct place in the matrix.
    aimed_matrix = dt.Matrix(m0, m1, m2, m3)

    pm.xform(node, m=aimed_matrix)

    print(aimed_matrix.formated())

    return