#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold
from plugins.settings.models.setting import Setting
import datetime
from google.appengine.api import memcache


class WebPage(Controller):
    class Meta:
        title = u"網站頁面"
        components = (scaffold.Scaffolding,)