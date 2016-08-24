#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

plugins_helper = {
    "title": u"網站資訊管理",
    "desc": u"伺服器相關資訊",
    "plugins_controller": "web_information"
}


web_information_action_helper = {
    "group": u"網站資訊",
    "actions": [
        {"action": "list", "name": u"網站資訊管理"},
        {"action": "add", "name": u"新增網站資訊"},
        {"action": "edit", "name": u"編輯網站資訊"},
        {"action": "view", "name": u"檢視網站資訊"},
        {"action": "delete", "name": u"刪除網站資訊"},
        {"action": "plugins_check", "name": u"啟用停用模組"},
    ]
}