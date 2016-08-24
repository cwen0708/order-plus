#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/07/08.

from monkey import datastore
from models.banner_model import BannerModel
from models.banner_model import BannerCategoryModel

datastore.register("Banner", BannerModel.all_enable)

plugins_helper = {
    "title": u"輪撥圖",
    "desc": u"請謹慎更改此模組的相關設置",
    "plugins_controller": "banner,banner_category"
}


banner_action_helper = {
    "group": u"輪撥圖",
    "actions": [
        {"action": "list", "name": u"輪撥圖管理"},
        {"action": "add", "name": u"新增輪撥圖"},
        {"action": "edit", "name": u"編輯輪撥圖"},
        {"action": "view", "name": u"檢視輪撥圖"},
        {"action": "delete", "name": u"刪除輪撥圖"},
        {"action": "plugins_check", "name": u"啟用停用模組"},
    ],
    "related_action": "banner_category"
}

banner_category_action_helper = {
    "group": u"輪撥圖分類",
    "actions": [
        {"action": "list", "name": u"輪撥圖分類管理"},
        {"action": "add", "name": u"新增輪撥圖分類"},
        {"action": "edit", "name": u"編輯輪撥圖分類"},
        {"action": "view", "name": u"檢視輪撥圖分類"},
        {"action": "delete", "name": u"刪除輪撥圖分類"},
    ]
}
