# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter(name='add_page')
def add_page(value, arg):
    splited = value.split('/')
    if splited[-2].isdigit():
        page = int(splited[-2]) + int(arg)
        if page > 0:
            if page == 1:
                splited[-2] = ""
                splited = splited[:-1]
            else:
                splited[-2] = str(page)
            return '/'.join(splited)
    else:
        page = 1 + int(arg)
        if page > 1:
            splited[-1] = str(page)
            return '/'.join(splited) + '/'
    return value
