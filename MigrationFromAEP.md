# Howtos for migrating your AEP applications to Kay

# Introduction #

Here are some considerations about how to migrate AEP applications to Kay.

# Things you have to care about #

  * Forms
> > kay.utils.forms module is slightly different from AEP. kay.utils.forms.modelform is a module for autogenerating forms from model definition. Please refer to the [official documentation](http://kay-docs.shehas.net/forms-usage.html) for a typical usage of forms module. Syntax and usage is slightly different.

  * User
> > Significant differences. Likely easiest route is to export your user model data from AEP and import into kay models.

  * render\_to\_response/direct\_to\_template
> > Almost identical in kay.

  * Http utils
> > Almost identical in kay. Symbol names are slightly different from AEP.

  * RequestContext
> > Very similar functionality in kay.

  * URL Mapping
> > Completely different.  You'll need to re-write your urls.py to match kay's format.

  * Auth
> > Almost identical in kay.  Some syntax differences.

  * Request/Response object
> > Significant differences. Please refer to the [documentation](http://kay-docs.shehas.net/request_response.html).