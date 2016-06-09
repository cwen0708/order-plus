#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Searchable
from monkey import Fields


class BackendAccountModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"標題",
            "title_en": u"英文標題",
            "page_url": u"頁面識別碼",
            "is_enable": u"顯示於前台",
            "content": u"內容 "
        }
    name = Fields.StringProperty(required=True)
    account = Fields.StringProperty(required=True)
    password = Fields.StringProperty(required=True)
    access_level = Fields.IntegerProperty(default=999)
    is_enable = Fields.BooleanProperty(default=True)

    @classmethod
    def get_account(cls, account, password, is_enable=True):
        a = cls.query(cls.account == account, cls.password == password,
                      cls.is_enable == is_enable).get()
        return a

    @classmethod
    def has_record(cls):
        r = cls.query().get()
        if r is not None:
            return True
        else:
            return False

    @classmethod
    def create_account(cls, name, account, password, level):
        n = cls()
        n.name = name
        n.account = account
        n.password = password
        n.access_level = level
        n.put()
