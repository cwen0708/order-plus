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
from authorizations import require_orderplus_user, default_authorizations
import json

process_collection = [
    "process_main",
    "process_order_check",
    "process_payment",
    "process_pre_order",
    "process_send_goods",
    "process_order_end",
    "process_order_change",
    "process_order_cancel",
    "process_return_goods",
    "process_refund"
]


def in_process_collection(process_name):
    return process_name in process_collection


def do_process(process_name):
    import logging
    logging.info(process_name)

def get_next_process(store, order, list_num, process_name):
    now_process = []
    if len(now_process) == 0:
        do_process("process_order_start")
        now_process.append("process_order_start")

def get_process(process_name, process_dict):
    pass

class StoreProcessModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"商家名稱",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(default=u"未命名的流程")
    path = Fields.StringProperty(default=u"")


    @classmethod
    def all_enable(cls):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.is_enable==True).order(-cls.sort)


class StoreProcess(Controller):
    class Meta:
        title = u"訂購流程"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 50
        authorizations = default_authorizations
        process_names = {
            "process_main": u"主流程",
            "process_order_check": u"訂單確認",
            "process_payment": u"金流收取",
            "process_pre_order": u"預購流程",
            "process_send_goods": u"貨品寄送",
            "process_order_end": u"訂單結束",
            "process_order_change": u"訂單修改",
            "process_order_cancel": u"訂單取消",
            "process_return_goods": u"退貨處理",
            "process_refund": u"金流退款",
            "process_seller_check": u"賣家確認訂單",
            "process_buyer_check": u"買家確認訂單",

            "process_auto_lock_order_change": u"買家停用訂單修改流程",
            "process_auto_lock_order_cancel": u"買家停用消取訂單流程",
            "process_auto_lock_return_goods": u"買家停用退貨流程",
        }
        desc = {
            "process_main": u"每筆訂單的起始流程，由此流程決定訂單分發之哪一個子流程",
            "process_order_check": u"與買家進行訂單的數量、金額、運費等項目之確認",
            "process_payment": u"向買家進行收款",
            "process_pre_order": u"若為團購項目，則轉至此流程",
            "process_send_goods": u"貨品寄送",
            "process_order_end": u"訂單結束",
            "process_order_change": u"訂單修改",
            "process_order_cancel": u"訂單取消",
            "process_return_goods": u"退貨處理",
            "process_refund": u"金流退款",
            "process_seller_check": u"賣家確認訂單",
            "process_buyer_check": u"買家確認訂單",
        }

    def get_name(self, process):
        return self.meta.process_names[process]

    def add_name(self, process):
        process_names = self.meta.process_names
        desc = self.meta.desc
        for item in process:
            item["title"] = process_names[item["id"]]
            if item["id"] in desc:
                item["desc"] = desc[item["id"]]
            else:
                item["desc"] = u""
            if item["id"] in process_collection:
                item["can_edit"] = True
            else:
                item["can_edit"] = False

        return process

    @route_with("/console/store/process")
    def index(self):
        store = self.Util.decode_key(self.session["store"]).get()
        menu = []
        for item in process_collection:
            try:
                record_list = json.loads(getattr(store, item))
            except:
                record_list = []
            menu.append({
                "id": item,
                "path": self.add_name(record_list)
            })
        self.context["menus"] = self.add_name(menu)

    @route_with("/console/store/process/edit/<target>")
    def process_edit(self, target):
        tools = {
            "process_main": [
                {"id": "process_order_check"},
                {"id": "process_payment"},
                {"id": "process_pre_order"},
                {"id": "process_send_goods"},
                {"id": "process_order_end"},
            ],
            "process_order_check": [
                {"id": "process_seller_check"},
                {"id": "process_auto_lock_order_change"},
                {"id": "process_auto_lock_order_cancel"},
                {"id": "process_auto_lock_return_goods"},
            ],
            "process_payment": [
                {"id": "process_seller_check"},
            ],
            "process_pre_order": [
                {"id": "process_seller_check"},
            ],
            "process_send_goods": [
                {"id": "process_seller_check"},
            ],
            "process_order_end": [
                {"id": "process_seller_check"},
            ],
            "process_order_change": [
                {"id": "process_seller_check"},
            ],
            "process_order_cancel": [
                {"id": "process_seller_check"},
            ],
            "process_return_goods": [
                {"id": "process_seller_check"},
            ],
            "process_refund": [
                {"id": "process_seller_check"},
            ],
            "general": [
                {"id": "process_seller_check"},
            ]
        }

        store = self.Util.decode_key(self.session["store"]).get()
        record = getattr(store, target)
        try:
            record_list = json.loads(record)
        except:
            record_list = []

        if len(record_list) == 0:
            self.context["has_record"] = False
        else:
            self.context["has_record"] = True

        check_list = []
        for target_item in record_list:
            check_list.append(target_item["id"])
        import logging
        tools_box = []
        tools_temp = tools[target] + tools["general"] + record_list
        for tools_item in tools_temp:
            if tools_item["id"] not in check_list:
                tools_box.append(tools_item)
                check_list.append(tools_item["id"])
                logging.info("%s no in list" % tools_item["id"])
            else:
                logging.warn("%s in list" % tools_item["id"])

        self.context["page_id"] = target
        self.context["page_name"] = self.get_name(target)
        self.context["record"] = self.add_name(record_list)
        self.context["toolbox"] = self.add_name(tools_box)
        return scaffold.view(self, self.session["store"])

    @route_with("/console/store/process/edit/<target>/save.json")
    def process_edit_save(self, target):
        store = self.Util.decode_key(self.session["store"]).get()
        setattr(store, target, self.params.get_string("p"))
        store.put()
        self.meta.change_view("json")
        self.context["data"] = {
            "target": '%s' % self.params.get_string("p")
        }
