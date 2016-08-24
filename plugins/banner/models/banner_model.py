#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields
from banner_category_model import BannerCategoryModel


class BannerModel(BasicModel):
    class Meta:
        label_name = {
            "name": u"名稱",
            "description": u"描述",
            "link": u"連結網址",
            "link_title": u"連結標題",
            "image": u"圖片",
            "is_enable": u"啟用",
            "category": u"分類",
        }
    name = Fields.StringProperty()
    description = Fields.TextProperty()
    link = Fields.StringProperty()
    link_title = Fields.StringProperty()
    image = Fields.ImageProperty()
    is_enable = Fields.BooleanProperty(default=True)
    category = Fields.CategoryProperty(required=True, kind=BannerCategoryModel)

    @classmethod
    def all_enable(cls, category=None, *args, **kwargs):
        cat = None
        if category:
            cat = BannerCategoryModel.get_by_name(category)
        if cat is None:
            return cls.query(cls.is_enable==True).order(-cls.sort)
        else:
            return cls.query(cls.category==cat.key, cls.is_enable==True).order(-cls.sort)
