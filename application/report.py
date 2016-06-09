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


class ReportModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"摘要",
        }
    title = Fields.StringProperty(default=u"未命名")


class Report(Controller):
    class Meta:
        title = u"銷售統計"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 20
