#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for forms.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import unittest
import logging

g_path = "/usr/local/google_appengine"
extra_path = [
  os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
  g_path,
  os.path.join(g_path, 'lib', 'antlr3'),
  os.path.join(g_path, 'lib', 'webob'),
  os.path.join(g_path, 'lib', 'django'),
  os.path.join(g_path, 'lib', 'yaml', 'lib'),
]
sys.path = extra_path + sys.path
APP_ID = u'test'
os.environ['APPLICATION_ID'] = APP_ID

from google.appengine.ext import db
import kay
kay.setup()

from werkzeug import Request

from kay.utils import local
from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from kay.utils.forms import ValidationError
from kay.tests.models import TestModel

from base import GAETestBase

class TestModelForm(ModelForm):
  csrf_protected = False
  class Meta():
    model = TestModel

class ModelFormTest(GAETestBase):
  def setUp(self):
    super(ModelFormTest, self).setUp()
    entries = TestModel.all().fetch(100)
    db.delete(entries)

  def test_form(self):
    """Form validation test with ModelForm."""
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())
    f = TestModelForm()
    params = {"number": "12"}
    # In your view, you can validate the form data with:
    # f.validate(request.form)
    # or with(If you have FileField):
    # f.validate(request.form, request.files)
    self.assertEqual(f.validate(params), False)

    f.reset()
    params = {"number": "12",
              "data_field": "data string longer than 20 characters",
              "is_active": "False"}
    self.assertEqual(f.validate(params), False)

    f.reset()
    params = {"number": "12", "data_field": "data string",
              "is_active": "False"}
    self.assertEqual(f.validate(params), True)
    f.save()
    self.assertEqual(TestModel.all().count(), 1)
    

  def tearDown(self):
    entries = TestModel.all().fetch(100)
    db.delete(entries)
    

class TestForm(forms.Form):
  csrf_protected = False
  username = forms.TextField("user name", required=True)
  password = forms.TextField("password", required=True)
  password_again = forms.TextField("confirm password", required=True)
  model_field = forms.ModelField(TestModel, label="ModelField Test",
                                 required=True,
                                 query=TestModel.all().filter('is_active =', True),
                                 option_name='data_field')
  
  def context_validate(self, data):
    if data['password'] != data['password_again']:
      raise ValidationError(u'The two passwords must be the same')

class FormTest(GAETestBase):
  def setUp(self):
    super(FormTest, self).setUp()
    if TestModel.all().count() == 0:
      for i in range(10):
        t = TestModel(number=i, data_field='Test Data %02d' % i,
                      is_active=(i%2==0))
        t.put()

  def test_form(self):
    """Form validation test with context_validate."""
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())
    f = TestForm()
    params = {'username': 'hoge'}
    self.assertEqual(f.validate(params), False)
    params = {
      'username': 'hoge',
      'password': 'fugafuga',
      'password_again': 'fugafuga',
      'model_field': str(TestModel.all().get().key())
    }
    result = f.validate(params)
    self.assertEqual(result, True)
    params['password_again'] = 'moge'
    result = f.validate(params)
    self.assertEqual(result, False)

  def tearDown(self):
    entries = TestModel.all().fetch(100)
    db.delete(entries)

class TestForm2(forms.Form):
  csrf_protected = False
  int_field = forms.IntegerField("int", min_value=5, max_value=99)
  float_field = forms.FloatField("float", min_value=5.5, max_value=99.9)
  number_field = forms.NumberField("number", min_value=5.5, max_value=99.9)

class NumberFieldTest(GAETestBase):
  def setUp(self):
    super(NumberFieldTest, self).setUp()
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())

  def test_validate(self):
    """Float value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 10.7})
    self.assertEqual(result, True)
    self.assertEqual(f['float_field'], 10.7)

    f = TestForm2()
    result = f.validate({'float_field': 'ten'})
    self.assertEqual(result, False)

    f = TestForm2()
    result = f.validate({'number_field': 10.7})
    self.assertEqual(result, True)
    self.assertEqual(f['number_field'], 10.7)

    f = TestForm2()
    result = f.validate({'number_field': 'ten'})
    self.assertEqual(result, False)

    f = TestForm2()
    result = f.validate({'int_field': 10})
    self.assertEqual(result, True)
    self.assertEqual(f['int_field'], 10)

    f = TestForm2()
    result = f.validate({'int_field': 'ten'})
    self.assertEqual(result, False)

  def test_min(self):
    """Minimal value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 5.4})
    self.assertEqual(result, False)

    result = f.validate({'int_field': 4})
    self.assertEqual(result, False)

    result = f.validate({'number_field': 5.4})
    self.assertEqual(result, False)

  def test_max(self):
    """Maximum value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 100.1})
    self.assertEqual(result, False)

    result = f.validate({'int_field': 100})
    self.assertEqual(result, False)

    result = f.validate({'number_field': 100.1})
    self.assertEqual(result, False)


if __name__ == "__main__":
  unittest.main()
