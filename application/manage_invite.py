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
from monkey import Fields, route_with
from mobile import MobileModel
from user_info import UserInfoModel
from store import StoreModel


class ManageInviteModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團購名稱",
            "store": u"商家",
        }
    inviter = Fields.CategoryProperty(kind=UserInfoModel)
    invitee_mobile = Fields.CategoryProperty(kind=MobileModel)
    store = Fields.CategoryProperty(kind=StoreModel)


class ManageInvite(Controller):
    class Meta:
        title = u"管理者邀請"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20
