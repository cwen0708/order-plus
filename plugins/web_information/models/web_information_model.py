#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import BasicModel
from monkey import Fields


class WebInformationModel(BasicModel):
    class Meta:
        label_name = {
            "title": u"通用名稱",
            "name": u"識別碼",
            "domain_registration": u"網域註冊地",
            "domain_registration_price": u"網域註冊費用",
            "domain_registration_date": u"網域註冊日",
            "domain_expiration_date": u"網域到期日",
            "space_rental_level": u"伺服器等級",
            "space_rental_price": u"空間費用",
            "space_rental_date": u"空間租借日",
            "space_expiration_date": u"空間到期日",
            
            "manager_company": u"管理公司",
            "manager_website": u"公司網址",
            "manager_person": u"管理人姓名",
            "manager_telephone": u"管理人電話",
            "manager_mobile": u"管理人手機",
            "manager_email": u"管理人信箱",

            "contact_person": u"聯絡人",
            "contact_telephone": u"聯絡電話",
            "contact_mobile": u"聯絡手機",
            "contact_email": u"聯絡信箱",
            "contact_address": u"聯絡地址",
            "is_enable": u"顯示於前台",
        }
    title = Fields.StringProperty(required=True)
    name = Fields.StringProperty()

    domain_registration = Fields.StringProperty()
    domain_registration_price = Fields.StringProperty()
    domain_registration_date = Fields.DateProperty()
    domain_expiration_date = Fields.DateProperty()
    space_rental_level = Fields.StringProperty()
    space_rental_price = Fields.StringProperty()
    space_rental_date = Fields.DateProperty()
    space_expiration_date = Fields.DateProperty()

    manager_company = Fields.StringProperty(default=u"侑良科技")
    manager_website = Fields.StringProperty(default="http://")
    manager_person = Fields.StringProperty()
    manager_telephone = Fields.StringProperty()
    manager_mobile = Fields.StringProperty()
    manager_email = Fields.StringProperty()

    contact_person = Fields.StringProperty()
    contact_telephone = Fields.StringProperty()
    contact_mobile = Fields.StringProperty()
    contact_email = Fields.StringProperty()
    contact_address = Fields.StringProperty()
    is_enable = Fields.BooleanProperty(default=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name==name).get()
