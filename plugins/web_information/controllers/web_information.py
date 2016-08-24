#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from google.appengine.api import namespace_manager
from monkey import Controller, scaffold
from monkey import route_with, route_menu
from google.appengine.api import memcache
from .. import web_information_action_helper
import datetime
from monkey.components.pagination import Pagination
from monkey.components.search import Search
import datetime


class WebInformation(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 50

    class Scaffold:
        title = web_information_action_helper["actions"]
        display_properties_in_list = ("name", "title", "domain_expiration_date",
                                      "space_expiration_date","contact_person",
                                      "contact_telephone", "contact_mobile",)

    @route_menu(list_name=u"backend", text=u"網站資訊", sort=9951, icon="gears", group=u"系統設定")
    @route_with('/admin/web_information/list')
    def admin_list(self):
        namespace_manager.set_namespace("shared.information")
        return scaffold.list(self)

    def admin_add(self):
        namespace_manager.set_namespace("shared.information")
        return scaffold.add(self)

    def admin_edit(self, key):
        namespace_manager.set_namespace("shared.information")
        self.context["item"] = self.util.decode_key(key).get()
        return scaffold.edit(self, key)

    def admin_view(self, key):
        namespace_manager.set_namespace("shared.information")
        self.context["item"] = self.util.decode_key(key).get()
        return scaffold.edit(self, key)

    def admin_delete(self, key):
        namespace_manager.set_namespace("shared.information")
        return scaffold.delete(self, key)

    @route_with('/admin/web_information/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }
