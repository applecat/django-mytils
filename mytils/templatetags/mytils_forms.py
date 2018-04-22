from django import template

register = template.Library()

from mytils.forms import (
    add_field_class as add_field_class_func,
    get_field_type,
    get_widget_type,
    get_widget_class,
)


@register.filter
def add_field_class(field, css_class):
    """
    Adds class for form field.
    Useful for example for bootstrap forms when needed add input class:
    {{ field|add_field_class:"form-control" }}
    """
    return add_field_class_func(field, css_class)


@register.filter
def field_type(field):
    """
    Returns fields's class name:
    CharField

    """
    return get_field_type(field)


@register.filter
def widget_type(field):
    """
    Returns fields's widget class name:
    CheckboxInput

    Example: {% if field|widget_type != "CheckboxInput" %}
    """
    return get_widget_type(field)


@register.filter
def widget_class(field):
    return get_widget_class(field)
