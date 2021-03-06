#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from monkey import Controller, scaffold, route_menu, route_with
from monkey.components.pagination import Pagination
from monkey.components.csrf import CSRF, csrf_protect
from monkey.components.search import Search
from .. import application_user_action_helper


class ApplicationUser(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        pagination_actions = ("list",)
        pagination_limit = 50

    class Scaffold:
        title = application_user_action_helper["actions"]
        display_properties = ("name", "account", "is_enable", "sort", "created", "modified")
        display_properties_in_list = ("name", "account")

    @route_menu(list_name=u"backend", text=u"帳號管理", sort=9700, icon="users", group=u"帳號管理")
    @route_with("/admin/application_user/list")
    def admin_list(self):
        self.context["administrator_key"] = self.administrator.key
        scaffold.list(self)
        for item in self.context[self.scaffold.plural]:
            item.level = item.role.get().level

    @csrf_protect
    def admin_add(self):
        def scaffold_before_validate(**kwargs):
            parser = kwargs["parser"]
            change_level = parser.data["role"].get().level
            def validate():
                if change_level > self.administrator_level:
                    parser.errors["role"] = u"您的權限等級低於此角色"
                    return False
                return parser.container.validate() if parser.container else False
            parser.validate = validate
        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.add(self)

    @csrf_protect
    def admin_edit(self, key):
        target = self.util.decode_key(key).get()
        target_level = target.role.get().level
        if self.administrator_level < target_level:
            return self.abort(403)
        def scaffold_before_validate(**kwargs):
            parser = kwargs["parser"]
            change_level = parser.data["role"].get().level
            def validate():
                if  self.administrator_level < change_level:
                    parser.errors["role"] = u"您的權限等級低於此角色"
                    return False
                return parser.container.validate() if parser.container else False
            parser.validate = validate
        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.edit(self, key)

    @csrf_protect
    @route_with("/admin/application_user/profile")
    def admin_profile(self):
        target = self.administrator
        target_level = target.role.get().level
        if self.administrator_level < target_level:
            return self.abort(403)
        def scaffold_before_validate(**kwargs):
            parser = kwargs["parser"]
            change_level = parser.data["role"].get().level
            def validate():
                if  self.administrator_level < change_level:
                    parser.errors["role"] = u"您的權限等級低於此角色"
                    return False
                return parser.container.validate() if parser.container else False
            parser.validate = validate
        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.edit(self, self.administrator.key)

    def admin_delete(self, key):
        target = self.util.decode_key(key).get()
        target_level = target.role.get().level
        if self.administrator_level < target_level:
            return self.abort(403)
        return scaffold.delete(self, key)
