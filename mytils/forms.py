

def add_field_class(field, css_class):
    """
    Adds class for form field.
    """
    return field.as_widget(attrs={"class": css_class})


def get_field_type(value):
    return value.field.__class__.__name__


def get_widget_type(value):
    return value.field.widget.__class__.__name__


def get_widget_class(value):
    return value.field.widget.attrs.get('class', '')
