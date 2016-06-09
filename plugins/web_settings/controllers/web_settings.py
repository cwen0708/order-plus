#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

import monkey
from plugins.settings.models.setting import Setting
import datetime
from ..models.web_setting import WebSetting
from google.appengine.api import memcache


class WebSettings(monkey.Controller):
    class Meta:
        title = u"網站設定"
        components = (monkey.scaffold.Scaffolding,)
        Model = WebSetting

    def startup(self):
        self.context['setting_classes'] = WebSetting.get_classes()

    def admin_list(self):
        self.context['page_title'] = u"網站設定"
        self.context['settings'] = monkey.settings.settings()

    def admin_edit(self, key, *args):
        model = Setting.factory(key)
        instance = model.get_instance(static_settings=monkey.settings.settings())

        self.meta.Model = model
        self.scaffold.ModelForm = monkey.model_form(model)

        self.context['settings_class'] = model

        def reload_settings(**kwargs):
            self.scaffold.redirect = False
            self.components.flash_messages(u'設定已被儲存，不過，有些應用程實例可能正在執行中，您可能無法立即查看到變動後的設定。', 'warning')

        self.events.scaffold_after_save += reload_settings
        return monkey.scaffold.edit(self, instance.key.urlsafe())
