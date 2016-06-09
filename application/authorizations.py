#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/1/28.
from monkey import auth


def require_orderplus_user(controller):
    """
    Requires that a user is logged in
    """
    try:
        account = controller.session["mobile"]
        if account:
            return True
    except KeyError:
        pass
    return (False, "require_orderplus_user")

require_orderplus_user_for_prefix = auth.predicate_chain(auth.prefix_predicate, require_orderplus_user)
require_orderplus_user_for_action = auth.predicate_chain(auth.action_predicate, require_orderplus_user)
require_orderplus_user_for_route = auth.predicate_chain(auth.route_predicate, require_orderplus_user)

default_authorizations = (auth.require_admin_for_prefix(prefix=('admin',)),
                          require_orderplus_user_for_prefix(prefix=('console',)))