#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, route, route_with, controllers, settings


class FlashMessages(Controller):
    @route_with("/admin/flash_message/get_messages.json")
    def get_messages(self):
        self.meta.change_view('json')
        if "__flash" in self.session:
            j = self.session["__flash"]
        else:
            j = {}
        jk = j.keys()
        jk.sort(reverse=True)
        nk = {}
        try:
            message_timeout = float(settings.get("application").get("message_timeout"))
        except:
            message_timeout = 28800.0
        import time
        t = time.time() - message_timeout
        for key in jk:
            if float(key) > t:
                nk[key] = j[key]
        if nk is not {}:
            self.session["__flash"] = nk
        self.context["data"]= nk

    @route_with("/admin/flash_message/clean")
    def clean_messages(self):
        self.session["__flash"] = {}
        return "clean"
