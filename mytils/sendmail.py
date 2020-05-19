from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.template.loader import render_to_string


def send_mail(subject, message, to, bcc=None,
              from_email=settings.DEFAULT_FROM_EMAIL,
              request=None, reply_to=None, attachments=None):

    """
    Base mail sending function.
    attachments - list of absolute paths to files
    """

    subject = ''.join(subject.splitlines())
    if reply_to:
        headers = {'Reply-To': reply_to}
    else:
        headers = {}

    for email in to:
        msg = EmailMessage(
            subject,
            message,
            from_email=from_email,
            to=[email],
            bcc=None,
            headers=headers
        )
        msg.content_subtype = "html"

        # прикрепим приложения
        if attachments is not None:
            for attachment in attachments:
                msg.attach_file(attachment)

        msg.send()


def prepare_message(message_template, context, request=None):
    site = Site.objects.get_current()
    message = render_to_string(
        message_template,
        dict({'site': site, 'request': request}, **context)
    )
    return message


def send_mail_template(subject, message_template, context, to, bcc=None,
                       from_email=settings.DEFAULT_FROM_EMAIL,
                       request=None, reply_to=None, attachments=[]):

    message = prepare_message(message_template, context, request)
    return send_mail(subject, message, to, bcc, from_email,
                     request, reply_to, attachments)


def send_mail_object_fields(subject, to, object, bcc=None, fields_exclude=['id'],
                            message_template='notification/sendform_message.html',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            request=None, reply_to=None, attachments=[]):

    """Send all object fields by email"""

    # Collect object fields
    context = {
        'fields': [
            (field.verbose_name.title(), getattr(object, field.name))
            for field in object._meta.fields if getattr(object, field.name) and
            field.name not in fields_exclude
        ]
    }

    message = prepare_message(message_template, context, request)
    return send_mail(subject, message, to, bcc, from_email,
                     request, reply_to, attachments)


# Deprecated
class SendMailMixin(object):
    """
    Class mixin for sending emails.
    Email template

    """

    send_from = settings.DEFAULT_FROM_EMAIL

    def get_mail_subject(self):
        if hasattr(self, 'mail_subject'):
            return self.mail_subject
        else:
            return 'Sended %s' % self.__class__.__name__

    def get_mail_message_template(self):
        if hasattr(self, 'mail_message_template'):
            return self.mail_message_template
        else:
            return 'notification/%s/message.html' % \
                    self.__class__.__name__.lower()

    def get_mail_context(self):
        return {}

    def get_reply_to(self):
        return None

    def get_attachments(self):
        """Returns list of absolute paths to files"""
        return []

    def send_mail(self, to=[m[1] for m in settings.MANAGERS], request=None):
        send_mail_template(
            subject=self.get_mail_subject(),
            message_template=self.get_mail_message_template(),
            context=self.get_mail_context(),
            to=to,
            from_email=self.send_from,
            request=request,
            reply_to=self.get_reply_to(),
            attachments=self.get_attachments(),
        )


class SendFormMixin(SendMailMixin):
    """
    Used to send Django forms over email.
    All form fields passes to template context.
    """

    mail_message_template = 'notification/sendform_message.html'

    def get_mail_context(self):
        return {'fields': [
            (f.label, f.data) for f in self.visible_fields() if f.data
        ]}


class SendModelMixin(SendMailMixin):
    """
    Used to send Django models over email.
    All model fields passes to template context.
    Model instanse now have the send_mail() method.
    By default email sends to settings.MANAGERS emails.
    """

    mail_message_template = 'notification/sendform_message.html'
    mail_fields_exclude = ['id']

    def get_mail_context(self):
        return {'fields': [
            (field.verbose_name.title(), getattr(self, field.name))
            for field in self._meta.fields if getattr(self, field.name) and
            field.name not in self.mail_fields_exclude
        ]}
