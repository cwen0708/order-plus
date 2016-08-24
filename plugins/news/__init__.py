#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import datastore
from models.news_model import NewsModel
datastore.register("News", NewsModel.all_enable)

plugins_helper = {
    "title": u"最新消息模組",
    "desc": u"最新消息與其分類",
    "plugins_controller": "news,news_category"
}


news_action_helper = {
    "group": u"最新消息",
    "actions": [
        {"action": "list", "name": u"最新消息"},
        {"action": "add", "name": u"新增最新消息"},
        {"action": "edit", "name": u"編輯最新消息"},
        {"action": "view", "name": u"檢視最新消息"},
        {"action": "delete", "name": u"刪除最新消息"},
        {"action": "plugins_check", "name": u"啟用停用模組"},
    ],
    "related_action": "news_category"
}

news_category_action_helper = {
    "group": u"最新消息分類",
    "actions": [
        {"action": "list", "name": u"最新消息分類"},
        {"action": "add", "name": u"新增最新消息分類"},
        {"action": "edit", "name": u"編輯最新消息分類"},
        {"action": "view", "name": u"檢視最新消息分類"},
        {"action": "delete", "name": u"刪除最新消息分類"},
    ]
}
