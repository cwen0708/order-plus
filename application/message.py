#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/1/9.

from google.appengine.api import channel
from monkey.core import json_util
from monkey.core.ndb import util
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey.behaviors.searchable import Searchable
from monkey import ndb
from monkey import Controller, scaffold
from monkey import BasicModel
from monkey import Fields, route_with
from application import get_mobile
from user_info import UserInfoModel
from store import StoreModel
from order_info import OrderInfoModel
import time


def create_message(msg_from, msg_type, store, purchaser, receiver, order_info=None):
    MessageModel.insert(msg_from, msg_type, store, purchaser, receiver, order_info)


def create_message_relationship(account_key, client_id):
    pass


def crete_channel_token(target, timeout=480):
    return channel.create_channel(target, timeout)


def send_message_to_mobile(mobile, data):
    m = get_mobile(mobile)
    #send_message_to_account(m.account, data)


def send_message_to_account(account_key, data):
    result = unicode(json_util.stringify(data))
    pass


def send_message_to_client(client_id, data):
    result = unicode(json_util.stringify(data))
    channel.send_message(client_id, result)


class AccountClientModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團購名稱",
            "store": u"商家",
        }
    account = Fields.CategoryProperty(kind=UserInfoModel)
    client_id = Fields.StringProperty(default=u"")


class StoreClientModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團購名稱",
            "store": u"商家",
        }
    store = Fields.CategoryProperty(kind=UserInfoModel)
    client_id = Fields.StringProperty(default=u"")


class MessageModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團購名稱",
            "store": u"商家",
        }
    store = Fields.CategoryProperty(kind=StoreModel)
    user_a = Fields.CategoryProperty(kind=UserInfoModel)
    user_b = Fields.CategoryProperty(kind=UserInfoModel)
    order_info = Fields.CategoryProperty(kind=OrderInfoModel)

    store_text = Fields.StringProperty()
    user_a_text = Fields.StringProperty()
    user_b_text = Fields.StringProperty()

    message_type = Fields.StringProperty()
    message_from = Fields.StringProperty()
    store_read = Fields.BooleanProperty(default=False)
    user_a_read = Fields.BooleanProperty(default=False)
    user_b_read = Fields.BooleanProperty(default=False)

    @classmethod
    def read(cls, order_info, store_key, account_key):
        r = ndb.Key(urlsafe=order_info).get()
        if r is None:
            return
        li = cls.query(cls.order_info==r.key).fetch()
        to_put = []
        for item in li:
            if item.store == store_key and item.store_read is False:
                item.store_read = True
                to_put.append(item)
            else:
                if r.purchaser == account_key and item.user_a_read is False:
                    r.user_a_read = True
                    to_put.append(item)
                elif item.user_b_read is False:
                    r.user_b_read = True
                    to_put.append(item)
        ndb.put_multi(to_put)

    @classmethod
    def insert(cls, msg_from, msg_type, store, purchaser, receiver, order_info=None):
        msg = cls()
        if order_info is not None:
            msg.order_info = order_info.key
        msg.store = store["key"]
        msg.store_text = store["message"]
        msg.user_a = purchaser["key"]
        msg.user_a_text = purchaser["message"]
        msg.user_b = receiver["key"]
        msg.user_b_text = u""
        if purchaser["key"] != purchaser["key"]:
            msg.user_b_text = receiver["message"]
        msg.message_from = msg_from
        msg.message_type = msg_type
        msg.put()
        return msg


class Message(Controller):
    class Meta:
        title = u"通知訊息"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20

    @route_with("/channel_push_message")
    @route_with("/remote/channel_push_message")
    def push_message(self):
        self.meta.change_view("jsonp")
        self.context["data"] = {"error": "need_login"}
        self.state = self.params.get_integer("state")
        self.cash_flow_state = self.params.get_integer("cash_flow_state")
        self.freight_flow_state = self.params.get_integer("freight_flow_state")
        self.official_order = self.params.get_boolean("official_order")
        self.client_id = None
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                m = get_mobile(self.session["mobile"])
                if m is None:
                    return
                self.client_id = self.util.encode_key(m.account)
        if self.client_id is None:
            return
        def factory(controller):
            return MessageModel.query(ndb.OR(
            MessageModel.store == controller.session["store"],
            MessageModel.user_a == controller.session["account"]
        )).order(MessageModel.sort)
        self.scaffold.query_factory = factory
        scaffold.list(self)
        list = self.context[self.scaffold.plural].fetch()
        msg_list = []
        for item in list:
            msg_id = u""
            url = u""
            message = u""
            is_read = False
            sort = item.sort
            created = item.created.isoformat()
            if item.message_type == u"order":
                msg_id = u"message_" + self.Util.encode_key(item.order_info)
                if item.store == self.session["store"]:
                    url = "/console/sales/detail/" + self.Util.encode_key(item.order_info)
                    message = item.store_text
                    is_read = item.store_read
                else:
                    url = "/console/order/detail/" + self.Util.encode_key(item.order_info)
                    if item.purchaser.key == self.session["account"]:
                        message = item.user_a_text
                        is_read = item.user_a_read
                    else:
                        message = item.user_b_text
                        is_read = item.user_b_read
            #TODO 訂單內訊息
            #TODO 人對商家的訊息
            #TODO 人對人的訊息
            msg_list.append({
                "id": msg_id,
                "message": message,
                "is_read": is_read,
                "url": url,
                "sort": sort,
                "created": created
            })
        self.context["data"] = msg_list
        result = unicode(json_util.stringify(msg_list))
        send_message_to_client(self.client_id, {"action": "message", "list": result})
