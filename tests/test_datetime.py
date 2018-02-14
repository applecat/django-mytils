# -*- coding: utf-8 -*-
"""
Unit-tests for mytils.datetime
"""

from datetime import datetime, timedelta

from django.test import TestCase
from django.template import Context, Template
from django.utils.translation import activate

from freezegun import freeze_time

from mytils.datetime import pubdate


class MytilsDatetimeTestCase(TestCase):
    """
    Test case for mytils.datetime
    """

    @freeze_time("2018-02-12")
    def setUp(self):
        today = datetime(
            year=2018,
            month=2,
            day=12,
            hour=21,
            minute=43,
        )
        yesterday = today - timedelta(days=1)

        self.test_langs = ['en-us', 'ru']

        self.test_dates = [today, yesterday, datetime(2018, 1, 1), datetime(2017, 4, 15)]

        self.test_results = {
            'en-us': ['today 9:43 p.m.', 'yesterday 9:43 p.m.', '1st January', '04/15/2017'],
            'ru':    ['сегодня 21:43',   'вчера 21:43',         '1 января',    '15.04.2017'],
        }

    @freeze_time("2018-02-12")
    def test_pubdate(self):
        """
        Unit-test for pubdate function
        """

        for lang in self.test_langs:
            activate(lang)
            results = self.test_results[lang]
            for i, d in enumerate(self.test_dates):
                r = pubdate(d)
                self.assertEqual(r, results[i])

    def render_template(self, string, context=None):
        """
        Util for template rendering
        """
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    @freeze_time("2018-02-12")
    def test_pubdate_filter(self):
        """
        Unit-test for pubdate template filter
        """
        for lang in self.test_langs:
            activate(lang)
            results = self.test_results[lang]
            for i, d in enumerate(self.test_dates):
                r = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate }}', {'mydate': d})
                self.assertEqual(r, results[i])

        # Custom format
        test_results = ['21:43', 'вчера в 21:43', '1 января', '15.04.17']
        for i, d in enumerate(self.test_dates):
            r = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate:"H:i|вчера в H:i|j E|d.m.y" }}', {'mydate': d})
            self.assertEqual(r, test_results[i])
