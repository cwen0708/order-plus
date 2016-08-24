#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields
from news_category_model import NewsCategoryModel


class NewsModel(BasicModel):
    class Meta:
        label_name = {
            "name": u"名稱",
            "date": u"日期",
            "is_enable": u"啟用",
            "category": u"分類",
            "title_lang_zhtw": u"繁體中文標題",
            "title_lang_zhcn": u"簡體中文標題",
            "title_lang_enus": u"英文標題",
            "content_lang_zhtw": u"繁體中文內容",
            "content_lang_zhcn": u"簡體中文內容",
            "content_lang_enus": u"英文內容",
        }
    name = Fields.StringProperty(required=True)
    date = Fields.DateProperty()
    is_enable = Fields.BooleanProperty(default=True)
    # category = Fields.CategoryProperty(kind=NewsCategoryModel)
    title_lang_zhtw = Fields.StringProperty()
    title_lang_zhcn = Fields.StringProperty()
    title_lang_enus = Fields.StringProperty()
    content_lang_zhtw = Fields.RichTextProperty()
    content_lang_zhcn = Fields.RichTextProperty()
    content_lang_enus = Fields.RichTextProperty()

    @classmethod
    def all_enable(cls, category=None, *args, **kwargs):
        cat = None
        if hasattr(cls, "category"):
            if category:
                cat = NewsCategoryModel.get_by_name(category)
            if cat is not None:
                return cls.query(cls.category == cat.key, cls.is_enable==True).order(-cls.sort)
        return cls.query(cls.is_enable==True).order(-cls.sort)
