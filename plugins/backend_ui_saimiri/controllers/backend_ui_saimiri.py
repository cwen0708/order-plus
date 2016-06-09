#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, route, route_with, controllers, settings


class BackendUiSaimiri(Controller):
    @route_with("/admin/")
    @route_with("/admin")
    def root(self):
        try:
            admin_user = self.session["administrator_name"]
        except KeyError:
            return self.redirect(self.uri('backend_ui_saimiri:login'))
        if admin_user is None:
            return self.redirect(self.uri('backend_ui_saimiri:login'))
        import datetime
        self.context["now"] = datetime.datetime.now()
        menus = self.util.get_menu("backend")
        try:
            self.context["backend_title"] = settings.get("application").get("name")
        except:
            self.context["backend_title"] = u"網站後台"
        self.context["controllers"] = controllers
        self.context["menus"] = menus
        self.context["backend_version"] = "0.2.1"

    @route_with("/admin/aa")
    def admin_aa(self):
        self.session["advanced_admin"] = True
        self.session["administrator_name"] = "WOW"
        return self.redirect("/admin")

    @route_with("/admin/jump_to_login")
    def jump_to_login(self):
        pass

    @route_with("/admin/login")
    def login(self):
        try:
            self.context["backend_title"] = settings.get("application").get("name")
        except:
            self.context["backend_title"] = u"網站後台"

    @route_with("/admin/login.json")
    def login_json(self):
        self.meta.change_view('json')
        self.context['data'] = {
            'is_login': u'false'
        }
        if self.request.method != "POST":
            return
        from plugins.backend_account import login, has_record, create_account
        input_account = self.params.get_string("account")
        input_password = self.params.get_string("password")
        administrator = login(input_account, input_password)
        if administrator is None:
            if has_record():
                return
            s = settings.get("plugins").get("backend_account_administrator")
            default_name = s.get("name")
            default_account = s.get("account")
            default_password = s.get("password")
            default_level = s.get("level")
            create_account(default_name, default_account, default_password, default_level)
            if default_account != input_account or default_password != input_password:
                return
            self.session["administrator_name"] = s.get("name")
            self.session["administrator_access_level"] = default_level
        else:
            self.session["administrator_name"] = administrator.account
            self.session["administrator_access_level"] = administrator.access_level
        self.context['data'] = {
            'is_login': 'true'
        }

    @route_with("/admin/logout")
    def logout(self):
        self.session["account"] = None
        self.session["already_login"] = False
        self.session["administrator_name"] = None
        return self.redirect("/admin/login")

