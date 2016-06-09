#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/3/3
import os
import random
import time
from datetime import datetime
from monkey import ndb
from monkey import auth, add_authorizations
from monkey import Controller, route_with, route, controllers, scaffold, BasicModel
from monkey import settings, Pagination
from monkey.core.gaeforms import model_form
from monkey.components.search import Search
from product import ProductModel
from group_info import GroupInfoModel
from order_item import OrderItemModel
from order_detail import OrderDetailModel
from application import require_orderplus_user, default_authorizations
from application import create_message, crete_channel_token, send_message_to_client
from application import get_mobile, get_or_create_mobile
from application import get_or_create_product_by_feature
from application import create_order


def process_order(number, a1, a2, info, order_list, store_name):
    store_number = get_or_create_mobile(number, store_name=store_name)
    store_key = store_number.store
    order = create_order(a1, a2, store_key, info)
    create_message("purchaser", "order",
        {
            "key": store_key,
            "message": u"%s 向您訂購了商品" % info["f1"]
        }, {
            "key": a1.account,
            "message": u"向賣家送出訂單"
        }, {
            "key": a2.account,
            "message": u"%s 訂購商品給您" % info["f1"]
        }, order
    )
    for n in order_list:
        if len(n["items"]) > 0:
            group_info = GroupInfoModel.get_or_create_by_name(store_key, n["name"])
            order_detail = OrderDetailModel()
            order_detail.title = n["name"]
            order_detail.group_info = group_info.key
            order_detail.order_info = order.key
            order_detail.shipping_fee = n["shipping_fee"]
            order_detail.sum = n["sum"]
            order_detail.put()
            for item in n["items"]:
                product = get_or_create_product_by_feature(store_key, group_info, item)
                order_item = OrderItemModel()
                order_item.title = product.title
                order_item.order_detail = order_detail.key
                order_item.product = product.key
                order_item.quantity = item["quantity"]
                order_item.put()
    return len(order_list), order.key


class HomeModel(BasicModel):
    class Meta:
        pass


class Home(Controller):
    class Meta:
        title = u"訂單"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10
        authorizations = default_authorizations

    @route_with('/')
    @route_with('/index.html')
    def index(self):
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                return self.redirect("/dashboard")

    @route_with('/doc.html')
    def doc(self):
        pass

    @route_with('/price.html')
    def price(self):
        pass

    @route_with('/db/clean')
    def db_clean(self):
        from mobile import MobileModel
        from mobile_key import MobileKeyModel
        from user_info import UserInfoModel
        from message import MessageModel
        from store import StoreModel
        from order_info import OrderInfoModel
        ndb.delete_multi(GroupInfoModel.query().fetch(keys_only=True))
        ndb.delete_multi(MobileModel.query().fetch(keys_only=True))
        ndb.delete_multi(MobileKeyModel.query().fetch(keys_only=True))
        ndb.delete_multi(OrderDetailModel.query().fetch(keys_only=True))
        ndb.delete_multi(OrderInfoModel.query().fetch(keys_only=True))
        ndb.delete_multi(OrderItemModel.query().fetch(keys_only=True))
        ndb.delete_multi(ProductModel.query().fetch(keys_only=True))
        ndb.delete_multi(StoreModel.query().fetch(keys_only=True))
        ndb.delete_multi(UserInfoModel.query().fetch(keys_only=True))
        ndb.delete_multi(MessageModel.query().fetch(keys_only=True))
        return "all delete"


    @route_with('/remote/get_shopping_fee_info')
    def get_shopping_fee_info(self, *args):
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.context["mobile"] = self.params.get_mobile_number("n")
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                return self.session["client_id"]

    @route_with('/remote/me')
    def get_profile_info(self, *args):
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                return self.session["client_id"]
        return "none"

    @route_with('/remote/send_order_info')
    def send_order_info(self, *args):
        from post_token import check_token
        self.meta.change_view('json')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        items = self.params.get_json("items")
        info = self.params.get_json("info")
        store = self.params.get_mobile_number("store")
        store_name = self.params.get_string("store_name")
        a1 = get_or_create_mobile(info["f2"], name=info["f1"])
        check_info = check_token(a1.number, self.params.get_string("token"))
        if check_info is None:
            self.context["data"] = {"state": "invalid"}
            return
        a2 = get_or_create_mobile(info["f4"], name=info["f3"])
        p, key = process_order(store, a1, a2, info, items, store_name)
        send_message_to_client(check_info, {
            "action": "post", "status": "success", "client": check_info,
            "key": key
        })

        self.context["data"] = {"state": "success"}

    @route_with("/dashboard")
    @add_authorizations(require_orderplus_user)
    def console_dashboard(self):
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        if "mobile" in self.session:
            if self.session["mobile"] is None:
                return self.redirect("/")
        else:
            return self.redirect("/")
        m = get_mobile(self.session["mobile"])
        self.session["store"] = m.store
        self.session["account"] = m.account
        self.context["user_name"] = m.account.get().user_name
        self.context["store"] = m.store
        self.context["account"] = m.account
        self.context["bg_color"] = u"bg-light-blue-a400"

    @route_with("/console/welcome")
    @add_authorizations(require_orderplus_user)
    def console_welcome(self):
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        m = get_mobile(self.session["mobile"])
        self.session["store"] = m.store
        self.session["account"] = m.account
        self.context["mobile"] = self.session["mobile"]
        self.context["store"] = m.store
        self.context["account"] = m.account
        self.context["user_name"] = m.account.get().user_name

    @route_with("/site_sidebar.html")
    def site_sidebar(self):
        pass

    @route_with('/api_info.json')
    def info(self):
        from plugins.online_code.models import online_code_target_model
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        target = self.params.get_string("target", u"api")
        api = online_code_target_model.OnlineCodeTargetModel.get_by_name(target)
        channel = online_code_target_model.OnlineCodeTargetModel.get_by_name("channel")
        self.context['data'] = {
            'js-vision': api.js_vision,
            'css-vision': api.css_vision,
            'channel-vision': channel.js_vision,
        }