#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from monkey.core.plugins import register_by_path
register_by_path(__file__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import urllib


class GetFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, source_blob_key):
        if self.request.headers.get('If-None-Match'):
                return self.error(304)

        if source_blob_key.find(".jpg"):
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.headers["Content-Transfer-Encoding"] = "base64"
            source_blob_key = source_blob_key.replace(".jpg", "")
            self.response.headers["ETag"] = source_blob_key

        blob_key = str(urllib.unquote(source_blob_key))
        self.response.headers["Cache-Control"] = "public, max-age=604800"
        if not blobstore.get(blob_key):
            self.redirect("/not_found?path=/userfile/" + source_blob_key)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=False)

getfile_app = webapp.WSGIApplication([('/userfile/([^/]+)?', GetFileHandler)],debug=False)


class DownloadFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, source_blob_key):
        if self.request.headers.get('If-Modified-Since'):
            self.error(304)
            return
        if source_blob_key.find(".jpg"):
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.headers["Content-Transfer-Encoding"] = "base64"
            source_blob_key = source_blob_key.replace(".jpg", "")

        blob_key = str(urllib.unquote(source_blob_key))
        self.response.headers["Cache-Control"] = "public, max-age=604800"
        if not blobstore.get(blob_key):
            self.redirect("/not_found?path=/download/" + source_blob_key)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)

download_app = webapp.WSGIApplication([('/download/([^/]+)?', DownloadFileHandler)],debug=False)
