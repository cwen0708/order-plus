#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields
from web_menu_self_referential_model import WebMenuModel as WMM


class WebMenuModel(BasicModel):
    class Meta:
        label_name = {
            "title": u"通用名稱",
            "name": u"識別碼",
            "title_lang_zhtw": u"繁中名稱",
            "title_lang_zhcn": u"簡中名稱",
            "title_lang_enus": u"英文名稱",
            "page_url": u"網址",
            "category": u"分類",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(required=True)
    name = Fields.StringProperty()
    title_lang_zhtw = Fields.StringProperty(default=u"未命名")
    title_lang_zhcn = Fields.StringProperty(default=u"未命名")
    title_lang_enus = Fields.StringProperty(default=u"未命名")
    page_url = Fields.StringProperty(required=True)
    is_enable = Fields.BooleanProperty(default=True)
    category = Fields.CategoryProperty(kind=WMM)

    @classmethod
    def get_by_url(cls, url, *args, **kwargs):
        return cls.query(cls.page_url==url)

    @classmethod
    def get_title(cls, url, *args, **kwargs):
        item_q = cls.get_by_url(url)
        item = item_q.get()
        if item is None:
            return ""
        if "lang" in kwargs:
            if kwargs["lang"] == "zhtw":
                return item.title_lang_zhtw
            if kwargs["lang"] == "zhcn":
                return item.title_lang_zhcn
            if kwargs["lang"] == "enus":
                return item.title_lang_enus
        return item.title

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name==name).get()

    @classmethod
    def all_enable(cls, category=None, *args, **kwargs):
        cat = None
        if category:
            cat = cls.get_by_name(category)
        if cat is None:
            return cls.query(cls.category==None, cls.is_enable==True).order(-cls.sort)
        else:
            return cls.query(cls.category==cat.key, cls.is_enable==True).order(-cls.sort)
