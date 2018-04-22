# -*- coding: utf-8 -*-
"""
Unit-tests for mytils.forms
"""

from django.test import TestCase

from .utils import render_template
from django import forms


class TestForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class MytilsFormsTestCase(TestCase):

    def test_add_field_class_filter(self):
        form = TestForm()
        r = render_template('{% load mytils_forms %}{{ form.name|add_field_class:"test-class" }}', {'form': form})
        self.assertIn('class="test-class"', str(r))

    def test_field_type_filter(self):
        form = TestForm()
        r = render_template('{% load mytils_forms %}{{ form.name|field_type }}', {'form': form})
        self.assertEqual(r, 'CharField')

    def test_widget_type_filter(self):
        form = TestForm()
        r = render_template('{% load mytils_forms %}{{ form.name|widget_type }}', {'form': form})
        self.assertEqual(r, 'TextInput')

    def test_widget_class_filter(self):
        form = TestForm()
        form.fields['name'].widget.attrs['class'] = 'test-class'
        r = render_template('{% load mytils_forms %}{{ form.name|widget_class }}', {'form': form})
        self.assertEqual(r, 'test-class')
