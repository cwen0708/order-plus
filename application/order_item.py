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
from order_detail import OrderDetailModel
from product import ProductModel


class OrderItemModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"摘要",
            "order_detail": u"所屬訂單細節",
        }
        not_show = {
            "title": u"摘要",
            "order_detail": u"所屬訂單細節",
        }
    title = Fields.StringProperty(default=u"未命名的商品")
    order_detail = Fields.CategoryProperty(kind=OrderDetailModel)
    product = Fields.CategoryProperty(kind=ProductModel)
    quantity = Fields.IntegerProperty()


class OrderItem(Controller):
    class Meta:
        title = u"訂單細節-項目"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20
