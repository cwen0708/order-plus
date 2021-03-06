#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields


class ApplicationUserRoleModel(BasicModel):
    class Meta:
        label_name = {
            "title": u"角色名稱",
            "name": u"角色識別碼",
            "is_enable": u"啟用",
            "prohibited_actions": u"禁止的操作",
            "level": u"權限等級"
        }
    title = Fields.StringProperty(required=True)
    name = Fields.StringProperty(required=True)
    prohibited_actions = Fields.StringProperty(default="")
    is_enable = Fields.BooleanProperty(default=True)
    level = Fields.IntegerProperty(default=0)

    @classmethod
    def get_role(cls, name):
        a = cls.query(cls.name == name).get()
        return a

    @classmethod
    def has_record(cls):
        r = cls.query().get()
        if r is not None:
            return True
        else:
            return False

    @classmethod
    def create_account(cls, name, account, password, prohibited_actions):
        n = cls()
        n.name = name
        n.account = account
        n.password = password
        n.prohibited_actions = prohibited_actions
        n.put()
        return n

    @classmethod
    def get_list(cls):
        return cls.query(cls.level < 1000).order(cls.level, -cls.sort)