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
from monkey import Fields, route_with
from store_process import StoreProcessModel


class StoreModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"商家名稱",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(default=u"未命名")
    is_enable = Fields.BooleanProperty(default=True)

    process_main = Fields.TextProperty(default=u"")         # 主流程
    process_order_check = Fields.TextProperty(default=u"")  # 訂單確認
    process_payment = Fields.TextProperty(default=u"")      # 金流收取
    process_pre_order = Fields.TextProperty(default=u"")    # 預購流程
    process_send_goods = Fields.TextProperty(default=u"")   # 貨品寄送
    process_order_end = Fields.TextProperty(default=u"")    # 訂單結束
    process_order_change = Fields.TextProperty(default=u"") # 訂單修改
    process_order_cancel = Fields.TextProperty(default=u"") # 訂單取消
    process_return_goods = Fields.TextProperty(default=u"") # 退貨處理
    process_refund = Fields.TextProperty(default=u"")       # 金流退款

    @classmethod
    def all_enable(cls):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.is_enable==True).order(-cls.sort)


class Store(Controller):
    class Meta:
        title = u"商家"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20

    @route_with("/console/store/setting")
    def console_store_setting(self):
        return scaffold.view(self, self.session["store"])