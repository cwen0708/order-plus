#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.


from monkey import Controller, scaffold, route_menu, route_with
from monkey.components.pagination import Pagination
from monkey.components.csrf import CSRF, csrf_protect
from monkey.components.search import Search
from .. import news_category_action_helper


class NewsCategory(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_actions = ("list",)
        pagination_limit = 50

    class Scaffold:
        title = news_category_action_helper["actions"]
        display_properties_in_list = ("title_lang_zhtw", "name")


    @route_menu(list_name=u"backend", text=u"最新消息分類", sort=112, icon="photo", group=u"內容管理")
    @route_with('/admin/news_category/list')
    def admin_list(self):
        return scaffold.list(self)