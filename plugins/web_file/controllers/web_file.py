#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

import monkey
from monkey import scaffold
from monkey.components.upload import Upload
from monkey import route_with
from google.appengine.ext.webapp import blobstore_handlers


class WebFile(monkey.Controller):
    class Meta:
        title = u"檔案管理"
        components = (monkey.scaffold.Scaffolding, Upload)
        advanced_menu = [
            {"url": "/admin/web_file/images_list", "text": u"檔案管理", "sort": 999},
        ]

    @route_with('/admin/web_file/get.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        from google.appengine.ext import blobstore
        from monkey import settings
        cloud_storage_bucket = ""
        if settings.get('upload').get('use_cloud_storage'):
            cloud_storage_bucket = settings.get('upload', {}).get('bucket')
        self.context['data'] = {
            'url': blobstore.create_upload_url(
                success_path= self.uri('admin:web_file:add'),
                gs_bucket_name=cloud_storage_bucket)
        }

    @route_with('/admin/web_file/images_list')
    def admin_images_list(self):
        self.context["list"] = self.meta.Model.all().fetch(250)

    def admin_add(self):
        controller = self.meta._controller
        if self.request.method in ('GET'):
            return scaffold.add(self)
        else:
            item = controller.scaffold.create_factory(controller)
            controller.scaffold.redirect = False

            controller.events.scaffold_before_parse(controller=controller)
            parser = controller.parse_request(fallback=item)

            if controller.request.method in ('PUT', 'POST', 'PATCH'):
                if parser.validate():

                    controller.events.scaffold_before_apply(controller=controller, container=parser.container, item=item)
                    parser.update(item)
                    controller.events.scaffold_before_save(controller=controller, container=parser.container, item=item)
                    item.put()
                    controller.events.scaffold_after_save(controller=controller, container=parser.container, item=item)
                    controller.events.scaffold_after_apply(controller=controller, container=parser.container, item=item)

                    controller.context.set(**{
                        controller.scaffold.singular: item})

                    if controller.scaffold.redirect:
                        return controller.redirect(controller.scaffold.redirect)

                else:
                    controller.context['errors'] = parser.errors
                return "/userfile/" + str(parser.data["file"]) + ".jpg"
