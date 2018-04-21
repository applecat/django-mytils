# -*- coding: utf-8 -*-
"""
Unit-tests for mytils.forms
"""

from datetime import datetime, timedelta

from django.test import TestCase
from django.template import Context, Template

from .utils import render_template
from django import forms


class TestForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class MytilsFormsTestCase(TestCase):
    """
    Test case for mytils.forms
    """

    def test_pubdate_filter(self):
        """
        Unit-test for pubdate template filter
        """
        form = TestForm()
        r = render_template('{% load mytils_forms %}{{ form.name|add_field_class:"test-class" }}', {'form': form})
        self.assertIn('class="test-class"', str(r))
