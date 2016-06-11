#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/22.

settings = dict()
# 應用程式設定
settings['application'] = {}
settings['application']['name'] = u'OrderPlus'
settings['application']['custom_error'] = True
settings['application']['message_timeout'] = 28800

# 驗証失敗時，重新導向路徑
settings["authorization_redirect"] = []
settings["authorization_redirect"].append({"authorization": 'require_orderplus_user', "redirect": '/'})
settings["authorization_redirect"].append({"authorization": 'require_admin', "redirect": '/admin/login'})
settings["authorization_redirect"].append({"authorization": 'require_user', "redirect": '/login.html'})

# 時區
settings['timezone'] = {}
settings['timezone']['local'] = 'Asia/Taipei'
# 設定用來寄送郵件的相關設定
settings['email'] = {}
settings['email']['sender'] = None
settings['email']['mailgun'] = {
    "domain_name": u"orderplus.com.tw",
    "default_sender": "service",
    "api_key": u"key-4df974aaafbe668bfd9b3539d14987e3"
}

# 外掛模組
settings['plugins'] = {}
settings['plugins']['scaffold'] = True
settings['plugins']['flash_messages'] = True
settings['plugins']['backend_account'] = True
settings['plugins']['backend_account_administrator'] = {}
settings['plugins']['backend_account_administrator']['name'] = u'管理者'
settings['plugins']['backend_account_administrator']['account'] = u'admin'
settings['plugins']['backend_account_administrator']['password'] = u'qwER12#$'
settings['plugins']['backend_account_administrator']['level'] = 999
settings['plugins']['backend_ui_saimiri'] = False
settings['plugins']['backend_ui_material'] = True
settings['plugins']['online_code'] = True
settings['plugins']['oauth'] = False
settings['plugins']['oauth_manager'] = False
settings['plugins']['custom_auth'] = False
settings['plugins']['recaptcha'] = False
settings['plugins']['web_settings'] = False
settings['plugins']['web_page'] = False
settings['plugins']['web_file'] = True
settings['plugins']['settings'] = False

settings['upload'] = {
    # Whether to use Cloud Storage (default) or the blobstore to store uploaded files.
    'use_cloud_storage': False,
    # The Cloud Storage bucket to use. Leave as "None" to use the default GCS bucket.
    # See here for info: https://developers.google.com/appengine/docs/python/googlecloudstorageclient/activate#Using_the_Default_GCS_Bucket
    'bucket': None
}

# Enables or disables app stats.
# Note that appstats must also be enabled in app.yaml.
settings['appstats'] = {
    'enabled': False,
    'enabled_live': False
}

settings['google_cloud_sql'] = {
    'database': u'',
    'instance_name': u'yooliang-technology:data',
    'service_ip': u'173.194.250.158',
}

settings['app_config'] = {
    'webapp2_extras.sessions': {
        # WebApp2 encrypted cookie key
        # You can use a UUID generator like http://www.famkruithof.net/uuid/uuidgen
        'secret_key': '_PUT_KEY_HERE_YOUR_SECRET_KEY_',
    },
    'webapp2_extras.auth': {
        'user_model': 'plugins.custom_auth.models.user.User',
        'user_attributes': ['email'],
    }
}

settings['oauth2'] = {
    # OAuth2 Configuration should be generated from
    # the google cloud console (Credentials for Web Application)
    'client_id': '200860892604-q9g76sk9smnc52ckicjkdiuk6h5ia7l0.apps.googleusercontent.com',  # XXXXXXXXXXXXXXX.apps.googleusercontent.com
    'client_secret': 'hUqWKgs5yhn7Xx1Rs0DXM4gN',
    'developer_key': None  # Optional
}

settings['oauth2_service_account'] = {
    # OAuth2 service account configuration should be generated
    # from the google cloud console (Service Account Credentials)
    'client_email': None,  # XXX@developer.gserviceaccount.com
    'private_key': None,  # Must be in PEM format
    'developer_key': None  # Optional
}

# Password AES Encryption Parameters
# aes_key must be only 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes (characters) long.
settings['aes_key'] = "12_24_32_BYTES_KEY_FOR_PASSWORDS"
settings['salt'] = "_PUT_SALT_HERE_TO_SHA512_PASSWORDS_"

# get your own consumer key and consumer secret by registering at https://dev.twitter.com/apps
# callback url must be: http://[YOUR DOMAIN]/login/twitter/complete
settings['twitter_consumer_key'] = 'TWITTER_CONSUMER_KEY'
settings['twitter_consumer_secret'] = 'TWITTER_CONSUMER_SECRET'

#Facebook Login
# get your own consumer key and consumer secret by registering at https://developers.facebook.com/apps
#Very Important: set the site_url= your domain in the application settings in the facebook app settings page
# callback url must be: http://[YOUR DOMAIN]/login/facebook/complete
settings['fb_api_key'] = 'FACEBOOK_API_KEY'
settings['fb_secret'] = 'FACEBOOK_SECRET'

#Linkedin Login
#Get you own api key and secret from https://www.linkedin.com/secure/developer
settings['linkedin_api'] = 'LINKEDIN_API'
settings['linkedin_secret'] = 'LINKEDIN_SECRET'

# Github login
# Register apps here: https://github.com/settings/applications/new
settings['github_server'] = 'github.com'
settings['github_redirect_uri'] = 'http://www.example.com/social_login/github/complete',
settings['github_client_id'] = 'GITHUB_CLIENT_ID'
settings['github_client_secret'] = 'GITHUB_CLIENT_SECRET'

# Enable Federated login (OpenID and OAuth)
# Google App Engine Settings must be set to Authentication Options: Federated Login
settings['enable_federated_login'] = True

# List of social login providers
# uri is for OpenID only (not OAuth)
settings['social_providers'] = {
        'google': {'name': 'google', 'label': 'Google', 'uri': 'gmail.com'},
        'github': {'name': 'github', 'label': 'Github', 'uri': ''},
        'facebook': {'name': 'facebook', 'label': 'Facebook', 'uri': ''},
        'linkedin': {'name': 'linkedin', 'label': 'LinkedIn', 'uri': ''},
        #'myopenid': {'name': 'myopenid', 'label': 'MyOpenid', 'uri': 'myopenid.com'},
        'twitter': {'name': 'twitter', 'label': 'Twitter', 'uri': ''},
        'yahoo': {'name': 'yahoo', 'label': 'Yahoo!', 'uri': 'yahoo.com'},
    }

# If true, it will write in datastore a log of every email sent
settings['log_email'] = False

# If true, it will write in datastore a log of every visit
settings['log_visit'] = False

settings['recaptcha_site_key'] = '6LeGnP8SAAAAAIk3VyWoxqiHBSAgIqTKBxgJKgZF'
settings['recaptcha_secret_key'] = '6LeGnP8SAAAAAH90uO0RQ3xCDKfGm2xy7EYpTcin'

settings['app_name'] = 'Yooliang'