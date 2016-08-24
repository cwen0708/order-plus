#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields


class BannerCategoryModel(BasicModel):
    class Meta:
        label_name = {
            "name": u"識別名稱",
            "title": u"分類標題",
            "is_enable": u"啟用",
        }
    name = Fields.StringProperty()
    title = Fields.StringProperty()
    is_enable = Fields.BooleanProperty(default=True)


    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name==name).get()

    @classmethod
    def all_enable(cls):
        return cls.query(cls.is_enable==True).order(-cls.sort)