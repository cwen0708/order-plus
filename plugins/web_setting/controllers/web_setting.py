#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold
from monkey import route_with, route_menu
from google.appengine.api import memcache
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from .. import web_setting_action_helper
import datetime


class WebSetting(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 50

    class Scaffold:
        title = web_setting_action_helper["actions"]
        display_properties_in_list = ("setting_name", "setting_key", "setting_value")

    @route_menu(list_name=u"backend", text=u"網站設定", sort=9900, icon="gears", group=u"系統設定")
    @route_with('/admin/web_setting/list')
    def admin_list(self):
        return scaffold.list(self)

    def admin_edit(self, key, *args):
        def reload_settings(**kwargs):
            item = kwargs["item"]
            memcache_key = "setting." + self.namespace + "." + item.setting_key
            memcache.set(key=memcache_key, value=item.setting_value, time=10)
            self.components.flash_messages(u'設定已被儲存，不過，有些應用程實例可能正在執行中，您可能無法立即查看到變動後的設定。', 'warning')

        self.events.scaffold_after_save += reload_settings
        return scaffold.edit(self, key)

    @route_with('/admin/web_setting/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }