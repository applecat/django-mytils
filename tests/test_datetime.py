# -*- coding: utf-8 -*-
"""
Unit-tests for pytils.translit
"""

from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
from django.utils.dateformat import format

from mytils.datetime import pubdate, PUBDATE_AGO_DAYS
from freezegun import freeze_time

from django.template import Context, Template

from django.utils.translation import activate
activate('ru')


class DatetimeTestCase(TestCase):
    """
    Test case for mytils.datetime
    """

    @freeze_time("2018-02-12")
    def test_pubdate(self):
        """
        Unit-test for pubdate
        TODO: automate test test the russian translation too
        """

        today = datetime(
            year=2018,
            month=2,
            day=12,
            hour=21,
            minute=43,
        )
        yesterday = today - timedelta(days=1)

        # settings.LANGUAGE_CODE = 'ru'
        lang = settings.LANGUAGE_CODE


        dates = [today, yesterday, datetime(2018, 1, 1), datetime(2017, 4, 15)]

        results_langs = {
            'en-us': ['today 9:43 p.m.', 'yesterday 9:43 p.m.', '1st January', '04/15/2017'],
            'ru':    ['сегодня 21:43',   'вчера 21:43',         '1 января',    '15.04.2017'],
        }
        results = results_langs[lang]

        for i, d in enumerate(dates):
            self.assertEqual(pubdate(d), results[i])


    # def render_template(self, string, context=None):
    #     context = context or {}
    #     context = Context(context)
    #     return Template(string).render(context)
    #
    # def test_pubdate_filter(self):
    #     t = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate }}', {'mydate': datetime.now()})
    #     print(t)
    #
    #     t = self.render_template('{% load mytils_datetime %}{{ mydate|pubdate:"H:i|вчера H:i|j E|d.m.Y" }}', {'mydate': datetime.now()})
    #     print(t)
