'''
namespaces.py

Module for finding/sorting namespaces.
'''

import pymel.core as pm


def from_selection():
    '''
    Find the namespace as a string component from a selection.

    Return value: namespace value plus ':'
    '''

    if(len(pm.ls(sl=True)) > 0):
        selection = pm.ls(sl=True)[0]
    else:
        pm.error("Can't determine namespace since nothing is selected.")
        return

    try:
        namestring = selection.name()
    except:
        pm.error("Selected object has no name method...")
        return

    if(':' in namestring):
        found_namespace = (namestring.split(':')[0] + ':')
    else:
        pm.error('The selected object has no namespace.')

    print("Namespace string is '{}'.".format(found_namespace))

    return found_namespace



    

    