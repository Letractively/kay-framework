# -*- coding: utf-8 -*-

from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from kay.ext.live_settings.models import KayLiveSetting

class KayLiveSettingForm(ModelForm):
  key_name = forms.TextField()
  value = forms.TextField(widget=forms.TextInput)
  class Meta:
    model = KayLiveSetting
    fields = ('key_name', 'value')
