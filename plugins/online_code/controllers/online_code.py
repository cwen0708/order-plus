#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/3/3

from monkey import settings, Pagination
from monkey import Controller, route_with, route, controllers
from monkey.core.gaeforms import model_form
from plugins.web_page.models.web_page_model import WebPageModel
import datetime
from ..models.online_code_model import OnlineCodeModel
from ..models.online_code_target_model import OnlineCodeTargetModel
from monkey import auth, add_authorizations
from time import time


class OnlineCode(Controller):
    class Meta:
        Model = OnlineCodeModel

    @route_with('/code/')
    @route_with('/code/<target_name>/edit.html')
    @add_authorizations(auth.require_admin)
    def index(self, target_name=None):
        self.context["body_class"] = "show_list"
        if target_name is None:
            self.context["list"] = OnlineCodeTargetModel.all()
            return

        n = OnlineCodeTargetModel.get_by_name(target_name)
        if n is None:
            n = OnlineCodeTargetModel()
            n.title = target_name
            n.put()
        self.context["body_class"] = "show_record"
        self.context["list"] = [n]


    @route_with('/code/welcome.html')
    @add_authorizations(auth.require_admin)
    def welcome(self):
        pass

    @route_with('/code/records.html')
    @add_authorizations(auth.require_admin)
    def records(self):
        target = self.params.get_ndb_record("target")
        file_type = self.params.get_string("file_type")
        records = self.meta.Model.all_with_target(target, file_type)

        self.context["target"] = target
        self.context["target_key"] = self.params.get_string("target")
        self.context["records"] = records.fetch(50)
        self.context["file_type"] = self.params.get_string("file_type")
        self.context["has_record"] = False
        if records.get() is not None:
            self.context["has_record"] = True

    @route_with('/code/editor.html')
    @add_authorizations(auth.require_admin)
    def editor(self):
        self.context["target"] = self.params.get_string("target")
        self.context["file_type"] = self.params.get_string("file_type")
        self.context["record_key"] = self.params.get_string("record_key")
        self.context["record"] = self.params.get_ndb_record("record_key")

    @route_with('/code/save.json')
    @add_authorizations(auth.require_admin)
    def save_json(self):
        self.meta.change_view("json")
        code = self.params.get_string("code")
        target = self.params.get_ndb_record("target")
        file_type = self.params.get_string("file_type")
        source_minify = u""
        vision = int(time()) - 1460000000
        if file_type == "javascript":
            target.js_vision = vision
        elif file_type == "css":
            target.css_vision = vision
        elif file_type == "html":
            target.html_vision = vision
        else:
            self.context["data"] = {"error": "Wrong File Type"}
            return
        target.put()

        n = self.meta.Model()
        n.title = u" 版本 " + str(vision)
        n.source = code
        n.vision = vision
        n.code_type = file_type
        n.target = target.key
        n.put()
        self.context["data"] = {"info": "done"}

    @route_with('/code/get_<target_name>_info.json')
    def info(self, target_name):
        import os
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        target = OnlineCodeTargetModel.get_by_name(target_name)
        self.context['data'] = {
            'content': target.title,
            'js-vision': target.js_vision,
            'css-vision': target.css_vision,
            'html-vision': target.html_vision,
            'vision': os.environ['CURRENT_VERSION_ID']
        }

    @route_with('/code/get_<target_name>_<vision>.html')
    def js(self, target_name, vision):
        c = OnlineCodeTargetModel.get_by_name(target_name)
        s = self.meta.Model.get_source(target=c, code_type="html", vision=vision)
        source = u""
        if s is not None:
            source = s.source
        self.context["record"] = {
            "source": source,
            "vision": vision
        }

    @route_with('/code/get_<target_name>_<vision>.js')
    def js(self, target_name, vision):
        self.response.headers['Content-Type'] = 'text/javascript'
        self.response.headers["Cache-control"] = "public, max-age=604800"
        self.meta.change_view('render')
        c = OnlineCodeTargetModel.get_by_name(target_name)
        s = self.meta.Model.get_source(target=c, code_type="javascript", vision=vision)
        source = u""
        if s is not None:
            source = s.source
        self.context["record"] = {
            "target_name": target_name,
            "source": source,
            "vision": vision
        }

    @route_with('/code/get_<target_name>_<vision>.css')
    def css(self, target_name, vision):
        self.response.headers['Content-Type'] = 'text/css'
        self.response.headers["Cache-control"] = "public, max-age=604800"
        self.meta.change_view('render')
        c = OnlineCodeTargetModel.get_by_name(target_name)
        s = self.meta.Model.get_source(target=c, code_type="css", vision=vision)
        source = u""
        if s is not None:
            source = s.source
        self.context["record"] = {
            "target_name": target_name,
            "source": source,
            "vision": vision
        }

    @route_with('/admin/online_code/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }