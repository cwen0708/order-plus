#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from monkey import datastore
from .models.web_menu_model import WebMenuModel

datastore.register("WebMenu", WebMenuModel.all_enable)
datastore.register("WebMenu", WebMenuModel.get_title)


plugins_helper = {
    "title": u"網站選單",
    "desc": u"提供多層的連結選單",
    "plugins_controller": "web_menu"
}


web_menu_action_helper = {
    "group": u"網站選單",
    "actions": [
        {"action": "list", "name": u"網站選單管理"},
        {"action": "add", "name": u"新增網站選單"},
        {"action": "edit", "name": u"編輯網站選單"},
        {"action": "view", "name": u"檢視網站選單"},
        {"action": "delete", "name": u"刪除網站選單"},
        {"action": "plugins_check", "name": u"啟用停用模組"},
    ]
}
