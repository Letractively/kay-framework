# Introduction #

Live settings is a proposed change to kay to allow key value settings to be set without redeploying the application.

Live settings are maintained in two global dictionary objects, one for the keys and values and one which contains the TTL values for each key. The values are backed in memcache with keys that have an infinite TTL as well as in the datastore for durability. If a key expires in memory, memcache is first checked and if that fails the value is pulled from the datastore. When values are set, they are stored in the datastore as well as memcached.

Live settings can be changed via a live settings admin page in the appengine admin.

# Importing the settings object #

The live settings object is memcache like object that when queried returns the current value of the given setting.

```

from kay.conf.live import settings

# Get a value
mysetting = settings.get("mysetting")

# Set a value, default 60 second expiration
settings.set("mysetting", "value")

# Set a value with an expiration
settings.set("mysetting", "value", expire=60*5)

# Get all settings
settings.keys()

```

# Issues #

  * Since live settings depend on memcached and the datastore, settings will change based on the current namespace (should we always store them in the default namespace?)