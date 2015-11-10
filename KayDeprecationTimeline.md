# Kay Deprecation Timeline #

This document outlines when various pieces of Kay will be removed, following their deprecation, as per the Kay deprecation policy.

## 1.5/2.0 ##

  * The HTTPException class in the werkzeug library will no longer have a "status\_code" property. This property is not included in the normal werkzeug distribution and was deprecated in Kay 1.1.
  * You will need to set your settings.DEFAULT\_MAIL\_FROM setting in order for error mails to be sent properly. Sending error mails using the first email address in the ADMINS setting was deprecated in Kay 1.1 and will no longer work.

## 1.2 ##

  * The kay.auth.backend module is deprecated. Please use kay.auth.backends package instead.
  * GoogleAuthenticationMiddleware? is obsolete. Please migrate it to AuthenticationMiddleware? and GoogleBackend? combination. See this URL for more details: http://kay-docs.shehas.net/auth.html#using-google-account-authentication