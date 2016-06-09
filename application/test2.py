#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields, route_with
from order_info import OrderInfoModel

class Test2Model(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "user_name": u"使用者名稱",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(default=u"未命名")
    user_name = Fields.StringProperty(default=u"未命名")
    is_enable = Fields.BooleanProperty(default=True)


    @classmethod
    def all_enable(cls):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.is_enable==True).order(-cls.sort)


class Test2(Controller):
    class Meta:
        title = u"使用者帳戶"
        components = (scaffold.Scaffolding, Pagination, Search)

    @route_menu(list_name=u"backend", text=u"Test2", sort=3)
    @route_with("/admin/test2")
    def admin_list(self):
        return scaffold.list(self)
