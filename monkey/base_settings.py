#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/22.

settings = dict()
# 應用程式設定
settings['application'] = {}
settings['application']['name'] = u'OrderPlus'
settings['application']['custom_error'] = True
settings['application']['message_timeout'] = 28800

# 驗証失敗時，重新導向路徑
settings["authorization_redirect"] = []
settings["authorization_redirect"].append({"authorization": 'require_orderplus_user', "redirect": '/'})
settings["authorization_redirect"].append({"authorization": 'require_admin', "redirect": '/admin/login'})
settings["authorization_redirect"].append({"authorization": 'require_user', "redirect": '/login.html'})

# 時區
settings['timezone'] = {}
settings['timezone']['local'] = 'Asia/Taipei'
# 設定用來寄送郵件的相關設定
settings['email'] = {}
settings['email']['sender'] = None

settings["name"]

settings['appstats'] = {
    'enabled': False,
    'enabled_live': False
}

settings['app_config'] = {
    'webapp2_extras.sessions': {
        # WebApp2 encrypted cookie key
        # You can use a UUID generator like http://www.famkruithof.net/uuid/uuidgen
        'secret_key': '_PUT_KEY_HERE_YOUR_SECRET_KEY_',
    },
    'webapp2_extras.auth': {
        'user_model': 'plugins.custom_auth.models.user.User',
        'user_attributes': ['email'],
    }
}
