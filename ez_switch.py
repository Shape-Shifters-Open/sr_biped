import pymel.core as pm
import sr_biped.fkik as fkik

# Constants
ik_bones_dict = {
    'shoulder': 'armUprIK_drv',
    'elbow': 'armLwrIK_drv',
    'wrist': 'armWristIK_drv',
    'hip': 'legUprIK_drv',
    'knee': 'legLwrIK_drv',
    'ankle': 'legAnkleIK_drv'
}

fk_bones_dict = {
    'shoulder': 'armUprFK_drv',
    'elbow': 'armLwrFK_drv',
    'wrist': 'armWristFK_drv',
    'hip': 'legUprFK_drv',
    'knee': 'legLwrFK_drv',
    'ankle': 'legAnkleFK_drv',
}

ik_ctrls_dict = {
    'shoulder': 'ArmUprIK_CTRL',
    'elbow': 'ArmElbow_CTRL',
    'elbow_pv': 'ArmPV_CTRL',
    'wrist': 'ArmWristIK_CTRL',
    'pv_offset_elbow': 'ArmPV_nOffset',
    'hip': 'LegUprIK_CTRL',
    'knee_pv': 'LegPV_CTRL',
    'knee': 'LegKnee_CTRL',
    'ankle': 'LegAnkleIK_CTRL',
    'toe': 'toe_CTRL',
    'ball': 'ball_CTRL',
    'heel': 'heel_CTRL'
}

fk_ctrls_dict = {
    'shoulder': 'ArmUprFK_CTRL',
    'elbow': 'ArmLwrFK_CTRL',
    'wrist': 'ArmWristFK_CTRL',
    'hip': 'LegUprFK_CTRL',
    'knee': 'LegLwrFK_CTRL',
    'ankle': 'LegAnkleFK_CTRL'
}

settings_ctrls_dict = {
    'leg': 'LegSetting_CTRL',
    'arm': 'ArmSetting_CTRL'
}


# Main
def show_ui():
    if (pm.window("ezSwitch", exists=True)):  # Delete existing window
        pm.deleteUI("ezSwitch")

    win = pm.window("ezSwitch", title="EZ Switch", wh=[180, 60], mnb=0, mxb=0, sizeable=0)
    layout = pm.rowColumnLayout(nr=2)
    btn = pm.button(label="Switch", parent=layout, w=180, h=60)

    btn.setCommand(toggle_selected)
    win.show()


def switch_ik_blend_attr(side, part, value):
    pm.setAttr('{}_{}.ikBlend'.format(side, settings_ctrls_dict[part]), value)

    return


def get_ik_blend_attr(side, part):
    value = pm.getAttr('{}_{}.ikBlend'.format(side, settings_ctrls_dict[part]))

    return value


def toggle_selected(*args):
    for sel in pm.selected():
        if 'CTRL' in str(sel) and str(sel)[0] in ['L', 'R']:
            # Checks if this is a control and has a side
            side = str(sel)[0]
            part = 'leg' if 'Leg_null' in sel.longName() else 'arm'

            ik_fk_toggle(side, part)


def ik_fk_toggle(side, part):
    value = 1 - get_ik_blend_attr(side, part)

    if value < 0.5:
        fkik.fk_to_ik(side, part, ik_bones_dict, fk_ctrls_dict)
        switch_ik_blend_attr(side, part, 0)

    else:
        switch_ik_blend_attr(side, part, 1)
        fkik.ik_to_fk(side, part, fk_bones_dict, ik_ctrls_dict, amp_pv=15)

    return


show_ui()
