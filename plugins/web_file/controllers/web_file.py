#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

import monkey
from monkey import scaffold
from monkey.components.pagination import Pagination
from monkey.components.search import Search
from monkey.components.upload import Upload
from monkey import route_with, route_menu
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


def generate_upload_url(success_path):
    from google.appengine.ext import blobstore
    from monkey import settings
    cloud_storage_bucket = ""
    if settings.get('upload').get('use_cloud_storage'):
        cloud_storage_bucket = settings.get('upload', {}).get('bucket')
    return blobstore.create_upload_url(
            success_path= success_path,
            gs_bucket_name=cloud_storage_bucket)


class WebFile(monkey.Controller):
    class Meta:
        components = (scaffold.Scaffolding, Upload, Pagination, Search)
        pagination_limit = 10
        pagination_actions = ("list", "images_list",)
        upload_actions = ("add", "add_from_ui")
        
    class Scaffold:
        title = {
            "list": u"檔案管理",
            "add": u"新增檔案",
            "edit": u"編輯檔案",
            "view": u"檢視檔案",
        }
        display_properties_in_list = ("filename", "content_type", "size", "url")

    @route_with('/admin/web_file/get.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        uri = self.params.get_string("uri", 'admin:web_file:add_from_ui')
        self.context['data'] = {
            'url': generate_upload_url(self.uri(uri))
        }

    @route_menu(list_name=u"backend", text=u"圖片", sort=9800, icon="files-o", group=u"檔案管理")
    @route_with('/admin/web_file/images_list')
    def admin_images_list(self):
        self.meta.pagination_limit = 12
        model = self.meta.Model
        def photo_factory(self):
            return model.query(
                model.content_type.IN(["image/jpeg", "image/jpg", "image/png", "image/gif"])).order(
                -model.content_type, -model.created, model._key)
        self.scaffold.query_factory = photo_factory
        return scaffold.list(self)

    @route_menu(list_name=u"backend", text=u"檔案", sort=9801, icon="files-o", group=u"檔案管理")
    @route_with('/admin/web_file/list')
    def admin_list(self):
        return scaffold.list(self)

    def admin_add(self):
        def scaffold_after_apply(**kwargs):
            item = kwargs["item"]
            controller = kwargs["controller"]
            blob_key = blobstore.BlobInfo.get(item.file)
            item.content_type = blob_key.content_type
            item.filename = blob_key.filename
            item.hash = blob_key.md5_hash
            item.size = blob_key.size
            item.url = "/userfile/" + str(item.file) + "." + item.filename.split(".")[-1]
            item.put()
            controller.context["data"] = {
                "url": item.url,
                "item": item
            }
        self.events.scaffold_after_apply += scaffold_after_apply
        return scaffold.add(self)

    @route_with('/admin/web_file/add_from_ui')
    def admin_add_from_ui(self):
        self.meta.change_view("json")
        def scaffold_after_apply(**kwargs):
            item = kwargs["item"]
            controller = kwargs["controller"]
            blob_key = blobstore.BlobInfo.get(item.file)
            item.content_type = blob_key.content_type
            item.filename = blob_key.filename
            item.hash = blob_key.md5_hash
            item.size = blob_key.size
            item.url = "/userfile/" + str(item.file) + "." + item.filename.split(".")[-1]
            item.put()
            controller.context["data"] = {
                "url": item.url,
                "item": item
            }
        self.events.scaffold_after_apply += scaffold_after_apply
        return scaffold.add(self)

    def admin_delete(self, key):
        try:
            item = self.util.decode_key(key).get()
            file_key = item.file
            blobstore.delete(file_key)
        except:
            pass
        return scaffold.delete(self, key)