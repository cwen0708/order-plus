#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields


class FileStackModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "filename": u"檔案名稱",
            "filestack_url": u"FileStack 網址",
            "storage_url": u"Storage 網址",
            "mimetype": u"mimetype",
            "size": u"檔案大小 ",
            "client": u"來源"
        }
    filename = Fields.BlobKeyProperty()
    filestack_url = Fields.StringProperty()
    storage_url = Fields.StringProperty()
    mimetype = Fields.StringProperty()
    size = Fields.StringProperty()
    client = Fields.StringProperty()

    @classmethod
    def all_by_created(cls):
        return cls.query().order(-cls.created)
