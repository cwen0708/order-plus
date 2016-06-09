#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from monkey.core.wtforms.wtforms.widgets import html_params, HTMLString
from monkey.core.wtforms.wtforms.compat import text_type
from cgi import escape

class MultipleReferenceCheckboxWidget(object):
    """
    Widget for MultipleReferenceField. Displays options as checkboxes"""
    def __init__(self, html_tag='div'):
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs['class'] = kwargs.get('class', '').replace('span6', '')
        html = [u'<%s %s>'
            % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            html.append(u'<label class="checkbox" for="%s">%s %s</label>'
                % (subfield.label.field_id, subfield(), subfield.label.text))
        html.append(u'</%s>' % self.html_tag)
        return HTMLString(u''.join(html))


class RichTextWidget(object):
    html_params = staticmethod(html_params)
    """
    Widget for MultipleReferenceField. Displays options as checkboxes"""
    def __init__(self, html_tag='textarea'):
        super(RichTextWidget, self).__init__()
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.id)
        kwargs['class'] = kwargs.get('class', '').replace('span6', '') + " editor"
        if field.data == "None" or field.data is None:
            field.data = ""
        html = u'<%s %s>%s</%s>'% (
            self.html_tag, html_params(**kwargs),
            field.data, self.html_tag
        )
        return HTMLString(html)


class ImageSelectWidget(object):
    html_params = staticmethod(html_params)
    """
    Widget for MultipleReferenceField. Displays options as checkboxes"""
    def __init__(self, html_tag='input'):
        super(ImageSelectWidget, self).__init__()
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.id)
        kwargs['class'] = kwargs.get('class', '').replace('span6', '') + " image"
        if field.data == "None" or field.data is None:
            field.data = ""
        html = u'<div class="img_selector_div"><%s type="hidden" %s value="%s" />' \
               u'<a data-target="%s" class="btn-image-open-dropbox">Dropbox</a>'\
               u'<a data-target="%s" class="btn-image-open-google-picker">Google相冊</a>'\
               u'<a data-target="%s" class="btn-image-open-server">伺服器</a>'\
               u'<div class="img_selector_sp"></div>'\
               % (
            self.html_tag, html_params(**kwargs), field.data,
            field.id,
            field.id,
            field.id,
        )
        if field.data:
            html += u'<div class="img_selector_item" id="img-%s" style="background-image: url(%s);" /></div>' % (field.id, field.data)
        else:
            html += u'<div class="img_selector_item img_selector_item_none" id="img-%s" style="" /></div>' % (field.id)

        return HTMLString(html)


class ImagesSelectWidget(object):
    html_params = staticmethod(html_params)
    """
    Widget for MultipleReferenceField. Displays options as checkboxes"""
    def __init__(self, html_tag='textarea'):
        super(ImagesSelectWidget, self).__init__()
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.id)
        kwargs['class'] = kwargs.get('class', '').replace('span6', '') + " images"
        if field.data == "None" or field.data is None:
            field.data = ""
        list = field.data.split(";")
        html = u'<div class="imgs_selector_div">' \
               u'<%s %s style="display:none" >%s</%s>' \
               u'<a data-target="%s" class="btn-images-open-dropbox">Dropbox</a>'\
               u'<a data-target="%s" class="btn-images-open-google-picker">Google相冊</a>'\
               u'<a data-target="%s" class="btn-images-open-server">伺服器</a>' \
               u'<div class="img_selector_sp"></div>'\
               % (
            self.html_tag, html_params(**kwargs), field.data, self.html_tag,
            field.id,
            field.id,
            field.id,
        )
        for item in list:
            if item != u"":
                html += u'<div class="img_selector_item" data-link="%s" style="background-image: url(%s);" />' % (item, item)
        return HTMLString(html + "</div>")



class CategorySelectWidget(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        options = dict(kwargs, value=value)
        if selected:
            options['selected'] = True
        if value == '__None':
            return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label))))
        else:
            return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label.title))))


class Option(object):
    """
    Renders the individual option from a select field.

    This is just a convenience for various custom rendering situations, and an
    option by itself does not constitute an entire field.
    """
    def __call__(self, field, **kwargs):
        return CategorySelectWidget.render_option(field._value(), field.label.text, field.checked, **kwargs)
