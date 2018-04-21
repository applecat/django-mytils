

def add_field_class(field, css_class):
    """
    Adds class for form field.
    """
    return field.as_widget(attrs={"class": css_class})
