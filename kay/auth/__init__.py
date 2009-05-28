# -*- coding: utf-8 -*-

"""
Kay auth application.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from kay.auth.models import AnonymousUser

def get_user(request):
  return AnonymousUser()
