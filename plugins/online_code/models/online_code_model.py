#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields
from online_code_target_model import OnlineCodeTargetModel


class OnlineCodeModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團體名稱",
            "customer": u"所屬客戶",
            "code_type": u"類型",
            "source": u"原始碼",
        }
    title = Fields.StringProperty(default=u"未命名")
    target = Fields.CategoryProperty(kind=OnlineCodeTargetModel)
    code_type = Fields.StringProperty()
    source = Fields.TextProperty()
    vision = Fields.IntegerProperty(default=0)

    @classmethod
    def all_with_target(cls, target, code_type):
        return cls.query(cls.code_type == code_type, cls.target == target.key).order(-cls.sort)

    @classmethod
    def get_source(cls, target, code_type, vision):
        return cls.query(cls.code_type == code_type, cls.target == target.key, cls.vision == int(vision)).order(-cls.sort).get()