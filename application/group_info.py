#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields, route_with, route_menu
from store import StoreModel
from monkey import ndb
from user_info import UserInfoModel


class GroupInfoModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團購名稱",
            "store": u"商家",
        }
    title = Fields.StringProperty(default=u"未命名")
    store = Fields.CategoryProperty(kind=StoreModel)
    date_last = Fields.DateTimeProperty()  #收單截止日
    date_send = Fields.DateTimeProperty()  #預計寄送日

    @classmethod
    def get_by_name(cls, store, name):
        return cls.query(cls.title == name, cls.store == store).get()

    @classmethod
    def get_or_create_by_name(cls, store, name):
        n = cls.get_by_name(store, name)
        if n is None:
            n = GroupInfoModel()
            n.title = name
            n.store = store
            n.put()
        return n


class GroupInfo(Controller):
    class Meta:
        title = u"團購"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20
        dir_name = Controller.get_file_name(__file__)

    @route_with("/console/group")
    def console_group(self):
        self.context["page_title_for_nav"] = u"團購項目"
        def factory(controller):
            return GroupInfoModel.query(ndb.AND(
            GroupInfoModel.store == controller.session["store"],
        )).order(-GroupInfoModel.sort)
        self.scaffold.query_factory = factory
        return scaffold.list(self)