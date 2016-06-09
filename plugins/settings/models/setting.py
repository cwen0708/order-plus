#!/usr/bin/env python
# -*- coding: utf-8 -*-
import monkey
from google.appengine.api import memcache
import logging
import datetime


class Setting(monkey.Model):
    _defaults = {}
    _settings = {}
    _settings_key = None
    _name = 'Unknown'
    class Meta:
        label_name = {
            "name": u"名稱",
            'administrator_name': u'管理員名稱',
            'administrator_account': u'管理帳號',
            'administrator_password': u'管理密碼',
            "title": u"標題",
            "title_en": u"英文標題",

            "oauth": u"oauth 驗証",
            "oauth_manager": u"oauth 驗証管理中心",
            "custom_auth": u"第三方登錄",
            "web_page": u"網站頁面",
            "web_settings": u"網站設定",
            "web_file": u"檔案管理中心",
        }

    class __metaclass__(monkey.Model.__metaclass__):
        def __new__(meta, name, bases, dict):
            cls = monkey.Model.__metaclass__.__new__(meta, name, bases, dict)

            if name != 'Setting':
                Setting._settings[monkey.inflector.underscore(cls.__name__)] = cls

                if name not in ('ApplicationSetting', 'TimezoneSetting', 'EmailSetting', 'OAuth2Setting',
                                'UploadSetting', 'ServiceAccountSetting', 'GoogleCloudSQLSetting'):
                    from plugins.settings import is_active
                    if is_active():
                        logging.warning("Dynamic settings class %s loaded after the dynamic settings plugin was activated. Please check app/settings.py" % name)

            return cls

    @classmethod
    def factory(cls, name):
        return cls._settings[monkey.inflector.underscore(name)]

    @classmethod
    def _get_kind(cls):
        return '_monkey_setting_%s' % cls._settings_key

    @classmethod
    def get_key(cls):
        return monkey.ndb.Key(cls, cls._settings_key)

    @classmethod
    def get_instance(cls, static_settings=None):
        result = cls.get_instance_async().get_result()
        if not result:
            result = cls.get_default(defaults=static_settings, wait=True)
        return result

    @classmethod
    def get_default(cls, defaults=None, wait=True):
        cls_defaults = cls._defaults.copy()

        if defaults:
            cls_defaults.update(defaults.get(cls._settings_key, {}))
        result = cls(key=cls.get_key(), **cls_defaults)
        f = result.put_async()
        if wait:
            f.get_result()
        return result

    @classmethod
    def get_instance_async(cls):
        key = cls.get_key()
        return key.get_async()

    @classmethod
    def get_classes(cls):
        return cls._settings

    @classmethod
    @monkey.caching.cache_using_memcache('__monkey_settings')
    def get_settings(cls, static_settings):
        settings = {}

        # Gather all of the settings instances as futures
        futures = {}
        for k, settings_cls in cls._settings.iteritems():
            futures[settings_cls] = settings_cls.get_instance_async()

        # Wait for them to finish together
        monkey.ndb.Future.wait_all(futures.itervalues())

        # Transform them into dictionaries, using the default if needed.
        for settings_cls, future in futures.iteritems():
            value = future.get_result()
            if not value:
                value = settings_cls.get_default(defaults=static_settings, wait=False)

            settings[settings_cls._settings_key] = value.to_dict()

        logging.info("Dynamic settings loaded from datastore")

        return settings

    @classmethod
    def get_settings_without_memcache(cls, static_settings):
        settings = {}

        # Gather all of the settings instances as futures
        futures = {}
        for k, settings_cls in cls._settings.iteritems():
            futures[settings_cls] = settings_cls.get_instance_async()

        # Wait for them to finish together
        monkey.ndb.Future.wait_all(futures.itervalues())

        # Transform them into dictionaries, using the default if needed.
        for settings_cls, future in futures.iteritems():
            value = future.get_result()
            if not value:
                value = settings_cls.get_default(defaults=static_settings, wait=False)

            settings[settings_cls._settings_key] = value.to_dict()

        logging.info("Dynamic settings loaded from datastore without memcache")

        return settings

    def after_put(self, key):
        memcache.delete('__monkey_settings')
        memcache.set('_monkey_settings_update_mutex', datetime.datetime.utcnow())


class ApplicationSetting(Setting):
    _name = u'網站基本設定'
    _settings_key = 'application'
    name = monkey.ndb.StringProperty(indexed=False)
    administrator_name = monkey.ndb.StringProperty(indexed=False)
    administrator_account = monkey.ndb.StringProperty(indexed=False)
    administrator_password = monkey.ndb.StringProperty(indexed=False)


class TimezoneSetting(Setting):
    _name = u'時區'
    _settings_key = 'timezone'
    local = monkey.ndb.StringProperty(indexed=False)


class EmailSetting(Setting):
    _name = 'Email'
    _settings_key = 'email'
    sender = monkey.ndb.StringProperty(indexed=False)


class UploadSetting(Setting):
    _name = u'檔案上傳'
    _settings_key = 'upload'
    _description = u"""檔案上傳的位置及其設定"""
    use_cloud_storage = monkey.ndb.BooleanProperty(indexed=False, default=True)
    bucket = monkey.ndb.StringProperty(indexed=False, verbose_name="Leave blank to use the default GCS bucket.")


class OAuth2Setting(Setting):
    _name = 'OAuth2'
    _settings_key = 'oauth2'
    _description = """OAuth2 Configuration should be generated from https://code.google.com/apis/console The API Console."""
    client_id = monkey.ndb.StringProperty(indexed=False)
    client_secret = monkey.ndb.StringProperty(indexed=False)
    developer_key = monkey.ndb.StringProperty(indexed=False)


class ServiceAccountSetting(Setting):
    _name = 'OAuth2 Service Account'
    _settings_key = 'oauth2_service_account'
    client_email = monkey.ndb.StringProperty(indexed=False, verbose_name="...@developer.gserviceaccount.com")
    private_key = monkey.ndb.TextProperty(verbose_name="PEM Format")
    developer_key = monkey.ndb.StringProperty(indexed=False)


class GoogleCloudSQLSetting(Setting):
    _name = u'Cloud SQL'
    _settings_key = 'google_cloud_sql'
    _description = u"""Google 雲端資料庫相關設定"""
    database = monkey.ndb.StringProperty(indexed=False)
    instance_name = monkey.ndb.StringProperty(indexed=False)
    service_ip = monkey.ndb.StringProperty(indexed=False)

