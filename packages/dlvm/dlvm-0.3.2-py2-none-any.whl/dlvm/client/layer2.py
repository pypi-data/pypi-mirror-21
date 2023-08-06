#!/usr/bin/env python

import logging
import time
from layer1 import Layer1
from fsm import fsm_register, fsm_start, fsm_resume

logger = logging.getLogger('dlvm_client')


class Layer2Error(Exception):
    pass


def dpv_available_action(client, obt, obt_args):
    kwargs = {
        'dpv_name': obt_args['dpv_name'],
        'action': 'available',
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.dpv_put(**kwargs)
    return ret


def dpv_available_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        dpv_name = obt_args['dpv_name']
        ret = client.dpv_get(dpv_name=dpv_name)
        if ret['status_code'] != 200:
            return 'err', ret
        if ret['body']['status'] == 'available':
            return 'ok', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


dpv_available_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dpv_available_action,
            'check': dpv_available_check,
            'ok': -1,
            'err': -2,
        },
    },
}

fsm_register('dpv_available', dpv_available_stage_info)


def dlv_create_action(client, obt, obt_args):
    kwargs = {
        'dlv_name': obt_args['dlv_name'],
        'dlv_size': obt_args['dlv_size'],
        'init_size': obt_args['init_size'],
        'partition_count': obt_args['partition_count'],
        'dvg_name': obt_args['dvg_name'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.dlvs_post(**kwargs)
    return ret


def dlv_create_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        dlv_name = obt_args['dlv_name']
        ret = client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'detached':
            return 'ok', ret
        elif status != 'creating':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def dlv_delete_action(client, obt, obt_args):
    kwargs = {
        'dlv_name': obt_args['dlv_name'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.dlv_delete(**kwargs)
    return ret


def dlv_delete_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        dlv_name = obt_args['dlv_name']
        ret = client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] == 404:
            return 'ok', ret
        elif ret['status_code'] != 200:
            return 'err', ret
        else:
            status = ret['data']['body']['status']
            if status != 'deleting':
                return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


dlv_create_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_create_action,
            'check': dlv_create_check,
            'ok': -1,
            'err': 2,
        },
        2: {
            'action': dlv_delete_action,
            'check': dlv_delete_check,
            'ok': -2,
            'err': 2,
        },
    },
}

fsm_register('dlv_create', dlv_create_stage_info)


dlv_delete_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_delete_action,
            'check': dlv_delete_check,
            'ok': -1,
            'err': 1,
        },
    },
}

fsm_register('dlv_delete', dlv_delete_stage_info)


def dlv_attach_action(client, obt, obt_args):
    kwargs = {
        'dlv_name': obt_args['dlv_name'],
        'action': 'attach',
        'thost_name': obt_args['thost_name'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.dlv_put(**kwargs)
    return ret


def dlv_attach_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        dlv_name = obt_args['dlv_name']
        ret = client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'attached':
            return 'ok', ret
        elif status != 'attaching':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def dlv_detach_action(client, obt, obt_args):
    kwargs = {
        'dlv_name': obt_args['dlv_name'],
        'action': 'detach',
        'thost_name': obt_args['thost_name'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.dlv_put(**kwargs)
    return ret


def dlv_detach_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        dlv_name = obt_args['dlv_name']
        ret = client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'detached':
            return 'ok', ret
        elif status != 'detaching':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


dlv_attach_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_attach_action,
            'check': dlv_attach_check,
            'ok': -1,
            'err': 2,
        },
        2: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -2,
            'err': 2,
        },
    },
}

fsm_register('dlv_attach', dlv_attach_stage_info)


dlv_detach_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -1,
            'err': 1,
        },
    },
}

fsm_register('dlv_detach', dlv_detach_stage_info)


def thost_available_action(client, obt, obt_args):
    kwargs = {
        'thost_name': obt_args['thost_name'],
        'action': 'available',
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.thost_put(**kwargs)
    return ret


def thost_available_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        thost_name = obt_args['thost_name']
        ret = client.thost_get(thost_name=thost_name)
        if ret['status_code'] != 200:
            return 'err', ret
        elif ret['body']['status'] == 'available':
            return 'ok', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


thost_available_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': thost_available_action,
            'check': thost_available_check,
            'ok': -1,
            'err': -2,
        },
    },
}

fsm_register('thost_available', thost_available_stage_info)


def snap_create_action(client, obt, obt_args):
    ori_snap_name = obt_args['ori_snap_name']
    snap_name = obt_args['snap_name']
    snap_pairs = '%s:%s' % (snap_name, ori_snap_name)
    kwargs = {
        'dlv_name': obt_args['dlv_name'],
        'snap_pairs': snap_pairs,
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.snaps_post(**kwargs)
    return ret


def snap_create_check(client, obt_args):
    retry = 0
    dlv_name = obt_args['dlv_name']
    snap_name = obt_args['snap_name']
    kwargs = {
        'dlv_name': dlv_name,
        'snap_name': snap_name,
    }
    while retry < obt_args['max_retry']:
        ret = client.snap_get(**kwargs)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'available':
            return 'ok', ret
        elif status != 'creating':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def snap_delete_action(client, obt, obt_args):
    dlv_name = obt_args['dlv_name']
    snap_name = obt_args['snap_name']
    kwargs = {
        'dlv_name': dlv_name,
        'snap_name': snap_name,
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.snap_delete(**kwargs)
    return ret


def snap_delete_check(client, obt_args):
    retry = 0
    dlv_name = obt_args['dlv_name']
    snap_name = obt_args['snap_name']
    kwargs = {
        'dlv_name': dlv_name,
        'snap_name': snap_name,
    }
    while retry < obt_args['max_retry']:
        ret = client.snap_get(**kwargs)
        if ret['status_code'] == 404:
            return 'ok', ret
        elif ret['status_code'] != 200:
            return 'err', ret
        else:
            status = ret['data']['body']['status']
            if status != 'deleting':
                return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


snap_create_simple_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': snap_create_action,
            'check': snap_create_check,
            'ok': -1,
            'err': 2,
        },
        2: {
            'action': snap_delete_action,
            'check': dlv_delete_check,
            'ok': -2,
            'err': 2,
        },
    },
}

fsm_register('snap_create_simple', snap_create_simple_stage_info)


snap_create_complex_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_attach_action,
            'check': dlv_attach_check,
            'ok': 2,
            'err': 10,
        },
        2: {
            'action': snap_create_action,
            'check': snap_create_check,
            'ok': 3,
            'err': 11,
        },
        3: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -1,
            'err': 3,
        },
        10: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -2,
            'err': 10,
        },
        11: {
            'action': snap_delete_action,
            'check': snap_delete_check,
            'ok': 10,
            'err': 11,
        },
    },
}

fsm_register('snap_create_complex', snap_create_complex_stage_info)


snap_delete_simple_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': snap_delete_action,
            'check': snap_delete_check,
            'ok': -1,
            'err': 1,
        },
    },
}

fsm_register('snap_delete_simple', snap_delete_simple_stage_info)


snap_delete_complex_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_attach_action,
            'check': dlv_attach_check,
            'ok': 2,
            'err': 10,
        },
        2: {
            'action': snap_delete_action,
            'check': snap_delete_check,
            'ok': 3,
            'err': 2,
        },
        3: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -1,
            'err': 3,
        },
        10: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -2,
            'er': 10,
        },
    },
}

fsm_register('snap_delete_complex', snap_delete_complex_stage_info)


def fj_create_action(client, obt, obt_args):
    kwargs = {
        'fj_name': obt_args['fj_name'],
        'dlv_name': obt_args['dlv_name'],
        'ori_id': obt_args['ori_id'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.fjs_post(**kwargs)
    return ret


def fj_create_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        fj_name = obt_args['fj_name']
        ret = client.fj_get(fj_name=fj_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'processing':
            return 'ok', ret
        elif status != 'creating':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def fj_cancel_action(client, obt, obt_args):
    kwargs = {
        'fj_name': obt_args['fj_name'],
        'action': 'cancel',
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.fj_put(**kwargs)
    return ret


def fj_cancel_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        fj_name = obt_args['fj_name']
        ret = client.fj_get(fj_name=fj_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status == 'canceled':
            return 'ok', ret
        elif status != 'canceling':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def fj_finish_action(client, obt, obt_args):
    kwargs = {
        'fj_name': obt_args['fj_name'],
        'action': 'finish',
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.fj_put(**kwargs)
    return ret


def fj_finish_check(client, obt_args):
    retry = 0
    while retry < obt_args['max_retry']:
        fj_name = obt_args['fj_name']
        ret = client.fj_get(fj_name=fj_name)
        if ret['status_code'] != 200:
            return 'err', ret
        status = ret['data']['body']['status']
        if status != 'finished':
            return 'ok', ret
        elif status != 'finishing':
            return 'err', ret
        time.sleep(obt_args['interval'])
        retry += 1
    return 'err', ret


def fj_delete_action(client, obt, obt_args):
    kwargs = {
        'fj_name': obt_args['fj_name'],
        't_id': obt['t_id'],
        't_owner': obt['t_owner'],
        't_stage': obt['t_stage'],
    }
    ret = client.fj_delete(**kwargs)
    return ret


def fj_delete_check(client, obt_args):
    fj_name = obt_args['fj_name']
    ret = client.fj_get(fj_name=fj_name)
    if ret['status_code'] == 404:
        return 'ok', ret
    else:
        return 'err', ret


fj_create_simple_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': fj_create_action,
            'check': fj_create_check,
            'ok': -1,
            'err': 2,
        },
        2: {
            'action': fj_cancel_action,
            'check': fj_cancel_check,
            'ok': 3,
            'err': 2,
        },
        3: {
            'action': fj_delete_action,
            'check': fj_delete_check,
            'ok': -2,
            'err': 3,
        },
    },
}

fsm_register('fj_create_simple', fj_create_simple_stage_info)


fj_create_complex_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': dlv_attach_action,
            'check': dlv_attach_check,
            'ok': 2,
            'err': 10,
        },
        2: {
            'action': fj_create_action,
            'check': fj_create_check,
            'ok': 3,
            'err': 11,
        },
        3: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -1,
            'err': 3,
        },
        10: {
            'action': dlv_detach_action,
            'check': dlv_detach_check,
            'ok': -2,
            'err': 10,
        },
        11: {
            'action': fj_cancel_action,
            'check': fj_cancel_check,
            'ok': 12,
            'err': 11,
        },
        12: {
            'action': fj_delete_action,
            'check': fj_delete_check,
            'ok': -2,
            'err': 12,
        },
    },
}

fsm_register('fj_create_complex', fj_create_complex_stage_info)


fj_cancel_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': fj_cancel_action,
            'check': fj_cancel_check,
            'ok': 2,
            'err': 1,
        },
        2: {
            'action': fj_delete_action,
            'check': fj_delete_check,
            'ok': -1,
            'err': 2,
        },
    },
}

fsm_register('fj_cancel', fj_cancel_stage_info)


fj_finish_stage_info = {
    'init_stage_num': 1,
    'stages': {
        1: {
            'action': fj_finish_action,
            'check': fj_finish_check,
            'ok': 2,
            'err': 1,
        },
        2: {
            'action': fj_delete_action,
            'check': fj_delete_check,
            'ok': -1,
            'err': 2,
        },
    },
}

fsm_register('fj_finish', fj_finish_stage_info)


class Layer2(object):

    def __init__(self, api_server_list):
        self.client = Layer1(api_server_list)

    def dpv_list(self):
        ret = self.client.dpvs_get()
        return ret

    def dpv_display(self, dpv_name):
        ret = self.client.dpv_get(dpv_name=dpv_name)
        return ret

    def dpv_create(self, dpv_name):
        ret = self.client.dpvs_post(dpv_name=dpv_name)
        return ret

    def dpv_delete(self, dpv_name):
        ret = self.client.dpv_delete(dpv_name=dpv_name)
        return ret

    def dpv_available(self, dpv_name):
        obt_args = {
            'dpv_name': dpv_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'dpv_available', self.client, obt_args)

    def dpv_unavailable(self, dpv_name):
        ret = self.client.dpv_put(
            dpv_name=dpv_name, action='unavailable')
        return ret

    def obt_list(self):
        ret = self.client.obts_get()
        return ret

    def obt_display(self, t_id):
        ret = self.client.obt_get(t_id=t_id)
        return ret

    def obt_resume(self, t_id):
        return fsm_resume(self.client, t_id)

    def thost_list(self):
        ret = self.client.thosts_get()
        return ret

    def thost_display(self, thost_name):
        ret = self.client.thost_get(thost_name=thost_name)
        return ret

    def thost_create(self, thost_name):
        ret = self.client.thosts_post(thost_name=thost_name)
        return ret

    def thost_delete(self, thost_name):
        ret = self.client.thost_delete(thost_name=thost_name)
        return ret

    def thost_unavailable(self, thost_name):
        ret = self.client.thost_put(
            thost_name=thost_name, action='unavailable')
        return ret

    def thost_available(self, thost_name):
        obt_args = {
            'thost_name': thost_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'thost_available', self.client, obt_args)

    def dvg_list(self):
        ret = self.client.dvgs_get()
        return ret

    def dvg_display(self, dvg_name):
        ret = self.client.dvg_get(dvg_name=dvg_name)
        return ret

    def dvg_create(self, dvg_name):
        ret = self.client.dvgs_post(dvg_name=dvg_name)
        return ret

    def dvg_delete(self, dvg_name):
        ret = self.client.dvg_delete(dvg_name=dvg_name)
        return ret

    def dvg_extend(self, dvg_name, dpv_name):
        ret = self.client.dvg_put(
            dvg_name=dvg_name, action='extend', dpv_name=dpv_name)
        return ret

    def dvg_reduce(self, dvg_name, dpv_name):
        ret = self.client.dvg_put(
            dvg_name=dvg_name, action='reduce', dpv_name=dpv_name)
        return ret

    def dlv_create(
            self, dlv_name, dvg_name, dlv_size, init_size, partition_count):
        obt_args = {
            'dlv_name': dlv_name,
            'dvg_name': dvg_name,
            'dlv_size': dlv_size,
            'init_size': init_size,
            'partition_count': partition_count,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'dlv_create', self.client, obt_args)

    def dlv_delete(self, dlv_name):
        obt_args = {
            'dlv_name': dlv_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'dlv_delete', self.client, obt_args)

    def dlv_display(self, dlv_name):
        ret = self.client.dlv_get(dlv_name=dlv_name)
        return ret

    def dlv_list(self):
        ret = self.client.dlvs_get()
        return ret

    def dlv_attach(self, dlv_name, thost_name):
        obt_args = {
            'dlv_name': dlv_name,
            'thost_name': thost_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'dlv_attach', self.client, obt_args)

    def dlv_detach(self, dlv_name, thost_name):
        obt_args = {
            'dlv_name': dlv_name,
            'thost_name': thost_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'dlv_detach', self.client, obt_args)

    def snap_list(self, dlv_name):
        ret = self.client.snaps_get(dlv_name=dlv_name)
        return ret

    def snap_display(self, dlv_name, snap_name):
        ret = self.client.snap_get(
            dlv_name=dlv_name, snap_name=snap_name)
        return ret

    def snap_create(self, dlv_name, snap_name, ori_snap_name):
        ret = self.client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            raise Layer2Error(ret)
        status = ret['data']['body']['status']
        if status == 'attached':
            obt_args = {
                'dlv_name': dlv_name,
                'snap_name': snap_name,
                'ori_snap_name': ori_snap_name,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'snap_create_simple', self.client, obt_args)
        elif status == 'detached':
            groups = ret['data']['body']['groups']
            thost_name = groups[0]['legs'][0]['dpv_name']
            obt_args = {
                'dlv_name': dlv_name,
                'snap_name': snap_name,
                'ori_snap_name': ori_snap_name,
                'thost_name': thost_name,
                'ori_snap_name': ori_snap_name,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'snap_create_complex', self.client, obt_args)
        else:
            raise Layer2Error('invalid status %s' % status)

    def snap_delete(self, dlv_name, snap_name):
        ret = self.client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            raise Layer2Error(ret)
        status = ret['data']['body']['status']
        if status == 'attached':
            obt_args = {
                'dlv_name': dlv_name,
                'snap_name': snap_name,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'snap_delete_simple', self.client, obt_args)
        elif status == 'detached':
            groups = ret['data']['body']['groups']
            thost_name = groups[0]['legs'][0]['dpv_name']
            obt_args = {
                'dlv_name': dlv_name,
                'snap_name': snap_name,
                'thost_name': thost_name,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'snap_delete_complex', self.client, obt_args)
        else:
            raise Layer2Error('invalid status %s' % status)

    def fj_list(self):
        ret = self.client.fjs_get()
        return ret

    def fj_display(self, fj_name):
        ret = self.client.fj_get(fj_name=fj_name)
        return ret

    def fj_create(self, fj_name, dlv_name, ori_id):
        ret = self.client.dlv_get(dlv_name=dlv_name)
        if ret['status_code'] != 200:
            raise Layer2Error(ret)
        status = ret['data']['body']['status']
        if status == 'attached':
            obt_args = {
                'fj_name': fj_name,
                'dlv_name': dlv_name,
                'ori_id': ori_id,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'fj_create_simple', self.client, obt_args)
        elif status == 'detached':
            groups = ret['data']['body']['groups']
            thost_name = groups[0]['legs'][0]['dpv_name']
            obt_args = {
                'fj_name': fj_name,
                'dlv_name': dlv_name,
                'thost_name': thost_name,
                'ori_id': ori_id,
                'max_retry': 10,
                'interval': 1,
            }
            return fsm_start(
                'fj_create_complex', self.client, obt_args)
        else:
            raise Layer2Error('invalid status %s' % status)

    def fj_cancel(self, fj_name):
        obt_args = {
            'fj_name': fj_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'fj_cancel', self.client, obt_args)

    def fj_finish(self, fj_name):
        obt_args = {
            'fj_name': fj_name,
            'max_retry': 10,
            'interval': 1,
        }
        return fsm_start(
            'fj_finish', self.client, obt_args)
