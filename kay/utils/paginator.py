# -*- coding: utf-8 -*-

from math import ceil

from werkzeug.utils import cached_property

__all__ = (
  'InvalidPage', 'PageNotAnInteger',
  'Paginator', 'Page',
  'InfinitePaginator', 'InfinitePage',
)

class InvalidPage(Exception):
  pass

class PageNotAnInteger(InvalidPage):
  pass

class EmptyPage(InvalidPage):
  pass

class Paginator(object):
  def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
    self.object_list = object_list
    self.per_page = per_page
    self.orphans = orphans
    self.allow_empty_first_page = allow_empty_first_page
    self._num_pages = self._count = None

  def validate_number(self, number):
    "Validates the given 1-based page number."
    try:
      number = int(number)
    except ValueError:
      raise PageNotAnInteger('That page number is not an integer')
    if number < 1:
      raise EmptyPage('That page number is less than 1')
    if number > self.num_pages:
      if number == 1 and self.allow_empty_first_page:
        pass
      else:
        raise EmptyPage('That page contains no results')
    return number

  def page(self, number):
    "Returns a Page object for the given 1-based page number."
    number = self.validate_number(number)
    bottom = (number - 1) * self.per_page
    top = bottom + self.per_page
    if top + self.orphans >= self.count:
      top = self.count
    return Page(self.object_list[bottom:top], number, self)

  def _get_count(self):
    "Returns the total number of objects, across all pages."
    if self._count is None:
      try:
        self._count = self.object_list.count()
      except (AttributeError, TypeError):
        # AttributeError if object_list has no count() method.
        # TypeError if object_list.count() requires arguments
        # (i.e. is of type list).
        self._count = len(self.object_list)
    return self._count
  count = property(_get_count)

  def _get_num_pages(self):
    "Returns the total number of pages."
    if self._num_pages is None:
      if self.count == 0 and not self.allow_empty_first_page:
        self._num_pages = 0
      else:
        hits = max(1, self.count - self.orphans)
        self._num_pages = int(ceil(hits / float(self.per_page)))
    return self._num_pages
  num_pages = property(_get_num_pages)

  def _get_page_range(self):
    """
    Returns a 1-based range of pages for iterating through within
    a template for loop.
    """
    return range(1, self.num_pages + 1)
  page_range = property(_get_page_range)

class Page(object):
  def __init__(self, object_list, number, paginator):
    self.object_list = object_list
    self.number = number
    self.paginator = paginator

  def __repr__(self):
    return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

  @property
  def has_next(self):
    return self.number < self.paginator.num_pages

  @property
  def has_previous(self):
    return self.number > 1

  @property
  def has_other_pages(self):
    return self.has_previous() or self.has_next()

  @property
  def next_page_number(self):
    return self.number + 1

  @property
  def previous_page_number(self):
    return self.number - 1

  @property
  def start_index(self):
    """
    Returns the 1-based index of the first object on this page,
    relative to total objects in the paginator.
    """
    # Special case, return zero if no items.
    if self.paginator.count == 0:
      return 0
    return (self.paginator.per_page * (self.number - 1)) + 1

  @property
  def end_index(self):
    """
    Returns the 1-based index of the last object on this page,
    relative to total objects found (hits).
    """
    # Special case for the last page because there can be orphans.
    if self.number == self.paginator.num_pages:
      return self.paginator.count
    return self.number * self.paginator.per_page

class InfinitePaginator(Paginator):
  """
  Paginator designed for cases when it's not important to know how many total
  pages.  This is useful for any object_list that has no count() method or can
  be used to improve performance for the datastore by removing counts.

  The orphans parameter has been removed for simplicity and there's a link
  template string for creating the links to the next and previous pages.
  """

  def __init__(self, object_list, per_page, allow_empty_first_page=True):
    orphans = 0 # no orphans
    super(InfinitePaginator, self).__init__(object_list, per_page, orphans,
        allow_empty_first_page)
    # no count or num pages
    del self._num_pages, self._count

  def validate_number(self, number):
    """
    Validates the given 1-based page number.
    """
    try:
      number = int(number)
    except ValueError:
      raise PageNotAnInteger('That page number is not an integer')
    if number < 1:
      raise EmptyPage('That page number is less than 1')
    return number

  def page(self, number):
    """
    Returns a Page object for the given 1-based page number.
    """
    number = self.validate_number(number)
    bottom = (number - 1) * self.per_page
    top = bottom + self.per_page
    page_items = self.object_list[bottom:top]
    # check moved from validate_number
    if not page_items:
      if number == 1 and self.allow_empty_first_page:
        pass
      else:
        raise EmptyPage('That page contains no results')
    return InfinitePage(page_items, number, self)

  def _get_count(self):
    """
    Returns the total number of objects, across all pages.
    """
    raise NotImplementedError
  count = property(_get_count)

  def _get_num_pages(self):
    """
    Returns the total number of pages.
    """
    raise NotImplementedError
  num_pages = property(_get_num_pages)

  def _get_page_range(self):
    """
    Returns a 1-based range of pages for iterating through within
    a template for loop.
    """
    raise NotImplementedError
  page_range = property(_get_page_range)

class InfinitePage(Page):

  def __repr__(self):
    return '<Page %s>' % self.number

  @cached_property
  def has_next(self):
    """
    Checks for one more item than last on this page.
    """
    try:
      next_item = self.paginator.object_list[
          self.number * self.paginator.per_page]
    except IndexError:
      return False
    return True

  @cached_property
  def start_index(self):
    """
    Returns the 1-based index of the first object on this page,
    relative to total objects in the paginator.
    """
    # Special case, return zero if no items.
    start_index = (self.paginator.per_page * (self.number - 1)) + 1
    try:
      first_item = self.paginator.object_list[start_index]
      return start_index
    except IndexError:
      return 0 

  @cached_property
  def end_index(self):
    """
    Returns the 1-based index of the last object on this page,
    relative to total objects found (hits).
    """
    return ((self.number - 1) * self.paginator.per_page +
        len(self.object_list))
