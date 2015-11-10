Kay is a web framework made specifically for Google App Engin The basic design of Kay is based on the Django framework, like middleware, settings and pluggable application, etc. Kay uses Werkzeug as lower level framework, Jinja2 as template engine, and babel for handling language translations. This software is distributed under BSD license. See LICENSE for more details. See README for quickstart.

Kay stands for "Kay makes Appengine Yummy".

Kay has these features out of the box:

  * Anonymous session
  * Authentication
    * Google Authentication
    * Authentication against credentials stored in the datastore
  * Cache mechanism
  * Jinja2 templates system bundled
  * WSGI debug middleware bundled (werkzeug)
  * i18n capability
  * Powerful shell tools (iPython powered if installed)
    * including dump/restore capability with a single command
  * flash message (instant messaging across different request)
  * allows apps to load modules lazily
  * Model driven RESTful API auto generation
  * Model driven CRUD+list auto generation
  * A new authentication backend for OpenID, OAuth, Facebook connect
    * You can also write apps for Google Apps Market Place easily
  * A brand new URL mapping syntax that is more intuitable than before
    * http://kay-docs.shehas.net/urlmapping.html#introducing-a-new-interface-for-urlmapping
  * Added some useful properties such as OwnerProperty
  * Fully functional test helper
    * A new test runner allows you to
      * run your tests by web browser
      * run your tests on production environment
    * detailed instruction is available at:
> > > http://takashi-matsuo.blogspot.com/2010/05/now-kay-framework-has-gaetestbase.html
  * Now you can add your own management script
  * Nuke is bundled in Kay now.
    * Nuke is a small web handler for wiping the datastore completely
    * Nuke is hosted at: http://code.google.com/p/jobfeed/wiki/Nuke
    * Detailed instructions:
> > > http://kay-docs.shehas.net/extensions.html#module-kay.ext.nuke

In spite of these variety of features, kay still keeps reasonably fast by the lazy loading feature mentioned before.

IRC channel:
  * [irc://irc.freenode.net/#kay-users](irc://irc.freenode.net/#kay-users) (English)
  * [irc://irc.freenode.net/#kay-ja](irc://irc.freenode.net/#kay-ja) (Japanese)

It seems that I'm always on above channels, but mainly I'm awake during the daytime in Tokyo(JST +0900).