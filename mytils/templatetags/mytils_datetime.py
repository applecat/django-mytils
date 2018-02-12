from django import template

register = template.Library()

from mytils.datetime import pubdate as pubdate_func


@register.filter
def pubdate(value, format=None):
    return pubdate_func(value, format)
