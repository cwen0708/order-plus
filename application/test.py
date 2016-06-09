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
from test2 import Test2Model

class TestModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "user_name": u"使用者名稱",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(default=u"未命名")
    user_name = Fields.StringProperty(default=u"未命名")
    is_enable = Fields.BooleanProperty(default=True)
    editor = Fields.RichTextProperty()
    n1 = Fields.StringProperty(required=True)
    order_info = Fields.CategoryProperty(kind=Test2Model)
    image = Fields.ImageProperty()
    images = Fields.ImagesProperty()


    @classmethod
    def all_enable(cls):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.is_enable==True).order(-cls.sort)


class Test(Controller):
    class Meta:
        scaffold_title = {
            "list": u"測試",
            "add": u"新增測試",
            "edit": u"編輯測試",
            "view": u"檢視測試",
        }
        components = (scaffold.Scaffolding, Pagination, Search)

    @route_menu(list_name=u"backend", text=u"測試", sort=31, group=u"Test")
    @route_with("/admin/test")
    def admin_user_info(self):
        return scaffold.view(self, self.session["account"])

    @route_menu(list_name=u"backend", text=u"測試2", sort=32, group=u"Test")
    @route_with("/admin/user_info/setting")
    def admin_test_setting(self):
        return scaffold.view(self, self.session["account"])