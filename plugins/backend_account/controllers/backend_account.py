#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.


from monkey import Controller, scaffold, route_menu, route_with


class BackendAccount(Controller):
    class Meta:
        scaffold_title = {
            "list": u"帳號設定",
            "add": u"新增管理帳號",
            "edit": u"編輯管理帳號",
            "view": u"檢視管理帳號",
        }
        components = (scaffold.Scaffolding,)

    @route_menu(list_name=u"backend", text=u"帳號設定", sort=9999, group=u"設定")
    @route_with("/admin/backend_account/list")
    def admin_list(self):
        return scaffold.list(self)


