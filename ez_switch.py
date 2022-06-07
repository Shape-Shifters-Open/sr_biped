import pymel.core as pm
from sr_biped import fkik

# Constants
ik_bones_dict = {
    'shoulder': 'armUprIK_drv',
    'elbow': 'armLwrIK_drv',
    'wrist': 'armWristIK_drv',
    'hip': 'legUprIK_drv',
    'knee': 'legLwrIK_drv',
    'ankle': 'legAnkleIK_drv',

    'rev_bk_hip': 'revBkLegUprIK_drv',
    'rev_bk_knee': 'revBkLegLwr01IK_drv',
    'rev_bk_ankle': 'revBkLegLwr02IK_drv',
    'rev_bk_foot': 'revBkLegAnkleIK_drv',

    'rev_fr_hip': 'revFrLegUprIK_drv',
    'rev_fr_knee': 'revFrLegLwr01IK_drv',
    'rev_fr_ankle': 'revFrLegLwr02IK_drv',
    'rev_fr_foot': 'revFrLegAnkleIK_drv',
}

fk_bones_dict = {
    'shoulder': 'armUprFK_drv',
    'elbow': 'armLwrFK_drv',
    'wrist': 'armWristFK_drv',
    'hip': 'legUprFK_drv',
    'knee': 'legLwrFK_drv',
    'ankle': 'legAnkleFK_drv',

    'rev_bk_hip': 'revBkLegUprFK_drv',
    'rev_bk_knee': 'revBkLegLwr01FK_drv',
    'rev_bk_knee2': 'revBkLegLwr02FK_drv',
    'rev_bk_ankle': 'revBkLegAnkleFK_drv',

    'rev_fr_hip': 'revFrLegUprFK_drv',
    'rev_fr_knee': 'revFrLegLwr01FK_drv',
    'rev_fr_knee2': 'revFrLegLwr02FK_drv',
    'rev_fr_ankle': 'revFrLegAnkleFK_drv',
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
    'heel': 'heel_CTRL',

    'rev_bk_hip': 'revBkLegUprIK_CTRL',
    'rev_bk_knee': 'RevBklegknee01_CTRL',
    'rev_bk_knee2': 'RevBklegknee02_CTRL',
    'rev_bk_ankle': 'revBkLegAnkleIK_CTRL',
    'rev_bk_knee_pv': 'RevBklegPV_CTRL',

    'rev_fr_hip': 'revFrLegUprIK_CTRL',
    'rev_fr_knee': 'RevFrlegknee01_CTRL',
    'rev_fr_knee2': 'RevFrlegknee02_CTRL',
    'rev_fr_ankle': 'revFrLegAnkleIK_CTRL',
    'rev_fr_knee_pv': 'RevFrlegPV_CTRL',
}

fk_ctrls_dict = {
    'shoulder': 'ArmUprFK_CTRL',
    'elbow': 'ArmLwrFK_CTRL',
    'wrist': 'ArmWristFK_CTRL',
    'hip': 'LegUprFK_CTRL',
    'knee': 'LegLwrFK_CTRL',
    'ankle': 'LegAnkleFK_CTRL',

    'rev_bk_hip': 'revBkLegUprFK_CTRL',
    'rev_bk_knee': 'revBkLegLwr01FK_CTRL',
    'rev_bk_ankle': 'revBkLegLwr02FK_CTRL',
    'rev_bk_foot': 'revBkLegAnkleFK_CTRL',

    'rev_fr_hip': 'revFrLegUprFK_CTRL',
    'rev_fr_knee': 'revFrLegLwr01FK_CTRL',
    'rev_fr_ankle': 'revFrLegLwr02FK_CTRL',
    'rev_fr_foot': 'revFrLegAnkleFK_CTRL'
}

settings_ctrls_dict = {
    'leg': 'LegSetting_CTRL',
    'arm': 'ArmSetting_CTRL',
    'revFrleg': 'RevFrlegSetting_CTRL',
    'revBkleg': 'RevBklegSetting_CTRL'
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
    sels = pm.selected()

    for sel in pm.selected():
        if 'CTRL' in str(sel) and str(sel)[0] in ['L', 'R']:
            side = str(sel)[0]

            if 'Leg_null' in sel.longName():
                part = 'leg'

            elif 'Arm_null' in sel.longName():
                part = 'arm'

            elif 'RevFrleg_null' in sel.longName():
                part = 'revFrleg'

            elif 'RevBkleg_null' in sel.longName():
                part = 'revBkleg'

            ik_fk_toggle(side, part)

    pm.select(sels)


def ik_fk_toggle(side, part):
    value = 1 - get_ik_blend_attr(side, part)
    if 'rev' in part:
        pole_direction = 1

    else:
        pole_direction = 1

    if value < 0.5:
        fkik.fk_to_ik(side, part, ik_bones_dict, fk_ctrls_dict, key=False)
        switch_ik_blend_attr(side, part, 0)

    else:
        switch_ik_blend_attr(side, part, 1)
        fkik.ik_to_fk(side, part, fk_bones_dict, ik_ctrls_dict, amp_pv=40,
                      pole_direction=pole_direction, key=False)

    return


show_ui()
