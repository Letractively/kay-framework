# -*- coding: utf-8 -*-

"""
Settings and configuration for Kay.

Values will be read from the module passed when initialization and
then, kay.conf.global_settings; see the global settings file for a
list of all possible variables.

:Copyright: (c) 2011 Ian Lewis <ianmlewis@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import re
import time

from google.appengine.ext import db
from google.appengine.api import memcache

_missing = type('MissingType', (), {'__repr__': lambda x: 'missing'})()

_DEFAULT_TTL = 60

class LiveSettings(object):
  """
  The LiveSettings class is managages persistent global settings
  much like those in settings.py but which can be modified without
  re-deploying an application.

  Things like enabling/disabling appstats or other middleware,
  can be done via live settings.

  Live settings are a string key to unicode text property pair.
  Settings are stored using a three-tiered approach first in
  an in-memory datastructure that is local to a single app instance,
  then as keys in memcached, then finally persistently
  in the datastore.
  
  During a set operation, the key is stored first in the
  datastore, then in memcached with no expiration, then finally
  in the in-memory cache local only to that instance.

  During a get operation the value is recieved from the in-memory
  cache, if missing it is subsequently retrieved from memcached or
  the datastore. Each in-memory key has an in-memory TTL
  which will cause the key to expire and for new values to be
  loaded from memcached during a get operation.

  Memcached keys may be evicted so the datastore is necessary to
  fully persist values.
  """

  def __init__(self):
    self._settings_cache = {}

  def set(self, key, value, expire=_DEFAULT_TTL):
    from kay.ext.live_settings.models import KayLiveSetting

    new_setting = KayLiveSetting(
        key_name=key,
        ttl=expire,
        value=value,
    )
    new_setting.put()

    # Set the memcached key to never expire. It only expires
    # if it is evicted from memory. TTLs are handled by the 
    # in-memory cache.
    memcache.set("kay:live:%s" % key, (value, expire))
    self._settings_cache[key] = (value, int(time.time())+expire, expire)

    return new_setting

  def set_multi(self, data, expire=_DEFAULT_TTL):
    from kay.ext.live_settings.models import KayLiveSetting

    data_items = data.items()
    db.put(map(lambda k,v: KayLiveSetting(key_name=k, ttl=expire, value=v),
        data_items))
    memcache.set_multi(dict(map(lambda k,v: ("kay:live:%s" % k, (v,expire)),data_items)))

    expire_time = int(time.time())+expire
    for key, value in data_items:
      self._settings_cache[key] = (value, expire_time, expire)

  def get(self, key, default=None):
    from kay.ext.live_settings.models import KayLiveSetting

    set_dictcache = False
    set_memcache = False

    value,expire,ttl = self._settings_cache.get(key,
                                        (_missing, _missing, _missing))

    if value is _missing or expire < time.time():
      set_dictcache = True
      value = memcache.get("kay:live:%s" % key)
      if value:
        value,ttl = value
      else:
        value,ttl = (_missing, _missing)
    if value is _missing:
      set_memcache = True
      entity = KayLiveSetting.get_by_key_name(key)
      if entity:
        value = entity.value or _missing
        ttl = entity.ttl or _missing

    if value is _missing:
      return default
    else:
      if ttl is None or ttl is _missing:
        ttl = _DEFAULT_TTL 
      if set_dictcache:
        self._settings_cache[key] = (value, time.time()+ttl, ttl)
      if set_memcache:
        memcache.set("kay:live:%s" % key, (value, ttl))

      return value

  def get_multi(self, keys):
    # For the time being just do a bunch of gets to ensure
    # we get the same value as the get() method.
    # TODO: Make this more efficient
    return dict(map(lambda k: (k,self.get(k)), keys))

  def delete(self, key):
    from kay.ext.live_settings.models import KayLiveSetting
    setting = KayLiveSetting.get_by_key_name(key)
    if setting:
        setting.delete()
    memcache.delete("kay:live:%s" % key)
    if key in self._settings_cache:
        del self._settings_cache[key]

  def keys(self):
    from kay.ext.live_settings.models import KayLiveSetting
    return map(lambda e: e.key().name(), KayLiveSetting.all())

  def items(self):
    # For the time being just do a multi_get to ensure 
    # we get the same value as the get() method.
    # TODO: Make this more efficient
    return self.multi_get(self.keys()).items()

live_settings = LiveSettings()
