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
from order_info import OrderInfoModel
from group_info import GroupInfoModel


class OrderDetailModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"訂購方式",
            "order_info": u"所屬訂單",
        }
    title = Fields.StringProperty(default=u"")
    order_info = Fields.CategoryProperty(kind=OrderInfoModel)
    group_info = Fields.CategoryProperty(kind=GroupInfoModel)
    shipping_fee = Fields.FloatProperty()
    sum = Fields.FloatProperty()

    def items(self):
        from order_item import OrderItemModel
        return OrderItemModel.query(OrderItemModel.order_detail == self.key).order(-OrderItemModel.sort).fetch()


class OrderDetail(Controller):
    class Meta:
        title = u"訂單細節"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20
