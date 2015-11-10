## Kay-3.0.0 - June 7 2012 ##

  * This version is made specifically to Python2.7 runtime.

## Kay-1.1.0 - March 7th 2011 ##

  * Improved exception and error handling.
    * Added a new kay.ext.ereporter application for managing error reporting.
  * Added a new kay.ext.live\_settings application for managing global settings without having to reploy.
  * Added a new AppStatsMiddleware which can be used to enable appstats.
  * Added a new Pagination API
  * Added the COOKIE\_SECURE setting to support secure session cookies ([Issue #90](https://code.google.com/p/kay-framework/issues/detail?id=#90))
  * Added a new timezone\_functions context processor.
  * Added a new cron\_only view decorator for securing cron views.
  * Lazy load jinja2 so that requests that don't require jinja2 can return faster.
  * Updated google SDK taskqueue imports to import from the new package name.
  * Fixed an issue where the django module could not be loaded.

## Kay-1.0.1 - March 7th 2011 ##

  * Fixed an issue where error mails could not be sent to email addresses that were not specified as a developer in the admin console. ([Issue #50](https://code.google.com/p/kay-framework/issues/detail?id=#50))
  * Fixed an issue were the django module could not be imported after upgrading to the Appengine SDK 1.4.2 ([Issue #92](https://code.google.com/p/kay-framework/issues/detail?id=#92))
  * Fixed an issue where kay returned instances of the InternalServerError exception rather than an object that subclasses BaseResponse ([Issue #54](https://code.google.com/p/kay-framework/issues/detail?id=#54),#56)
  * Fixed an issue with the remote API and the HR datastore.
  * Updated imports to the taskqueue API so they use the new import path ([Issue #73](https://code.google.com/p/kay-framework/issues/detail?id=#73))

## Kay-1.0.0 - July 7th 2010 ##

  * Model driven RESTful API auto generation
  * Model driven CRUD+list auto generation
  * A new authentication backend for OpenID, OAuth, Facebook connect
    * You can also write apps for Google Apps MarketPlace easily
  * A brand new URL mapping syntax which is more intuitable than before: http://kay-docs.shehas.net/urlmapping.html#introducing-a-new-interface-for-urlmapping
  * Added some useful properties such as OwnerProperty
  * Fully functional test helper
    * A new test runner allows you to
      * run your tests by web browser
      * run your tests on production environment
  * Now you can add your own management script
  * Nuke is bundled in Kay now.
    * Nuke is a small web handler for wiping the datastore completely
    * Nuke is hosted at: http://code.google.com/p/jobfeed/wiki/Nuke
    * Detailed instructions: http://kay-docs.shehas.net/extensions.html#module-kay.ext.nuke
  * Many small improvements and bug fixes

## Kay-0.8.0 - March 31, 2010 ##

  * Added login\_box context processor and render\_loginbox macro to
> > kay.auth module.
  * Added a media\_compressor extension.
  * Improved a process for detecting user's preferred language.
  * Added a jsonrpc2 extension.
  * Improved db\_hook feature.
  * Added password changing/resetting capabilities.
  * Added a capability for changing entire settings according to the
> > host part of the URL.
  * Added a flash (quick indicator, not Adobe's flash) library
  * Added a handler for blobstore upload/download.
  * Added a registration application.
  * Allow defining class based handler as tuple which has (handler\_name, args, kwargs) style.
  * Allow disabling automount feature by setting None in APP\_MOUNT\_POINTS explicitly.
  * Added task\_handler for deferred library that corresponds with kay's rules.
  * Moved auth backend classes from kay.auth.backend module to kay.auth.backends package.
  * Various improvements.
  * Notice about this release
    * kay.auth.backend module is now deprecated. Please use
> > > kay.auth.backends package instead.

## Kay-0.3.0 - October 27, 2009 ##

  * Added CacheMiddleware, cache\_page decorator and FragmentCache jinja2 extension.
  * Added SecureCookieSessionStore.
  * Added handler for InboundMail
  * Capability for customizing Jinja2 environ
  * Now views can be defined as strings for lazy loading
  * Users can migrate data from an appid to another one very easily
  * Added kay.auth.GoogleBackend
  * More documentations available.
  * Added --all option to i18n related scripts.
  * Fixed testing environment was partially broken.
  * Allow users to choose a xhtml renderer for rendering forms.
  * More and more lazy loading of modules.
  * Notice about this release
    * GoogleAuthenticationMiddleware is obsolete. Please migrate it to AuthenticationMiddleware and GoogleBackend combination. See this URL for more details: http://kay-docs.shehas.net/auth.html#using-google-account-authentication
    * Changed options of some i18n related scripts. Please refer to
> > > URL bellow for more details:
> > > http://kay-docs.shehas.net/manage_py.html

## Kay-0.2.0 - September 23, 2009 ##

  * Added handers for XMPP
  * Added clear\_datastore action
  * Added create\_user action
  * Added dump\_all/restore\_all action
  * Added a capability for adding custom jinja2 filters
  * Added a capability for setting user's preffered language explicitly.
  * Documentation sites started.

## Kay-0.1.0 - August 27, 2009 ##

  * Added db\_hook feature.
  * Added zh\_TW translations.
  * Improved i18n mechanism.
  * Implemented authentication backend.
  * Fixed many bugs.
  * Changed the copyright declaration.

## Kay-0.0.0 - July 7, 2009 ##

  * First release.