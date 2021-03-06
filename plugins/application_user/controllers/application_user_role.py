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
from .. import application_user_role_action_helper


class ApplicationUserRole(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        pagination_actions = ("list",)
        pagination_limit = 50

    class Scaffold:
        title = application_user_role_action_helper["actions"]
        display_properties = ("title", "name", "level", "is_enable", "sort", "created", "modified")
        display_properties_in_list = ("title", "name", "level")

    @route_with('/admin/application_user_role/permissions_set.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        role = self.params.get_ndb_record("role_key")
        if not role:
            return self.error(403)
        if self.administrator.role.get().level < role.level:
            return self.error(403)
        uri = self.params.get_string("uri", '')
        enable = self.params.get_string("enable", 'enable')
        if uri is '':
            return self.error(404)
        role_prohibited_actions_list = str(role.prohibited_actions).split(",")
        if enable == u"true":
            if uri in role_prohibited_actions_list:
                role_prohibited_actions_list.remove(uri)
            msg = u"已啟用"
        else:
            if uri not in role_prohibited_actions_list:
                role_prohibited_actions_list.append(uri)
            msg = u"已停用"
        s = ",".join(role_prohibited_actions_list)
        role.prohibited_actions = s
        role.put()
        self.context['data'] = {
            'info': "done",
            'msg': msg
        }

    @route_with('/admin/application_user_role/:<key>/permissions')
    def admin_action_permissions(self, key):
        def process_item(model, item, action):
            for act in item["actions"]:
                uri = "admin:%s:%s" % (model, act["action"])
                act["uri"] = uri
                act["checkbox_id"] = "admin-%s-%s" % (model, act["action"])
                if act["uri"] in action:
                    act["enable"] = False
                else:
                    act["enable"] = True
            return item

        role = self.util.decode_key(key).get()
        if self.administrator_level < role.level:
            return self.abort(403)
        action_list = []
        role_prohibited_actions = role.prohibited_actions
        all_plugins = set(self.plugins_all) & set(self.plugins)
        for item in all_plugins:
            module_path = 'plugins.%s' % item
            try:
                module = __import__('%s' % module_path, fromlist=['*'])
                cls = getattr(module, '%s_action_helper' % item)
                action_list.append(process_item(item, cls, role_prohibited_actions))
                if "related_action" in cls:
                    related_action_list = cls["related_action"].split(",")
                    for ra_item in related_action_list:
                        related_cls = getattr(module, '%s_action_helper' % ra_item)
                        action_list.append(process_item(cls["related_action"], related_cls, role_prohibited_actions))
            except:
                pass
        module_path = 'application'
        module = __import__('%s' % module_path, fromlist=['*'])
        for item in all_plugins:
            try:
                cls = getattr(module, '%s_action_helper' % item)
                action_list.append(process_item(item, cls, role_prohibited_actions))
            except:
                pass

        self.context["item"] = role
        self.context["item_key"] = key
        self.context["application_user_role"] = action_list

    @route_menu(list_name=u"backend", text=u"角色管理", sort=9701, icon="users", group=u"帳號管理")
    @route_with("/admin/application_user_role/list")
    def admin_list(self):
        self.context["administrator_role"] = self.administrator.role
        return scaffold.list(self)

    @csrf_protect
    def admin_add(self):
        def scaffold_before_validate(**kwargs):
            parser = kwargs["parser"]
            change_level = self.params.get_integer("level")
            def validate():
                if self.administrator_level < change_level:
                    parser.errors["level"] = u"您的權限等級 (%s) 低於設定值 (%s)，您無法設置比您高等級的值" % (self.administrator_level, change_level)
                    return False
                return parser.container.validate() if parser.container else False
            parser.validate = validate

        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.add(self)

    @csrf_protect
    def admin_edit(self, key, *args):
        target = self.util.decode_key(key).get()
        target_level = target.level
        if self.administrator_level < target_level:
            return self.abort(403)

        def scaffold_before_validate(**kwargs):
            parser = kwargs["parser"]
            change_level = self.params.get_integer("level")
            def validate():
                if self.administrator_level < target_level:
                    parser.errors["level"] = u"您的權限等級 (%s) 低於目標值 (%s)，您無法設置比您高等級的角色" % (self.administrator_level, target_level)
                    return False
                if self.administrator_level < change_level:
                    parser.errors["level"] = u"您的權限等級 (%s) 低於設定值 (%s)，您無法設置比您高等級的值" % (self.administrator_level, change_level)
                    return False
                if change_level > 1000 < self.administrator_level and target_level != 9999:
                    parser.errors["level"] = u"權限等級最高為 999"
                    return False
                if target_level == 9999 and change_level != 9999:
                    parser.errors["level"] = u"此權限等級無法變更"
                    return False
                return parser.container.validate() if parser.container else False
            parser.validate = validate

        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.edit(self, key)

    def admin_view(self, key):
        return scaffold.view(self, key)

    def admin_delete(self, key):
        target = self.util.decode_key(key).get()
        target_level = target.level
        if self.administrator_level< target_level:
            return self.abort(403)
        return scaffold.delete(self, key)
