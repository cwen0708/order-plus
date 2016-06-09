#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/8/22.
from monkey.core.plugins import register_by_path
import threading
import logging
from models.setting import Setting as SettingsModel
from monkey import events
from google.appengine.api import memcache
import datetime
register_by_path(__file__)


global_cache = {}
local_cache = threading.local()


def activate(settings):
    if 'overrides' not in global_cache:
        global_cache['overrides'] = SettingsModel.get_settings(settings)
    settings.update(global_cache['overrides'])
    global_cache['cts'] = datetime.datetime.utcnow()


def is_active():
    return 'overrides' in global_cache


def clear_global_cache():
    if is_active():
        del global_cache['overrides']


@events.on('after_settings')
def check_update_settings(settings):
    if hasattr(local_cache, 'checked'):
        activate(settings)
        return

    local_cache.checked = True

    cts = global_cache.get('cts', None)
    nts = memcache.get('_monkey_settings_update_mutex')
    if (nts and cts and nts > cts) or (nts and not cts):
        logging.info("Settings update detected. Reloading.")
        clear_global_cache()
    global_cache['cts'] = nts

    activate(settings)
