#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields


class NewsCategoryModel(BasicModel):
    class Meta:
        label_name = {
            "name": u"分類識別碼",
            "is_enable": u"啟用",
            "title": u"分類名稱",
            "title_lang_zhtw": u"繁體中文分類名稱",
            "title_lang_zhcn": u"簡體中文分類名稱",
            "title_lang_enus": u"英文分類名稱",
        }
    name = Fields.StringProperty(required=True)
    title = Fields.StringProperty(default=u"未命名")
    title_lang_zhtw = Fields.StringProperty(default=u"未命名")
    title_lang_zhcn = Fields.StringProperty(default=u"未命名")
    title_lang_enus = Fields.StringProperty(default=u"未命名")
    is_enable = Fields.BooleanProperty(default=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name==name).get()