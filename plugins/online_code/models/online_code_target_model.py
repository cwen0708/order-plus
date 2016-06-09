#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu, Fields, route_with
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey import BasicModel
from monkey.behaviors.searchable import Searchable


class OnlineCodeTargetModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"目標名稱",
            "url": u"網址",
            "is_enable": u"顯示於前台",
            "telephone": u"連絡方式",
            "image": u"照片",
            "content": u"簡介",
        }
    title = Fields.StringProperty(default=u"未命名")
    js_vision = Fields.IntegerProperty(default=0)
    css_vision = Fields.IntegerProperty(default=0)
    html_vision = Fields.IntegerProperty(default=0)

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.title==name).get()
