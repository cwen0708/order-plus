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

    def get_name(self, process):
        return self.meta.process_names[process]

    def add_name(self, process):
        process_names = self.meta.process_names
        for item in process:
            item["title"] = process_names[item["id"]]
        return process

    @route_with("/console/store/process")
    def index(self):
        menu = []
        for item in process_collection:
            menu.append({"id": item})
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
        }

        import logging
        store = self.Util.decode_key(self.session["store"]).get()
        record = getattr(store, target)
        if record is None or record == u"" or record == "":
            record_list = []
        else:
            record_list = json.loads(record)
        if len(record_list) == 0:
            self.context["has_record"] = False
        else:
            self.context["has_record"] = True

        self.context["page_name"] = self.get_name(target)
        self.context["record"] = self.add_name(record_list)
        self.context["toolbox"] = self.add_name(tools[target])
        return scaffold.view(self, self.session["store"])

    @route_with("/console/store/process/backup/<target>")
    def process_backup(self, target):
        process_help = {
            "start": u"訂單開始",
            "seller_check_order": u"等待商家確認訂單",
            "buyer_change_order": u"等待買家確認訂單",
            "seller_check_order_2": u"等待商家再次確認訂單",
            "wait_buyer_pay": u"等待買家進行付款",
            "seller_pay_with_system": u"買家使用系統的付款方式(可自動核對金額)",
            "wait_seller_check_pay": u"等待買家確認付款",
            "auto_seller_check_pay": u"自動-買家確認付款",
            "end": u"每個訂單的結束",
            "seller_cancel": u"商家取消交易",
            "buyer_cancel": u"買家取消交易",
        }
        ct = {
            "now": "buyer_change_order",
            "next_x": "",
            "next_error": "",
            "next_at_next": False
        }

        def process_helper(item, ct):
            id = str(item["id"])
            try:
                if id.find("jump_") >= 0:
                    id = id.replace("jump_", "")
                    item["title"] = u"跳至: " + process_help[id]
                else:
                    item["title"] = process_help[id]
            except:
                item["title"] = u"未知的流程"
            if str(item["id"]).find("if") >= 0:
                item["bg"] = "bg-green-100"
            elif str(item["id"]).find("wait") >= 0:
                item["bg"] = "bg-green-100"
            elif str(item["id"]).find("cancel") >= 0:
                item["bg"] = "bg-red-100"
            else:
                item["bg"] = "bg-grey-100"

            if "children" in item:
                children = []
                for sub in item["children"]:
                    if ct["next_at_next"] and ct["next_x"] == "":
                        ct["next_x"] = sub["id"]
                    if str(sub["id"]) == ct["now"]:
                        ct["next_at_next"] = True
                        if "children" in sub:
                            ct["next_error"] = sub["children"][0]["id"]
                for sub in item["children"]:
                    children.append(process_helper(sub, ct))
                item["children"] = children
            return item

        record = u'''
[{"id":"start"},{"id":"seller_check_order"},{"id":"wait_buyer_pay"},{"id":"buyer_change_order","children":[{"id":"jump_buyer_cancel"}]},{"id":"seller_check_order_2","children":[{"id":"jump_seller_cancel"}]},{"id":"seller_pay_with_system","children":[{"id":"auto_seller_check_pay"}]},{"id":"seller_cancel","children":[{"id":"end"}]},{"id":"buyer_cancel","children":[{"id":"end"}]}]
'''
        toolbox = []
        for item in process_help:
            toolbox.append({"id": item})
        import json

        record_js_data = []
        toolbox_js_data = []
        record_list = json.loads(record)
        idx = 0
        for sub in record_list:
            if ct["next_at_next"] and ct["next_x"] == "":
                ct["next_x"] = sub["id"]
            if str(sub["id"]) == ct["now"]:
                ct["next_at_next"] = True
                if "children" in sub:
                    ct["next_error"] = sub["children"][0]["id"]
        for sub in record_list:
            record_js_data.append(process_helper(sub, ct))
        for item in toolbox:
            toolbox_js_data.append(process_helper(item, ct))

        self.context["record"] = record_js_data
        self.context["toolbox"] = toolbox_js_data
        self.context["source"] = record
        from order_info import get_order_process
        self.context["ct"] = get_order_process(record, "buyer_change_order")
        return scaffold.view(self, self.session["store"])