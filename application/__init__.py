#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/9/14.
from mobile import get_mobile, get_or_create_mobile
from message import crete_channel_token
from message import send_message_to_client
from message import send_message_to_mobile
from message import send_message_to_account
from message import create_message_relationship, create_message
from product import get_or_create_product_by_feature
from order_info import create_order
from authorizations import require_orderplus_user, default_authorizations

__all__ = (
    "crete_channel_token",
    "create_message",
    "create_message_relationship",
    "get_or_create_mobile",
    "get_mobile",
    "get_or_create_product_by_feature",
    "send_message_to_mobile",
    "send_message_to_client",
    "send_message_to_account",
    "require_orderplus_user",
    "default_authorizations"
)


mobile_key_action_helper = {
    "group": u"後台帳號管理",
    "actions": [
        {"action": "list", "name": u"手機驗証碼"},
        {"action": "add", "name": u"新增驗証碼"},
        {"action": "edit", "name": u"編輯驗証碼"},
        {"action": "view", "name": u"檢視驗証碼"},
        {"action": "delete", "name": u"刪除驗証碼"},
    ],
    "related_action": "application_user_role"
}