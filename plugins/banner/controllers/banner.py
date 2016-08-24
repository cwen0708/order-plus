#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu, Fields, route_with
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from .. import banner_action_helper


class Banner(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10

    class Scaffold:
        title = banner_action_helper["actions"]
        display_properties_in_list = ("name", "image", "is_enable", "category")

    @route_menu(list_name=u"backend", text=u"輪撥圖", sort=101, icon="photo", group=u"內容管理")
    @route_with('/admin/banner/list')
    def admin_list(self):
        return scaffold.list(self)

    @route_with('/admin/banner/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }