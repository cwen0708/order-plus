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
from application import get_mobile
from application import crete_channel_token, send_message_to_client, send_message_to_mobile
import random, string
import time
import logging
import webapp2
import os

timeout = 300


class PostTokenModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "mobile": u"手機號碼",
            "token": u"驗証碼",
        }
    token = Fields.StringProperty(required=True)
    client_id = Fields.StringProperty()
    mobile = Fields.StringProperty()

    @classmethod
    def create(cls, controller):
        """
        產生一組驗証碼
        """
        client_id = None
        if "client_id" in controller.session:
            client_id = controller.session["client_id"]
        for i in xrange(0, 100):
            rnd = ''.join([str(random.randint(100, 999)) for x in range(0, 10)])
            token = rnd[0:6]
            f = cls.get_by_token(token)
            if client_id is None:
                client_id = token + rnd[11:16] + rnd[21:26]
            if f is None:
                f = cls()
                f.token = token
                f.client_id = client_id
                f.put()
                controller.session["mobile_token"] = f.token
                controller.session["mobile_token_time"] = f.sort
                controller.session["client_id"] = client_id
                return f

    @classmethod
    def clean(cls, die=timeout):
        """
        產生一組驗証碼
        """
        r = cls.query(cls.sort<time.time()-die).fetch(100, keys_only=True)
        if r:
            ndb.delete_multi(r)

    @classmethod
    def get_by_token(cls, token):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.token == token).get()

    @classmethod
    def check_token(cls, mobile, token):
        k = cls.get_by_token(token)
        if k is None:
            return False
        if k.mobile == mobile:
            return k.client_id
        else:
            return None

    @classmethod
    def get_key(cls, controller):
        cls.clean()
        length = 30
        m = cls()
        m.client_id = controller.session["client_id"]
        m.token = ''.join(random.choice(string.lowercase) for i in range(length))
        m.mobile = controller.session["mobile"]
        m.put()
        return m


class PostToken(Controller):
    class Meta:
        title = u"手機驗証碼"
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10

    @route_menu(list_name=u"backend", text=u"手機驗証碼", sort=34, group=u"資料維護")
    def admin_list(controller):
        return scaffold.list(controller)

    @route_with('/remote/get_post_token')
    def get_post_token(self, *args):
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.context['data'] = {
            'info': "error",
            'msg': "need to login"
        }
        if "mobile" not in self.session:
            return
        if self.session["mobile"] is None:
            return
        if "client_id" not in self.session:
            return
        if self.session["client_id"] is None:
            return
        m = PostTokenModel.get_key(self)

        self.context['data'] = {
            'info': "success",
            'msg': "success",
            "token": m.token
        }


check_token = PostTokenModel.check_token
