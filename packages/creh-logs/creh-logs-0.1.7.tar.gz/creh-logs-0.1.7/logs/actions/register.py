# -*- coding: utf-8 -*-
import sys

from .. import contstants
from ..models import Log


def create_by_exception(exception, message, location, user=None, tag=None, code_error=None,
                        level=contstants.LEVEL_ERROR, status=contstants.STATUS_ACTIVE):
    log = Log(
        title=exception.__class__.__name__,
        message=message,
        code_error=code_error,
        location=location,
        user=user,
        level=level,
        tag=tag,
        status=status
    )
    log.save()
    return log


def create_log(title, message, location, user=None, tag=None, code_error=None,
               level=contstants.LEVEL_WARNING, status=contstants.STATUS_ACTIVE):
    log = Log(
        title=title,
        message=message,
        code_error=code_error,
        location=location,
        user=user,
        level=level,
        tag=tag,
        status=status
    )
    log.save()
    return log