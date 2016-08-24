#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu, Fields, route_with
from .. import web_menu_action_helper
from monkey.components.pagination import Pagination
from monkey.components.search import Search
import datetime


class WebMenu(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 50

    class Scaffold:
        title = web_menu_action_helper["actions"]
        display_properties_in_list = ("title", "name", "page_url", "is_enable", "category")

    @route_menu(list_name=u"backend", text=u"網站選單", sort=9911, icon="gears", group=u"系統設定")
    @route_with('/admin/web_menu/list')
    def admin_list(self):
        return scaffold.list(self)

    @route_with('/admin/web_menu/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }

    def admin_add(self):
        def scaffold_after_apply(**kwargs):
            item = kwargs["item"]
            if item.name is u"" or item.name is None:
                import random
                item.name = '-'.join(str(random.randint(1000, 9999)) for i in range(4))
                item.put()
        self.events.scaffold_after_apply += scaffold_after_apply
        return scaffold.add(self)

    def admin_edit(self, key):
        def scaffold_after_apply(**kwargs):
            item = kwargs["item"]
            if item.name is u"" or item.name is None:
                import random
                item.name = '-'.join(str(random.randint(1000, 9999)) for i in range(4))
                item.put()
        self.events.scaffold_after_apply += scaffold_after_apply
        return scaffold.edit(self, key)
