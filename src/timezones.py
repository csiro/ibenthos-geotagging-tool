"""
timezones.py: This module provides functionality to handle timezones

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
from datetime import timedelta, tzinfo

TIMEZONES = ['UTC-12:00', 'UTC-11:00', 'UTC-10:00', 'UTC-09:30', 'UTC-09:00', 'UTC-08:00',
             'UTC-07:00', 'UTC-06:00', 'UTC-05:00', 'UTC-04:00', 'UTC-03:30', 'UTC-03:00',
             'UTC-02:30', 'UTC-02:00', 'UTC-01:00', 'UTC+00:00', 'UTC+01:00', 'UTC+02:00',
             'UTC+03:00', 'UTC+03:30', 'UTC+04:00', 'UTC+04:30', 'UTC+05:00', 'UTC+05:30',
             'UTC+05:45', 'UTC+06:00', 'UTC+06:30', 'UTC+07:00', 'UTC+08:00', 'UTC+08:45',
             'UTC+09:00', 'UTC+09:30', 'UTC+10:00', 'UTC+10:30', 'UTC+11:00', 'UTC+12:00',
             'UTC+12:45', 'UTC+13:00', 'UTC+13:45', 'UTC+14:00']

class Timezone(tzinfo):
    '''
    This class provides minimum functionality to create a timezone object
    from a string in the format 'UTC±HH:MM'.
    '''
    def __init__(self, name):
        self._tzname = name
        time = name.replace('UTC', '').split(':')
        self._utcoffset = timedelta(hours=int(time[0]), minutes=int(time[1]))
        self._dst = timedelta(0)

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return self._dst

    def tzname(self, dt):
        return self._tzname

    def fromutc(self, dt):
        return dt + self.utcoffset(dt)
