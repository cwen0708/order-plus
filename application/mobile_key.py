#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from monkey import Controller, scaffold, route_menu
from monkey import auth, add_authorizations
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey.behaviors.searchable import Searchable
from monkey import Fields, route_with
from monkey import BasicModel
from monkey import ndb
from application import get_mobile, get_or_create_mobile
from application import crete_channel_token, send_message_to_client, send_message_to_mobile
import random
import time
import logging
import webapp2
import os

timeout = 864000


class MobileKeyModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "mobile": u"手機號碼",
            "code": u"驗証碼",
        }
    code = Fields.StringProperty(required=True)
    client_id = Fields.StringProperty()
    mobile = Fields.StringProperty(default=u"")
    user_agent = Fields.StringProperty(default=u"")

    @classmethod
    def create(cls, controller):
        """ 產生一組 Key """
        client_id = None
        if "client_id" in controller.session:
            client_id = controller.session["client_id"]
        cid = controller.params.get_string("client_id")
        if cid != u"":
            client_id = cid
            n = cls.query(cls.client_id==client_id).order(-cls.sort).get()
            logging.info("cid %s" % cid)
            if n is not None:
                controller.session["mobile_code"] = n.code
                controller.session["mobile_code_time"] = n.sort
                controller.session["client_id"] = client_id
                return n
        for i in xrange(0, 100):
            rnd = ''.join([str(random.randint(100, 999)) for x in range(0, 10)])
            code = rnd[0:6]
            f = cls.get_by_code(code)
            if client_id is None:
                client_id = code + rnd[11:16] + rnd[21:26]
            if f is None:
                f = cls()
                f.code = code
                f.client_id = client_id
                f.user_agent = controller.request.environ.get('HTTP_USER_AGENT')
                f.put()
                controller.session["mobile_code"] = f.code
                controller.session["mobile_code_time"] = f.sort
                controller.session["client_id"] = client_id
                return f

    @classmethod
    def clean(cls, die=timeout):
        """ 清除過期 Key """
        t1 = time.time()-die
        r = cls.query(cls.mobile=="",cls.sort<t1).fetch(100, keys_only=True)
        if r:
            ndb.delete_multi(r)
        t2 = time.time()-die*10
        r2 = cls.query(cls.sort<t2).fetch(100, keys_only=True)
        if r2:
            ndb.delete_multi(r2)

    @classmethod
    def clean_by_client_id(cls, client_id, die=timeout):
        """ 清除特定客戶端 Key """
        r = cls.query(cls.sort<time.time()-die, cls.client_id==client_id).fetch(100, keys_only=True)
        if r:
            ndb.delete_multi(r)

    @classmethod
    def get_by_code(cls, code):
        """ 依驗証碼取得 Key """
        return cls.query(cls.code == code).get()

    @classmethod
    def get_by_client_id(cls, client_id, user_agent):
        """ 取得特定客戶端 Key """
        return cls.query(cls.client_id == client_id, cls.user_agent == user_agent).get()

    @classmethod
    def get_key(cls, controller, check_first=True):
        """ 取得連線 token 與 登入資訊"""
        cls.clean()
        ms = None
        if check_first:
            # 先檢查同客戶端是否存在
            ms = cls.get_by_client_id(controller.params.get_string("client_id"), controller.request.environ.get('HTTP_USER_AGENT'))

            # 用驗証碼檢查
            if "mobile_code" in controller.session and ms is None:
                ms = cls.get_by_code(controller.session["mobile_code"])

        # 若上列2項皆不存在，則建立新的
        if ms is None:
            ms = cls.create(controller)
        # 延長存續時間
        ms.sort = time.time()
        ms.put()
        controller.session["client_id"] = ms.client_id
        controller.context["mobile_code"] = ms.code
        controller.context["token"] = crete_channel_token(ms.client_id)
        controller.context["second"] = int(timeout - (time.time() - float(ms.sort)))
        return ms

    @classmethod
    def login(cls, mobile, code):
        ms = cls.get_by_code(code)
        if mobile.startswith("09"):
            mobile = "+886" + mobile[1:]
        if ms:
            if int(timeout - (time.time() - ms.sort)) >= 0:
                ms.mobile = mobile
                rv = {
                    "action": "login",
                    "status": "success",
                    "client": ms.client_id,
                    "mobile": mobile
                }
                send_message_to_mobile(mobile, rv)
                send_message_to_client(ms.client_id, rv)
                ms.put()
                return ms


class MobileKey(Controller):
    class Meta:
        title = u"手機驗証碼"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10

    @route_menu(list_name=u"backend", text=u"手機驗証碼", sort=34, group=u"資料維護")
    def admin_list(controller):
        return scaffold.list(controller)

    @route_with("/remote/api_refresh")
    def api_refresh(self, *args):
        self.meta.change_view("jsonp")
        send_message_to_client(self.session["client_id"], {
            "action": "api_refresh", "status": "success", "client": self.session["client_id"]
        })

    @route_with("/console/logout")
    @route_with("/remote/channel_logout")
    def console_logout(self, *args):
        self.meta.change_view("jsonp")
        ms = MobileKeyModel.get_key(self, False)
        rv = {
            "action": "logout",
            "status": "success",
            "client": self.session["client_id"],
            "code": ms.code
        }
        send_message_to_client(self.session["client_id"], rv)
        self.session["mobile"] = None
        self.context["data"] = rv

    @route_with("/remote/channel_sign_in")
    def channel_sing_in(self):
        self.meta.change_view("jsonp")
        # 反向驗証使用
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                get_or_create_mobile(self.session["mobile"])
                self.context["data"] = {
                    "action": "channel_sign_in",
                    "is_login": True,
                    "client": self.session["client_id"],
                    "mobile": self.session["mobile"]
                }
                return

        # 正向驗証使用
        if "mobile_code" in self.session:
            ms = MobileKeyModel.get_by_code(self.session["mobile_code"])
            if ms is not None:
                if ms.mobile is not None and ms.mobile != "":
                    get_or_create_mobile(ms.mobile)
                    self.session["mobile"] = str(ms.mobile)
                    self.context["data"] = {
                        "action": "channel_sign_in",
                        "is_login": True,
                        "client": self.session["client_id"],
                        "mobile": self.session["mobile"]
                    }
                    return
        mobile = ""
        client_id = ""
        if "mobile" in self.session:
            mobile = self.session["mobile"]
        if "client_id" in self.session:
            client_id = self.session["client_id"]
        self.context["data"] = {
            "action": "channel_sign_in",
            "is_login": False,
            "client": client_id,
            "mobile": mobile
        }

    @route_with("/remote/get_client_token")
    def get_client_token(self):
        self.meta.change_view("jsonp")
        ms = MobileKeyModel.get_key(self)
        self.context["data"] = {
            "code": ms.code,
            "token": self.context["token"],
            "client": ms.client_id,
        }
        if "mobile" in self.session:
            if self.session["mobile"] is not None:
                m = get_mobile(self.session["mobile"])
                if m is None:
                    return
                self.context["data"] = {
                    "token": self.context["token"],
                    "is_login": True,
                    "client": ms.client_id,
                    "mobile": self.session["mobile"]
                }

    @route_with('/remote/open')
    @add_authorizations(auth.require_admin)
    def check_json(self):
        self.meta.change_view("jsonp")
        mobile = self.params.get_mobile_number("mobile")
        code = self.params.get_string("code")
        ms = MobileKeyModel.login(mobile, code)
        if ms is None:
            self.context["data"] = {
                "error": "MobileKey not exist",
            }
            return
        self.session["mobile"] = mobile
        self.session["client_id"] = ms.client_id
        self.session["mobile_code"] = code
        self.context["data"] = {
            "mobile_code": ms.code,
            "client": ms.client_id,
            "mobile": mobile
        }


class MailReceiver(InboundMailHandler):
    def receive(self, mail_message):
        plaintext_bodies = mail_message.bodies('text/plain')
        for content_type, body in plaintext_bodies:
            decoded_html = body.decode()
            logging.info(decoded_html)
            if decoded_html.find("If you can get this email") >= 0:
                logging.info("Test Mail")
                return
            r = decoded_html.split("Date")
            try:
                n = r[1]
                n = n.split("SMS contents:")[1]
                mobile = r[0].strip().replace("SMS From : ", "").strip()
                content = n.split("Sent")[0].strip()
            except IndexError:
                logging.info("Other Mail")
                return
            content = "".join(content.split())
            content = content.replace("SentbySMStoMailPro", "")
            logging.info(mobile)
            logging.info(content)
            MobileKeyModel.login(mobile, content)

from_sms = webapp2.WSGIApplication([MailReceiver.mapping()], debug=True)