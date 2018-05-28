from django.test import TestCase

from django import forms
from django.db import models
from django.core import mail

from mytils.sendmail import send_mail, SendModelMixin


class TestForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class TestModel(models.Model, SendModelMixin):
    name = models.CharField(max_length=250)
    text = models.TextField()
    email = models.EmailField()


class MytilsFormsTestCase(TestCase):

    def test_send_mail(self):
        send_mail('subject', 'message', to=['test@test.ru'])
        self.assertEqual(len(mail.outbox), 1)  # письмо отправлено


    def test_send_model_mixin(self):
        obj = TestModel(name='John Doe', text='Lorem ipsum dolor sit amet', email='test@example.com')
        obj.send_mail()
        self.assertEqual(len(mail.outbox), 1)  # письмо отправлено
