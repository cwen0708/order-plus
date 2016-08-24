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
import logging


process_main_collection = [
    "process_main",
    "process_normal",
    "process_pre_order",

    "process_order_check",
    "process_order_end",
    "process_order_change",
    "process_order_cancel",
    "process_send_goods",
    "process_return_goods",
    "process_payment",
    "process_refund"
]


def in_process_collection(process_name):
    return process_name in process_main_collection


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
        process_list = {
            "process_main":              {"title": u"主流程",   "desc": u"每筆訂單的起始流程，由此流程決定訂單分發之哪一個子流程" },
            "process_normal":            {"title": u"一般流程", "desc": u"一般的商品購買流程" },
            "process_pre_order":         {"title": u"預購流程", "desc": u"若為團購項目，則轉至此流程" },

            "process_order_check":       {"title": u"訂單確認", "desc": u"與買家進行訂單的數量、金額、運費等項目之確認" },
            "process_payment":           {"title": u"金流收取", "desc": u"向買家進行收款" },
            "process_send_goods":        {"title": u"貨品寄送", "desc": u"於商品撿貨後觸發"},
            "process_order_end":         {"title": u"訂單結束", "desc": u""},
            "process_order_change":      {"title": u"訂單修改", "desc": u""},
            "process_order_cancel":      {"title": u"訂單取消", "desc": u""},
            "process_return_goods":      {"title": u"退貨處理", "desc": u""},
            "process_refund":            {"title": u"金流退款", "desc": u""},

            "jump_process_main":         {"title": u"回到流程",      "desc": u"每筆訂單的起始流程，由此流程決定訂單分發之哪一個子流程"},
            "jump_process_normal":       {"title": u"跳至 一般流程", "desc": u"一般的商品購買流程"},
            "jump_process_pre_order":    {"title": u"跳至 預購流程", "desc": u"若為團購項目，則轉至此流程"},
            "jump_process_order_check":  {"title": u"跳至 訂單確認", "desc": u"與買家進行訂單的數量、金額、運費等項目之確認"},
            "jump_process_payment":      {"title": u"跳至 金流收取", "desc": u"向買家進行收款"},
            "jump_process_send_goods":   {"title": u"跳至 貨品寄送", "desc": u""},
            "jump_process_order_end":    {"title": u"跳至 訂單結束", "desc": u""},
            "jump_process_order_change": {"title": u"跳至 訂單修改", "desc": u""},
            "jump_process_order_cancel": {"title": u"跳至 訂單取消", "desc": u""},
            "jump_process_return_goods": {"title": u"跳至 退貨處理", "desc": u""},
            "jump_process_refund":       {"title": u"跳至 金流退款", "desc": u""},
            
            "process_seller_check":      {"title": u"賣家確認訂單",        "desc": u""},
            "process_buyer_check":       {"title": u"買家確認訂單",        "desc": u""},
            "lock_order_change":         {"title": u"停用買家訂單修改流程", "desc": u""},
            "lock_order_cancel":         {"title": u"停用買家消取訂單流程", "desc": u""},

            "set_order_status_unconfirmed": {"title": u"設定訂單狀態為未確認", "desc": u""},
            "set_order_status_pending":     {"title": u"設定訂單狀態為待處理", "desc": u""},
            "set_order_status_need_check":  {"title": u"設定訂單狀態為需確認", "desc": u""},
            "set_order_status_processing":  {"title": u"設定訂單狀態為處理中", "desc": u""},
            "set_order_status_complete":    {"title": u"設定訂單狀態為已完成", "desc": u""},
            "set_order_status_cancelled":   {"title": u"設定訂單狀態為已取消", "desc": u""},
            "set_cash_flow_unconfirmed":    {"title": u"設定金流狀態為未確認", "desc": u""},
            "set_cash_flow_pending":        {"title": u"設定金流狀態為待付款", "desc": u""},
            "set_cash_flow_reconciliation": {"title": u"設定金流狀態為對帳中", "desc": u""},
            "set_cash_flow_receivables":    {"title": u"設定金流狀態為已收款", "desc": u""},
            "set_freight_flow_unconfirmed": {"title": u"設定物流狀態為未確認", "desc": u""},
            "set_freight_flow_stocking":    {"title": u"設定物流狀態為備貨中", "desc": u""},
            "set_freight_flow_restock":     {"title": u"設定物流狀態為補貨中", "desc": u""},
            "set_freight_flow_need_send":   {"title": u"設定物流狀態為待發貨", "desc": u""},
            "set_freight_flow_shipped":     {"title": u"設定物流狀態為已發貨", "desc": u""},
            "set_freight_flow_arrived":     {"title": u"設定物流狀態為已到貨", "desc": u""},


            "if_order_unconfirmed":         {"title": u"如果 訂單 未確認", "desc": u""},
            "if_has_group":                 {"title": u"如果 包含 團購的訂單", "desc": u""},
            "if_cash_flow_pending":         {"title": u"如果 金流 已付款",     "desc": u""},
        }

    @staticmethod
    def unique_process(check_list, target):
        target_list = []
        for tools_item in target:
            if tools_item["id"] not in check_list:
                target_list.append(tools_item)
                check_list.append(tools_item["id"])
        return target_list

    def get_name(self, process):
        return self.meta.process_list[process]["title"]

    def add_name(self, process):
        process_list = self.meta.process_list
        for item in process:
            item_id = item["id"]
            if item_id not in process_list:
                continue
            item["title"] = process_list[item_id]["title"]
            item["desc"] = process_list[item_id]["desc"]
            item["bg"] = u""
            if item["id"].find("if") >= 0:
                item["bg"] = "bg-blue-100"
            if item["id"].find("jump") >= 0:
                item["bg"] = "bg-green-100"
            if item_id in process_main_collection:
                item["can_edit"] = True
            else:
                item["can_edit"] = False
            if "children" in item:
                item["children"] = self.add_name(item["children"])
        return process

    @route_with("/console/store/process")
    def index(self):
        store = self.Util.decode_key(self.session["store"]).get()
        menu = []
        for item in process_main_collection:
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
            "process_normal": [
                {"id": "process_seller_check"},
            ],
            "process_pre_order": [
                {"id": "process_seller_check"},
            ],
            "process_order_check": [
                {"id": "process_seller_check"},
                {"id": "lock_order_change"},
                {"id": "lock_order_cancel"},
                {"id": "lock_return_goods"},
            ],
            "process_payment": [
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
            "status": [
                {"id": "set_order_status_unconfirmed"},
                {"id": "set_order_status_pending"},
                {"id": "set_order_status_processing"},
                {"id": "set_order_status_complete"},
                {"id": "set_order_status_cancelled"},

                {"id": "set_cash_flow_unconfirmed"},
                {"id": "set_cash_flow_pending"},
                {"id": "set_cash_flow_reconciliation"},
                {"id": "set_cash_flow_receivables"},

                {"id": "set_freight_flow_unconfirmed"},
                {"id": "set_freight_flow_stocking"},
                {"id": "set_freight_flow_restock"},
                {"id": "set_freight_flow_shipped"},
                {"id": "set_freight_flow_arrived"},
            ],
            "if": [
                {"id": "if_order_unconfirmed"},
                {"id": "if_has_group"},
                {"id": "if_cash_flow_pending"},
            ],
            "jump": []
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

        process_collection = []
        for item in process_main_collection:
            process_collection.append({
                "id": item,
            })
            tools["jump"].append({
                "id": "jump_" + item,
            })

        check_list = []
        for target_item in record_list:
            check_list.append(target_item["id"])
            if "children" in target_item:
                for sub_item in target_item["children"]:
                    check_list.append(sub_item["id"])

        self.context["page_id"] = target
        self.context["page_name"] = self.get_name(target)
        self.context["record"] = self.add_name(record_list)
        self.context["process_collection"] = self.add_name(process_collection)
        self.context["toolbox"] = self.add_name(self.unique_process(check_list, tools[target]))
        self.context["toolbox_status"] = self.add_name(self.unique_process(check_list, tools["status"]))
        self.context["toolbox_if"] = self.add_name(self.unique_process(check_list, tools["if"]))
        self.context["toolbox_jump"] = self.add_name(self.unique_process(check_list, tools["jump"]))
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
