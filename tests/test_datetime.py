# -*- coding: utf-8 -*-
"""
Unit-tests for pytils.translit
"""

from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
from django.utils.dateformat import format

from mytils.datetime import pubdate, PUBDATE_AGO_DAYS

from django.template import Context, Template

class DatetimeTestCase(TestCase):
    """
    Test case for mytils.datetime
    """

    def test_pubdate(self):
        """
        Unit-test for pubdate
        TODO: test the russian translation too
        """

        now = datetime.now()
        today = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=21,
            minute=43,
        )

        lang = settings.LANGUAGE_CODE

        # TODO: как тестировать RECENTLY и LONG AGO сравнивая их с простоянными строками? нужно менять величину now в функции, но тогда пропадает весь смысл pubdate
        results = {
            'en': ['today 21:43', 'yesterday 21:43'],
            'ru': ['сегодня 21:43', 'вчера 21:43']
        }

        # TODAY
        itoday = pubdate(today)
        self.assertEqual(itoday, results[lang][0])

        # YESTERDAY
        yesterday = today - timedelta(days=1)
        iyesterday = pubdate(yesterday)
        self.assertEqual(iyesterday, results[lang][1])

        # RECENTLY
        recently = today - timedelta(days=PUBDATE_AGO_DAYS-1)
        irecently = pubdate(recently)
        self.assertEqual(irecently, format(recently, 'j E'))

        # LONG AGO
        longago = today - timedelta(days=PUBDATE_AGO_DAYS+1)
        ilongago = pubdate(longago)
        self.assertEqual(ilongago, format(longago, 'd.m.Y'))

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_pubdate_filter(self):
        t = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate }}', {'mydate': datetime.now()})
        print(t)

        t = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate:"H:i|вчера H:i|j E|d.m.Y" }}', {'mydate': datetime.now()})
        print(t)
