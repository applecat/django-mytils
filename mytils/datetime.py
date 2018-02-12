# -*- encoding: utf-8 -*-

from datetime import date, datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.dateformat import DateFormat


# In Django date filter format:
# https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date
# TODAY|YESTERDAY|RECENTLY|LONGAGO
PUBDATE_FORMAT = getattr(settings, 'MYTILS_PUBDATE_FORMAT', _('\\t\\o\\d\\a\\y H:i|\\y\\e\\s\\t\\e\\r\\d\\a\\y H:i|j E|d.m.Y'))
PUBDATE_FORMAT_SPLITTER = getattr(settings, 'MYTILS_PUBDATE_FORMAT_SPLITTER', '|')
PUBDATE_AGO_DAYS = getattr(settings, 'MYTILS_PUBDATE_AGO_DAYS', 6*30)


# def idate_from_to(from_, to, show_year=True):
#     if not from_ or not to:
#         return
#
#     start = u"с %s" % (from_.day)
#     end = u" по %s %s" % (to.day, MONTHS[to.month - 1])
#
#     if from_.month != to.month:
#         start += u" %s" % MONTHS[from_.month - 1]
#
#     if show_year:
#         if from_.year != to.year:
#             start += u" %s" % from_.year
#         end += u" %s" % to.year
#
#     return start + end


def pubdate(d, fmt=None):
    """
    Usually used for display pubdate of some article, blog post etc.

    Splits fmt param in four pieces:
    1) today 16:32 - for today date
    2) yesterday 16:32 - for yeaterday
    3) 10 January 16:32 - date before MYTILS_PUBDATE_AGO_DAYS days (6*30 by default)
    4) 10.01.2017 16:32 - date after MYTILS_PUBDATE_AGO_DAYS days
    """
    if not type(d) is datetime:
        return ""

    if not fmt:
        fmt = PUBDATE_FORMAT  # default format

    # formats
    formats = fmt.split(PUBDATE_FORMAT_SPLITTER)
    if len(formats) != 4:
        # TODO: is throw exeption here needed?
        return ""

    TODAY, YESTERDAY, RECENTLY, LONGAGO = formats

    if settings.USE_TZ:
        now = timezone.now()
        now = timezone.localtime(now)
        d = timezone.localtime(d)
    else:
        now = datetime.now()

    if now.date() == d.date():
        format = TODAY
    elif now.date() - timedelta(days=1) == d.date():
        format = YESTERDAY
    elif now.date() - timedelta(days=PUBDATE_AGO_DAYS) < d.date():
        format = RECENTLY
    else:
        format = LONGAGO

    df = DateFormat(d)
    return df.format(format)

