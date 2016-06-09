#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Searchable
from monkey import Fields

class WebPageModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"標題",
            "title_en": u"英文標題",
            "page_url": u"頁面識別碼",
            "is_enable": u"顯示於前台",
            "content": u"內容 "
        }
    title = Fields.StringProperty(required=True)
    title_en = Fields.StringProperty(required=True)
    page_url = Fields.StringProperty(required=True)
    is_enable = Fields.BooleanProperty(default=True)
    content = Fields.RichTextProperty()

    @classmethod
    def get_by_url(cls, page_url):
        return cls.query(WebPageModel.page_url== page_url).get()