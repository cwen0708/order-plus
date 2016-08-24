#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import monkey
import os

_plugins = []
_plugins_list = []

def exists(name):
    """
    Checks to see if a particular plugin is enabled
    """
    return name in _plugins


def register(name, templating=True):
    """
    Adds a plugin's template path to the templating engine
    """
    if name in _plugins:
        return
    import template
    _plugins.append(name)

    if templating:
        path = os.path.normpath(os.path.join(
            os.path.dirname(monkey.__file__),
            '../plugins/%s/templates' % name))
        template.add_template_path(path)
        template.add_template_path(path, prefix=name)


def list():
    return _plugins


def get_plugins_controller(plugin_name):
    module_path = 'plugins.%s' % plugin_name
    try:
        module = __import__('%s' % module_path, fromlist=['*'])
        cls = getattr(module, 'plugins_helper')
        if "plugins_controller" in cls:
            return cls["plugins_controller"].split(",")
    except:
        return [plugin_name]


def get_all_in_application():
    plugins_list = []
    try:
        from application import application_action_helper
        for item in application_action_helper:
            plugins_list.append(item)
    except:
        pass
    return plugins_list


def get_all_installed():
    plugins_list = []
    dir_plugins = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugins'))
    for dirPath in os.listdir(dir_plugins):
        if dirPath.find(".") < 0:
            plugins_list += get_plugins_controller(dirPath)
    try:
        from application import application_action_helper
        for item in application_action_helper:
            plugins_list.append(item)
    except:
        pass
    return plugins_list
