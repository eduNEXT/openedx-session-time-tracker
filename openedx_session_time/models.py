# -*- coding: utf-8 -*-
"""
Database models for openedx_session_time.
"""

from __future__ import absolute_import, unicode_literals

from django.db import models


class SessionLog(models.Model):
    """
    Defines the fields that are stored in the session log database.
    """

    dtcreated = models.DateTimeField('Creation date', auto_now_add=True)
    username = models.CharField(max_length=32, blank=True)
    courseid = models.TextField(blank=True)
    session_duration = models.DurationField('Session duration')
    start_time = models.DateTimeField('Started at')
    end_time = models.DateTimeField('Ended at')
    host = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        fmt = (
            u"[{self.session_duration}] {self.username}@{self.courseid}"
        )
        return fmt.format(self=self)
