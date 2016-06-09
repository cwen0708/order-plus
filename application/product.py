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
from store import StoreModel
from group_info import GroupInfoModel
from monkey import ndb
from datetime import datetime


def get_or_create_product_by_feature(store, group_info, item):
    """依照產品特徵建立或取得產品
    :param store:
    :param group_info:
    :param item:
    :return:
    """
    p = ProductModel.get_by_feature(store, group_info.key, item["name"], item["spec"], item["price"])
    if p is None:
        p = ProductModel()
    p.title = item["name"]
    p.spec = item["spec"]
    p.price = item["price"]
    p.image_url = item["image"]
    p.limit_1 += item["quantity"]
    p.limit_2 = item["limit"]
    p.group_info = group_info.key
    if "date" in item:
        d = datetime.strptime(item["date"] + ":00", "%Y/%m/%d %H:%M:00")
    else:
        d = datetime(9999, 12, 31)
    p.date = d
    p.store = store
    p.put()
    return p


class ProductModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"商品名稱",
            "spec": u"商品規格",
            "image_url": u"圖片網址",
            "quantity": u"庫存數量",
            "date": u"可購買期限",
            "price": u"價格",
            "limit_1": u"已出售數量",
            "limit_2": u"可供購買數量",
        }
    title = Fields.StringProperty(default=u"未命名的商品")
    spec = Fields.StringProperty(default=u"")
    image_url = Fields.StringProperty(default=u"")
    date = Fields.DateTimeProperty()
    price = Fields.FloatProperty(default=0.0)
    limit_1 = Fields.IntegerProperty(default=0)
    limit_2 = Fields.IntegerProperty(default=99999)
    store = Fields.CategoryProperty(kind=StoreModel)
    group_info = Fields.CategoryProperty(kind=GroupInfoModel)

    @classmethod
    def get_by_feature(cls, store, group_info, title, spec, price):
        p = float(price)
        return cls.query(cls.title == title, cls.spec == spec, cls.price == p, cls.store == store, cls.group_info == group_info).get()


class Product(Controller):
    class Meta:
        title = u"商品"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20

    
    @route_with("/console/product")
    def console_product(self):
        self.context["page_title_for_nav"] = u"商品列表"
        def factory(controller):
            return ProductModel.query(ndb.AND(
            ProductModel.store == controller.session["store"],
        )).order(-ProductModel.sort)
        self.scaffold.query_factory = factory
        return scaffold.list(self)