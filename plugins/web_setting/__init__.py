#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

plugins_helper = {
    "title": u"系統設定值",
    "desc": u"請謹慎更改此模組的相關設置",
    "plugins_controller": "web_setting"
}


web_setting_action_helper = {
    "group": u"網站設定",
    "actions": [
        {"action": "list", "name": u"網站設定管理"},
        {"action": "add", "name": u"新增網站設定"},
        {"action": "edit", "name": u"編輯網站設定"},
        {"action": "view", "name": u"檢視網站設定"},
        {"action": "delete", "name": u"刪除網站設定"},
        {"action": "plugins_check", "name": u"啟用停用模組"},
    ]
}