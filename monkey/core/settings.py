#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2014/9/30
from webapp2 import get_request
import logging
import inspect
from . import events

_defaults = {}


class ConfigurationError(Exception):
    pass


def load_settings(app_settings=None, refresh=False):
    """
    Executed when the project is created and loads the settings from application/settings.py
    """
    global _defaults

    if _defaults and not refresh:
        return
    if app_settings is None:
        try:
            from application import settings as appsettings
            reload(appsettings)
            # try:
            # except ImportError:
            #     raise ConfigurationError("Settings not found. Please create /application/settings.py")
            appdefaults = appsettings.settings
            logging.debug("Static settings loaded from application.settings.py")
        except:
            try:
                from monkey import base_settings as appsettings
                reload(appsettings)
                # try:
                # except ImportError:
                #     raise ConfigurationError("Settings not found. Please create /application/settings.py")
                appdefaults = appsettings.settings
                logging.debug("Static settings loaded from monkey.settings.py")
            except AttributeError:
                raise ConfigurationError("No dictionary 'settings' found in settings.py")
    else:
        appdefaults = app_settings
    defaults(appdefaults)




def defaults(dict=None):
    """
    Adds a set of default values to the settings registry. These can and will be updated
    by any settings modules in effect, such as the Settings Manager.

    If dict is None, it'll return the current defaults.
    """
    if dict:
        _defaults.update(dict)
    else:
        return _defaults


def settings():
    """
    Returns the entire settings registry
    """
    settings = {}
    events.fire('before_settings', settings=settings)
    settings.update(_defaults)
    events.fire('after_settings', settings=settings)
    return settings


def get(key, default=None):
    """
    Returns the setting at key, if available, raises an ConfigurationError if default is none, otherwise
    returns the default
    """
    _settings = settings()
    if not key in _settings:
        if default is None:
            raise ConfigurationError("Missing setting %s" % key)
        else:
            return default
    return _settings[key]
