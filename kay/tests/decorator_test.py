#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay decorator test.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import unittest

from google.appengine.ext import db
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import user_service_stub
from google.appengine.api.capabilities import capability_stub

from werkzeug import BaseResponse, Client, Request

import kay
from kay.app import get_application
from kay.utils import local
from kay.utils import forms
from kay.utils.forms import ValidationError
from kay.conf import LazySettings
from kay.tests import capability_stub as mocked_capability_stub

class DecoratorTestCase(unittest.TestCase):

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)

  def tearDown(self):
    pass

  def test_success(self):
    """Test with normal CapabilityServiceStub"""
    if apiproxy_stub_map.apiproxy\
          ._APIProxyStubMap__stub_map.has_key('capability_service'):
      del(apiproxy_stub_map.apiproxy\
            ._APIProxyStubMap__stub_map['capability_service'])
    apiproxy_stub_map.apiproxy.RegisterStub(
      'capability_service',
      capability_stub.CapabilityServiceStub())
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_failure(self):
    """Test with DisabledCapabilityServiceStub
    """
    if apiproxy_stub_map.apiproxy\
          ._APIProxyStubMap__stub_map.has_key('capability_service'):
      del(apiproxy_stub_map.apiproxy\
            ._APIProxyStubMap__stub_map['capability_service'])
    apiproxy_stub_map.apiproxy.RegisterStub(
      'capability_service',
      mocked_capability_stub.DisabledCapabilityServiceStub())
    response = self.client.get('/')
    self.assertEqual(response.status_code, 503)

if __name__ == "__main__":
  unittest.main()
