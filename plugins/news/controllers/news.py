#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu, route_with
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from .. import news_action_helper


class News(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_actions = ("list",)
        pagination_limit = 50

    class Scaffold:
        title = news_action_helper["actions"]
        display_properties_in_list = ("name", "title_lang_zhtw", "date")

    @route_with('/admin/news/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }

    @route_menu(list_name=u"backend", text=u"最新消息", sort=111, icon="photo", group=u"內容管理")
    @route_with('/admin/news/list')
    def admin_list(self):
        return scaffold.list(self)