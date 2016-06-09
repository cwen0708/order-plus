#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields


class WebFileModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "a22": u"分類",
            "title": u"標題",
            "title_en": u"英文標題",
            "page_url": u"頁面網址",
            "is_enable": u"顯示於前台",
            "content": u"內容 "
        }
    file = Fields.BlobKeyProperty()
    file_cloud_storage = Fields.StringProperty()

    @classmethod
    def all_by_created(cls):
        return cls.query().order(-cls.created)
