# -*- coding: utf-8 -*-
"""
Database models for openedx_session_time.
"""

from __future__ import absolute_import, unicode_literals

# from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class SessionLog(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<SessionLog, ID: {}>'.format(self.id)
