from django import template

register = template.Library()

from mytils.forms import add_field_class as add_field_class_func


@register.filter
def add_field_class(field, css_class):
    """
    Adds class for form field.
    Useful for example for bootstrap forms when needed add input class:
    {{ field|add_field_class:"form-control" }}
    """
    return add_field_class_func(field, css_class)
