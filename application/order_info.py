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
from user_info import UserInfoModel
from monkey import ndb, auth
from authorizations import require_orderplus_user, require_orderplus_user_for_prefix
from datetime import datetime


def get_order_process(forecast, path_now):
    import json
    ct = {
        "now": path_now,
        "next_process": "",
        "next_error": "",
        "at_next": False
    }

    def process_helper(item, ct):
        if "children" in item:
            for sub in item["children"]:
                if ct["at_next"] and ct["next_process"] == "":
                    ct["next_process"] = sub["id"]
                if str(sub["id"]) == ct["now"]:
                    ct["at_next"] = True
                    if "children" in sub:
                        ct["next_error"] = sub["children"][0]["id"]
            for sub in item["children"]:
                process_helper(sub, ct)

    record_list = json.loads(forecast)
    for sub in record_list:
        if ct["at_next"] and ct["next_process"] == "":
            ct["next_process"] = sub["id"]
        if str(sub["id"]) == ct["now"]:
            ct["at_next"] = True
            if "children" in sub:
                ct["next_error"] = sub["children"][0]["id"]
    for sub in record_list:
        process_helper(sub, ct)
    if ct["next_process"].find("jump_") >= 0:
        ct["next_process"] = ct["next_process"].replace("jump_", "")
    if ct["next_error"].find("jump_") >= 0:
        ct["next_error"] = ct["next_error"].replace("jump_", "")
    return ct


def create_order(a1, a2, store, info):
    """ 建立訂單
    :param a1: 訂購者
    :param a2: 收件者
    :param store: 商家
    :param info: 其它訊息
    :return: 訂單
    """
    order = OrderInfoModel()
    order.store = store
    order.purchaser = a1.account
    order.purchaser_name = info["f1"]
    order.purchaser_mobile = info["f2"]
    order.receiver = a2.account
    order.receiver_name = info["f3"]
    order.purchaser_mobile = info["f4"]
    order.receiver_address = info["f5"]
    order.state = 0
    order.cash_flow_state = 0
    order.freight_flow_state = 0
    order.path_forecast = u'''
[{"id":"start"},{"id":"seller_check_order"},{"id":"wait_buyer_pay"},{"id":"end","children":[{"id":"seller_cancel"},{"id":"buyer_cancel"}]},{"id":"buyer_change_order","children":[{"id":"jump_buyer_cancel"}]},{"id":"seller_check_order_2","children":[{"id":"jump_seller_cancel"}]},{"id":"seller_pay_with_system","children":[{"id":"auto_seller_check_pay"}]}]
      '''
    order.path_event = u'''
    [
        {"if": "seller_check_order", "on": "quantity_change", "then": "jump_to_seller_cancel"},
    ]
      '''
    order.path_now = "start"
    p = get_order_process(order.path_forecast, order.path_now)
    order.path_next = p["next_process"]
    n = int(info["f2"].replace("+8869", "09")) - 900000000 / 10 + int(datetime.now().strftime("%S%H%M%d")) / 100
    order.order_info_id = u"%s-%s-%s" % (int(datetime.now().strftime("%Y%m")), str(n)[:3], str(n)[3:7])
    order.put()
    return order


class OrderInfoModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "store": u"商家",
            "purchaser": u"購買人",
            "purchaser_name": u"購買人姓名",
            "purchaser_mobile": u"購買人手機",
            "receiver_name": u"收件人姓名",
            "receiver_address": u"收件人地址",
            "receiver_mobile": u"收件人手機",
            "state": u"訂單狀態",
            "cash_flow_state": u"金流狀態",
            "freight_flow_state": u"物流狀態",
            "official_order": u"正式訂單",
            "official_order_date": u"正式訂單成立時間",
        }
    order_info_id = Fields.StringProperty()
    store = Fields.CategoryProperty(kind=StoreModel)
    purchaser = Fields.CategoryProperty(kind=UserInfoModel)
    purchaser_name = Fields.StringProperty(default=u"")
    purchaser_mobile = Fields.StringProperty(default=u"")
    receiver = Fields.CategoryProperty(kind=UserInfoModel)
    receiver_name = Fields.StringProperty(default=u"")
    receiver_address = Fields.StringProperty(default=u"")
    receiver_mobile = Fields.StringProperty(default=u"")
    state = Fields.IntegerProperty(default=0)
    cash_flow_state = Fields.IntegerProperty(default=0)
    freight_flow_state = Fields.IntegerProperty(default=0)
    path_event = Fields.StringProperty(default="")
    path_forecast = Fields.StringProperty(default="")
    path_now = Fields.StringProperty(default="")
    path_next = Fields.StringProperty(default="")

    process_now = Fields.StringProperty(default="")
    process_1 = Fields.TextProperty(default="")
    process_2 = Fields.TextProperty(default="")
    process_3 = Fields.TextProperty(default="")
    process_4 = Fields.TextProperty(default="")
    process_5 = Fields.TextProperty(default="")

    official_order = Fields.BooleanProperty(default=False)
    official_order_date = Fields.DateTimeProperty()

    def details(self):
        from order_detail import OrderDetailModel
        return OrderDetailModel.query(OrderDetailModel.order_info == self.key).order(-OrderDetailModel.sort).fetch()

    def messages(self):
        from message import MessageModel
        return MessageModel.query(MessageModel.order_info == self.key).order(-MessageModel.sort).fetch()


class OrderInfo(Controller):
    class Meta:
        title = u"訂單"
        pagination_actions = ["list", "order", "sales"]
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10
        authorizations = (auth.require_admin_for_route(route=('admin',)),
                          require_orderplus_user_for_prefix(prefix=('console',)))

    admin_list = scaffold.list
    console_list = scaffold.list

    @route_with("/console/old_order_1")
    def console_order_1(self):
        self.state = self.params.get_integer("state")
        self.cash_flow_state = self.params.get_integer("cash_flow_state")
        self.freight_flow_state = self.params.get_integer("freight_flow_state")
        self.official_order = self.params.get_boolean("official_order")
        self.context["page_title"] = u"訂購管理"
        limit = self.components.pagination.paginate()
        return scaffold.list(self)


    @route_with("/console/order")
    def console_order(self):
        self.state = self.params.get_integer("state")
        self.cash_flow_state = self.params.get_integer("cash_flow_state")
        self.freight_flow_state = self.params.get_integer("freight_flow_state")
        self.official_order = self.params.get_boolean("official_order")
        self.context["page_title_for_nav"] = u"訂購管理"
        def factory(controller):
            return OrderInfoModel.query(ndb.AND(
            OrderInfoModel.purchaser == controller.session["account"],
            OrderInfoModel.state == controller.state,
            OrderInfoModel.cash_flow_state == controller.cash_flow_state,
            OrderInfoModel.freight_flow_state == controller.freight_flow_state,
            OrderInfoModel.official_order == controller.official_order,
        )).order(-OrderInfoModel.sort)
        self.scaffold.query_factory = factory
        return scaffold.list(self)

    @route_with("/console/sales")
    def console_sales(self):
        self.state = self.params.get_integer("state")
        self.cash_flow_state = self.params.get_integer("cash_flow_state")
        self.freight_flow_state = self.params.get_integer("freight_flow_state")
        self.official_order = self.params.get_boolean("official_order")
        self.context["page_title_for_nav"] = u"銷售管理"
        def factory(controller):
            return OrderInfoModel.query(ndb.AND(
            OrderInfoModel.store == controller.session["store"],
            OrderInfoModel.state == controller.state,
            OrderInfoModel.cash_flow_state == controller.cash_flow_state,
            OrderInfoModel.freight_flow_state == controller.freight_flow_state,
            OrderInfoModel.official_order == controller.official_order,
        )).order(-OrderInfoModel.sort)
        self.scaffold.query_factory = factory
        return scaffold.list(self)

    @route_with("/console/order/detail/<key>")
    def console_order_detail(self, key):
        from message import MessageModel
        self.context["page_title_for_nav"] = u"訂購管理"
        self.context["store_key"] = self.session["store"]
        self.context["account_key"] = self.session["account"]
        MessageModel.read(key, self.session["store"], self.session["account"])
        return scaffold.view(self, key)

    @route_with("/console/sales/detail/<key>")
    def console_sales_detail(self, key):
        from message import MessageModel
        self.context["page_title_for_nav"] = u"銷售管理"
        self.context["store_key"] = self.session["store"]
        self.context["account_key"] = self.session["account"]
        MessageModel.read(key, self.session["store"], self.session["account"])
        return scaffold.view(self, key)


"""
訂單流程
order_start         訂單啟動
order_check       訂單確認 -> 訂單修改 / 訂單取消
payment            金流收取 -> 訂單取消
pre_order          預購流程
send_goods       貨品寄送 -> 訂單取消
order_end         訂單結束
order_change    訂單修改
order_cancel     訂單取消
return_goods    退貨處理
refund             金流退款

order_check
seller_check    賣家確認訂單
buyer_check   買家確認訂單



"""