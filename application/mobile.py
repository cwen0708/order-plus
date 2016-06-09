#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey import BasicModel
from monkey.behaviors.searchable import Searchable
from monkey import Fields
from application.store import StoreModel
from application.user_info import UserInfoModel


def get_or_create_mobile(number, name=u"未命名使用者", store_name=u"未命名店家"):
    return MobileModel.get_or_create_by_number(number, name, store_name)


def get_mobile(number):
    return MobileModel.get_by_number(number)


class MobileModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "number": u"電話",
            "code": u"驗証碼",
            "password": u"密碼",
            "store": u"所屬商家",
            "is_enable": u"啟用/停用",
        }
        hide_filed = ["account", "store"]
    number = Fields.StringProperty(required=True)
    code = Fields.StringProperty()
    password = Fields.StringProperty()
    store = Fields.CategoryProperty(kind=StoreModel)
    account = Fields.CategoryProperty(kind=UserInfoModel)
    is_enable = Fields.BooleanProperty(default=True)

    @classmethod
    def format_mobile_number(cls, value=u''):
        """
        處理手機格式
        :param value: 輸入值
        :param taiwan_format: 台灣手機
        :return: 正確的手機格式 或 None
        """
        if value.startswith("09") is True:
            if len(value) == 10:
                return "+886" + value[1:]
        if value.startswith("+886") is True:
            if len(value) == 13:
                return value
        return None
    
    @classmethod
    def get_by_number(cls, number):
        return cls.query(cls.number == number).get()

    @classmethod
    def get_or_create_by_number(cls, number, name=u"未命名使用者", store_name=u"未命名店家"):
        number = cls.format_mobile_number(number)
        if number is None:
            raise u"手機格式有誤"
        mobile = cls.get_by_number(number)

        if mobile is None:
            mobile = MobileModel()
            mobile.number = number
            mobile.put()
        if mobile.store is None:
            s = StoreModel()
            s.title = store_name
            s.process_main = '[{"id":"process_order_check"},{"id":"process_payment"},{"id":"process_send_goods"},{"id":"process_order_end"}]'
            s.put()
            mobile.store = s.key
            mobile.put()
        if mobile.account is None:
            a = UserInfoModel()
            a.user_name = name
            a.put()
            mobile.account = a.key
            mobile.put()
        return mobile

    @classmethod
    def already_register_check_and_login(cls, mobile, code):
        r = cls.query(cls.number == mobile, cls.password == code).get()
        if r is None:
            r = cls.query(cls.number == mobile, cls.code == code).get()
            if r is None:
                return None
        return r

    @classmethod
    def all_enable(cls):
        return cls.query(cls.is_enable == True).order(-cls.sort)

    @classmethod
    def all_enable_with_category(cls, cat):
        return cls.query(cls.is_enable == True, cls.store == cat.key).order(-cls.sort)

    @classmethod
    def get_prev_one_with_enable(cls, item):
        return cls.query(cls.is_enable == True, cls.sort > item.sort).order(cls.sort).get()

    @classmethod
    def get_next_one_with_enable(cls, item):
        return cls.query(cls.is_enable == True, cls.sort < item.sort).order(-cls.sort).get()


class Mobile(Controller):
    class Meta:
        title = u"電話"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20