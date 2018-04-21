from django.template import Context, Template


def render_template(string, context=None):
    """
    Util for template rendering
    """
    context = context or {}
    context = Context(context)
    return Template(string).render(context)
