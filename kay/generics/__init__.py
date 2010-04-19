# -*- coding: utf-8 -*-

"""
Kay generics.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from string import Template

from werkzeug.routing import (
  Rule, RuleTemplate, EndpointPrefix, Submount,
)
from werkzeug.exceptions import (
  NotFound, Forbidden
)
from werkzeug import (
  Response, redirect
)

from kay.utils import (
  render_to_response, url_for
)
from kay.utils.flash import (
  set_flash, get_flash
)
from kay.exceptions import NotAuthorized
from kay.i18n import gettext as _
from kay.routing import ViewGroup

endpoints = {
  'list': "list_$model",
  'show': "show_$model",
  'create': "create_$model",
  'update': "update_$model",
  'delete': "delete_$model",
}

OPE_LIST = 'list'
OPE_SHOW = 'show'
OPE_CREATE = 'create'
OPE_UPDATE = 'update'
OPE_DELETE = 'delete'

def only_owner_can_write(self, request, operation, obj=None):
  if operation == OPE_CREATE:
    if request.user.is_anonymous():
      raise NotAuthorized()
  elif operation == OPE_UPDATE or operation == OPE_DELETE:
    owner = getattr(obj, self.owner_attr)
    if owner != request.user:
      raise NotAuthorized()

class CRUDViewGroup(ViewGroup):
  entities_per_page = 20
  templates = {
    OPE_LIST: '_internal/general_list.html',
    OPE_SHOW: '_internal/general_show.html',
    OPE_UPDATE: '_internal/general_update.html',
  }
  forms = {}
  form = None
  owner_attr = None
  rule_template = RuleTemplate([
    Rule('/$model/list', endpoint=endpoints[OPE_LIST]),
    Rule('/$model/list/<cursor>', endpoint=endpoints[OPE_LIST]),
    Rule('/$model/show/<key>', endpoint=endpoints[OPE_SHOW]),
    Rule('/$model/create', endpoint=endpoints[OPE_CREATE]),
    Rule('/$model/update/<key>', endpoint=endpoints[OPE_UPDATE]),
    Rule('/$model/delete/<key>', endpoint=endpoints[OPE_DELETE]),
  ])

  def __init__(self, model=None, **kwargs):
    super(CRUDViewGroup, self).__init__(**kwargs)
    self.model = model or self.model
    self.model_name = self.model.__name__
    self.model_name_lower = self.model_name.lower()

  def get_additional_context_on_create(self, request, form):
    if self.owner_attr:
      if request.user.is_anonymous():
        owner = None
      else:
        owner = request.user.key()
      return {self.owner_attr: owner}
    else:
      return {}

  def get_additional_context_on_update(self, request, form):
    return {}

  def get_query(self, request):
    if hasattr(self.model, 'created'):
      return self.model.all().order('-created')
    else:
      return self.model.all()

  def get_template(self, request, name):
    return self.templates[name]

  def get_form(self, request, name):
    try:
      return self.forms[name]
    except KeyError:
      return self.form

  def get_list_url(self, cursor=None):
    return url_for(self.get_endpoint(OPE_LIST), cursor=cursor)

  def get_detail_url(self, obj):
    return url_for(self.get_endpoint(OPE_SHOW), key=obj.key())

  def get_delete_url(self, obj):
    return url_for(self.get_endpoint(OPE_DELETE), key=obj.key())

  def get_update_url(self, obj):
    return url_for(self.get_endpoint(OPE_UPDATE), key=obj.key())

  def get_create_url(self):
    return url_for(self.get_endpoint(OPE_CREATE))

  def url_processor(self, request):
    return {'list_url': self.get_list_url,
            'detail_url': self.get_detail_url,
            'delete_url': self.get_delete_url,
            'update_url': self.get_update_url,
            'create_url': self.get_create_url}

  def authorize(self, request, operation, obj=None):
    """ Raise AuthorizationError when the operation is not permitted.
    """
    return True

  def check_authority(self, request, operation, obj=None):
    try:
      self.authorize(request, operation, obj)
    except NotAuthorized, e:
      from kay.conf import settings
      if 'kay.auth.middleware.AuthenticationMiddleware' in \
            settings.MIDDLEWARE_CLASSES and \
            request.user.is_anonymous():
        from kay.utils import create_login_url
        return redirect(create_login_url(request.url))
      else:
        raise Forbidden("Access not allowed.")

  def list(self, request, cursor=None):
    # TODO: bi-directional pagination instead of one way ticket forward
    ret = self.check_authority(request, OPE_LIST)
    if ret:
      return ret
    q = self.get_query(request)
    if cursor:
      q = q.with_cursor(cursor)
    entities = q.fetch(self.entities_per_page)
    next_cursor = q.cursor()
    q = q.with_cursor(next_cursor)
    if q.get() is None:
      next_cursor = None
    return render_to_response(self.get_template(request, OPE_LIST),
                              {'model': self.model_name,
                               'entities': entities,
                               'cursor': next_cursor,
                               'message': get_flash(),
                              },
                              processors=(self.url_processor,))

  def show(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    try:
      entity = self.model.get(key)
    except BadKeyError:
      # just ignore it
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    ret = self.check_authority(request, OPE_SHOW, entity)
    if ret:
      return ret
    return render_to_response(self.get_template(request, OPE_SHOW),
                              {'entity': entity,
                               'model': self.model_name},
                              processors=(self.url_processor,))

  def create_or_update(self, request, key=None):
    from google.appengine.api.datastore_errors import BadKeyError
    if key:
      try:
        entity = self.model.get(key)
      except BadKeyError:
        entity = None
      if entity is None:
        raise NotFound("Specified %s not found." % self.model_name)
      form_class = self.get_form(request, OPE_UPDATE)
      form = form_class(instance=entity)
      title = _("Updating a %s entity") % self.model_name
      ret = self.check_authority(request, OPE_UPDATE, entity)
      if ret:
        return ret
    else:
      form_class = self.get_form(request, OPE_CREATE)
      form = form_class()
      title = _("Creating a new %s") % self.model_name
      ret = self.check_authority(request, OPE_CREATE)
      if ret:
        return ret
    if request.method == 'POST':
      if form.validate(request.form, request.files):
        if key:
          additional_context = self.get_additional_context_on_update(request,
                                                                     form)
          message = _("An entity is updated successfully.")
        else:
          additional_context = self.get_additional_context_on_create(request,
                                                                     form)
          message = _("A new entity is created successfully.")
        new_entity = form.save(**additional_context)
        set_flash(message)
        return redirect(self.get_list_url())
    return render_to_response(self.get_template(request, OPE_UPDATE),
                              {'form': form.as_widget(),
                               'title': title,
                               },
                              processors=(self.url_processor,))

  def create(self, *args, **kwargs):
    return self.create_or_update(*args, **kwargs)

  def update(self, *args, **kwargs):
    return self.create_or_update(*args, **kwargs)

  def delete(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    try:
      entity = self.model.get(key)
    except BadKeyError:
      # just ignore it
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    ret = self.check_authority(request, OPE_DELETE, entity)
    if ret:
      return ret
    entity.delete()
    set_flash(_("An entity is deleted successfully."))
    # TODO: back to original page
    return redirect(self.get_list_url())
    
  def _get_rules(self):
    return [self.rule_template(model=self.model_name_lower)]

  def _get_views(self, prefix=None):
    self.prefix = prefix
    ret = {}
    for key, val in endpoints.iteritems():
      s = Template(val)
      endpoint = s.substitute(model=self.model_name_lower)
      if prefix:
        endpoint = prefix+endpoint
      ret[endpoint] = getattr(self, key)
    return ret

  def get_endpoint(self, key):
    endpoint = Template(endpoints[key]).substitute(model=self.model_name_lower)
    if self.prefix:
      endpoint = self.prefix+endpoint
    return endpoint
