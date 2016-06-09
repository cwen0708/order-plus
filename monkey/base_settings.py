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

# 外掛模組
settings['plugins'] = {}
settings['plugins']['scaffold'] = True
settings['plugins']['flash_messages'] = True
settings['plugins']['backend_account'] = True
settings['plugins']['backend_account_administrator'] = {}
settings['plugins']['backend_account_administrator']['name'] = u'管理者'
settings['plugins']['backend_account_administrator']['account'] = u'admin'
settings['plugins']['backend_account_administrator']['password'] = u'qwER12#$'
settings['plugins']['backend_account_administrator']['level'] = 999
settings['plugins']['backend_ui_saimiri'] = False
settings['plugins']['backend_ui_material'] = True
settings['plugins']['online_code'] = True
settings['plugins']['oauth'] = False
settings['plugins']['oauth_manager'] = False
settings['plugins']['custom_auth'] = False
settings['plugins']['recaptcha'] = True
settings['plugins']['web_settings'] = False
settings['plugins']['web_page'] = False
settings['plugins']['web_file'] = True
settings['plugins']['settings'] = False

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
