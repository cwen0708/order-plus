#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from monkey.core.plugins import register_by_path
from plugins.backend_account.models.backend_account_model import BackendAccountModel
register_by_path(__file__)

login = BackendAccountModel.get_account
has_record = BackendAccountModel.has_record
create_account = BackendAccountModel.create_account

__all__ = (
    'login',
    'has_record'
    'create_account'
)