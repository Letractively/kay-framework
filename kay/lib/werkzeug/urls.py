# -*- coding: utf-8 -*-
"""
    werkzeug.urls
    ~~~~~~~~~~~~~

    This module implements various URL related functions.

    :copyright: (c) 2009 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import urlparse

from werkzeug._internal import _decode_unicode


#: list of characters that are always safe in URLs.
_always_safe = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         'abcdefghijklmnopqrstuvwxyz'
                         '0123456789_.-')

#: lookup table for encoded characters.
_hextochr = dict(('%02x' % i, chr(i)) for i in xrange(256))
_hextochr.update(('%02X' % i, chr(i)) for i in xrange(256))


def _quote(s, safe='/', _quotechar='%%%02X'.__mod__):
    assert isinstance(s, str), 'quote only works on bytes'
    safe = _always_safe | set(safe)
    rv = list(s)
    for idx, char in enumerate(s):
        if char not in safe:
            rv[idx] = _quotechar(ord(char))
    return ''.join(rv)


def _quote_plus(s, safe=''):
    if ' ' in s:
        return _quote(s, safe + ' ').replace(' ', '+')
    return _quote(s, safe)


def _unquote(s, unsafe=''):
    assert isinstance(s, str), 'unquote only works on bytes'
    unsafe = set(unsafe)
    rv = s.split('%')
    for i in xrange(1, len(rv)):
        item = rv[i]
        try:
            char = _hextochr[item[:2]]
            if char in unsafe:
                raise KeyError()
            rv[i] = char + item[2:]
        except KeyError:
            rv[i] = '%' + item
    return ''.join(rv)


def _unquote_plus(s):
    return _unquote(s.replace('+', ' '))


def _uri_split(uri):
    """Splits up an URI or IRI."""
    scheme, netloc, path, query, fragment = urlparse.urlsplit(uri)

    port = None

    if '@' in netloc:
        auth, hostname = netloc.split('@', 1)
    else:
        auth = None
        hostname = netloc
    if hostname:
        if ':' in hostname:
            hostname, port = hostname.split(':', 1)
    return scheme, auth, hostname, port, path, query, fragment


def iri_to_uri(iri, charset='utf-8'):
    r"""Converts any unicode based IRI to an acceptable ASCII URI.  Werkzeug
    always uses utf-8 URLs internally because this is what browsers and HTTP
    do as well.  In some places where it accepts an URL it also accepts a
    unicode IRI and converts it into a URI.

    Examples for IRI versus URI:

    >>> iri_to_uri(u'http://☃.net/')
    'http://xn--n3h.net/'
    >>> iri_to_uri(u'http://üser:pässword@☃.net/påth')
    'http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th'

    .. versionadded:: 0.6

    :param iri: the iri to convert
    :param charset: the charset for the URI
    """
    iri = unicode(iri)
    scheme, auth, hostname, port, path, query, fragment = _uri_split(iri)

    scheme = scheme.encode('ascii')
    hostname = hostname.encode('idna')
    if auth:
        if ':' in auth:
            auth, password = auth.split(':', 1)
        else:
            password = None
        auth = _quote(auth.encode(charset))
        if password:
            auth += ':' + _quote(password.encode(charset))
        hostname = auth + '@' + hostname
    if port:
        hostname += ':' + port

    path = _quote(path.encode(charset), safe="/:~+")
    query = _quote(query.encode(charset), safe="=%&[]:;$()+,!?*/")

    return urlparse.urlunsplit([scheme, hostname, path, query, fragment])


def uri_to_iri(uri, charset='utf-8', errors='ignore'):
    r"""Converts a URI in a given charset to a IRI.

    Examples for URI versus IRI

    >>> uri_to_iri('http://xn--n3h.net/')
    u'http://\u2603.net/'
    >>> uri_to_iri('http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th')
    u'http://\xfcser:p\xe4ssword@\u2603.net/p\xe5th'

    Query strings are left unchanged:

    >>> uri_to_iri('/?foo=24&x=%26%2f')
    u'/?foo=24&x=%26%2f'

    .. versionadded:: 0.6

    :param uri: the URI to convert
    :param charset: the charset of the URI
    :param errors: the error handling on decode
    """
    uri = url_fix(str(uri), charset)
    scheme, auth, hostname, port, path, query, fragment = _uri_split(uri)

    scheme = _decode_unicode(scheme, 'ascii', errors)

    try:
        hostname = hostname.decode('idna')
    except UnicodeError:
        # dammit, that codec raised an error.  Because it does not support
        # any error handling we have to fake it.... badly
        if errors not in ('ignore', 'replace'):
            raise
        hostname = hostname.decode('ascii', errors)

    if auth:
        if ':' in auth:
            auth, password = auth.split(':', 1)
        else:
            password = None
        auth = _decode_unicode(_unquote(auth), charset, errors)
        if password:
            auth += u':' + _decode_unicode(_unquote(password),
                                           charset, errors)
        hostname = auth + u'@' + hostname
    if port:
        # port should be numeric, but you never know...
        hostname += u':' + port.decode(charset, errors)

    path = _decode_unicode(_unquote(path, '/;?'), charset, errors)
    query = _decode_unicode(_unquote(query, ';/?:@&=+,$'),
                            charset, errors)

    return urlparse.urlunsplit([scheme, hostname, path, query, fragment])


def url_decode(s, charset='utf-8', decode_keys=False, include_empty=True,
               errors='ignore', separator='&', cls=None):
    """Parse a querystring and return it as :class:`MultiDict`.  Per default
    only values are decoded into unicode strings.  If `decode_keys` is set to
    `True` the same will happen for keys.

    Per default a missing value for a key will default to an empty key.  If
    you don't want that behavior you can set `include_empty` to `False`.

    Per default encoding errors are ignored.  If you want a different behavior
    you can set `errors` to ``'replace'`` or ``'strict'``.  In strict mode a
    `HTTPUnicodeError` is raised.

    .. versionchanged:: 0.5
       In previous versions ";" and "&" could be used for url decoding.
       This changed in 0.5 where only "&" is supported.  If you want to
       use ";" instead a different `separator` can be provided.

       The `cls` parameter was added.

    :param s: a string with the query string to decode.
    :param charset: the charset of the query string.
    :param decode_keys: set to `True` if you want the keys to be decoded
                        as well.
    :param include_empty: Set to `False` if you don't want empty values to
                          appear in the dict.
    :param errors: the decoding error behavior.
    :param separator: the pair separator to be used, defaults to ``&``
    :param cls: an optional dict class to use.  If this is not specified
                       or `None` the default :class:`MultiDict` is used.
    """
    if cls is None:
        cls = MultiDict
    result = []
    for pair in str(s).split(separator):
        if not pair:
            continue
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key = pair
            value = ''
        key = _unquote_plus(key)
        if decode_keys:
            key = _decode_unicode(key, charset, errors)
        result.append((key, url_unquote_plus(value, charset, errors)))
    return cls(result)


def url_encode(obj, charset='utf-8', encode_keys=False, sort=False, key=None,
               separator='&'):
    """URL encode a dict/`MultiDict`.  If a value is `None` it will not appear
    in the result string.  Per default only values are encoded into the target
    charset strings.  If `encode_keys` is set to ``True`` unicode keys are
    supported too.

    If `sort` is set to `True` the items are sorted by `key` or the default
    sorting algorithm.

    .. versionadded:: 0.5
        `sort`, `key`, and `separator` were added.

    :param obj: the object to encode into a query string.
    :param charset: the charset of the query string.
    :param encode_keys: set to `True` if you have unicode keys.
    :param sort: set to `True` if you want parameters to be sorted by `key`.
    :param separator: the separator to be used for the pairs.
    :param key: an optional function to be used for sorting.  For more details
                check out the :func:`sorted` documentation.
    """
    if isinstance(obj, MultiDict):
        items = obj.lists()
    elif isinstance(obj, dict):
        items = []
        for k, v in obj.iteritems():
            if not isinstance(v, (tuple, list)):
                v = [v]
            items.append((k, v))
    else:
        items = obj or ()
    if sort:
        items.sort(key=key)
    tmp = []
    for key, values in items:
        if encode_keys and isinstance(key, unicode):
            key = key.encode(charset)
        else:
            key = str(key)
        for value in values:
            if value is None:
                continue
            elif isinstance(value, unicode):
                value = value.encode(charset)
            else:
                value = str(value)
            tmp.append('%s=%s' % (_quote(key),
                                  _quote_plus(value)))
    return separator.join(tmp)


def url_quote(s, charset='utf-8', safe='/:'):
    """URL encode a single string with a given encoding.

    :param s: the string to quote.
    :param charset: the charset to be used.
    :param safe: an optional sequence of safe characters.
    """
    if isinstance(s, unicode):
        s = s.encode(charset)
    elif not isinstance(s, str):
        s = str(s)
    return _quote(s, safe=safe)


def url_quote_plus(s, charset='utf-8', safe=''):
    """URL encode a single string with the given encoding and convert
    whitespace to "+".

    :param s: the string to quote.
    :param charset: the charset to be used.
    :param safe: an optional sequence of safe characters.
    """
    if isinstance(s, unicode):
        s = s.encode(charset)
    elif not isinstance(s, str):
        s = str(s)
    return _quote_plus(s, safe=safe)


def url_unquote(s, charset='utf-8', errors='ignore'):
    """URL decode a single string with a given decoding.

    Per default encoding errors are ignored.  If you want a different behavior
    you can set `errors` to ``'replace'`` or ``'strict'``.  In strict mode a
    `HTTPUnicodeError` is raised.

    :param s: the string to unquote.
    :param charset: the charset to be used.
    :param errors: the error handling for the charset decoding.
    """
    if isinstance(s, unicode):
        s = s.encode(charset)
    return _decode_unicode(_unquote(s), charset, errors)


def url_unquote_plus(s, charset='utf-8', errors='ignore'):
    """URL decode a single string with the given decoding and decode
    a "+" to whitespace.

    Per default encoding errors are ignored.  If you want a different behavior
    you can set `errors` to ``'replace'`` or ``'strict'``.  In strict mode a
    `HTTPUnicodeError` is raised.

    :param s: the string to unquote.
    :param charset: the charset to be used.
    :param errors: the error handling for the charset decoding.
    """
    return _decode_unicode(_unquote_plus(s), charset, errors)


def url_fix(s, charset='utf-8'):
    r"""Sometimes you get an URL by a user that just isn't a real URL because
    it contains unsafe characters like ' ' and so on.  This function can fix
    some of the problems in a similar way browsers handle data entered by the
    user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param s: the string with the URL to fix.
    :param charset: The target charset for the URL if the url was given as
                    unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = _quote(path, '/%')
    qs = _quote_plus(qs, ':&%=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


class Href(object):
    """Implements a callable that constructs URLs with the given base. The
    function can be called with any number of positional and keyword
    arguments which than are used to assemble the URL.  Works with URLs
    and posix paths.

    Positional arguments are appended as individual segments to
    the path of the URL:

    >>> href = Href('/foo')
    >>> href('bar', 23)
    '/foo/bar/23'
    >>> href('foo', bar=23)
    '/foo/foo?bar=23'

    If any of the arguments (positional or keyword) evaluates to `None` it
    will be skipped.  If no keyword arguments are given the last argument
    can be a :class:`dict` or :class:`MultiDict` (or any other dict subclass),
    otherwise the keyword arguments are used for the query parameters, cutting
    off the first trailing underscore of the parameter name:

    >>> href(is_=42)
    '/foo?is=42'
    >>> href({'foo': 'bar'})
    '/foo?foo=bar'

    Combining of both methods is not allowed:

    >>> href({'foo': 'bar'}, bar=42)
    Traceback (most recent call last):
      ...
    TypeError: keyword arguments and query-dicts can't be combined

    Accessing attributes on the href object creates a new href object with
    the attribute name as prefix:

    >>> bar_href = href.bar
    >>> bar_href("blub")
    '/foo/bar/blub'

    If `sort` is set to `True` the items are sorted by `key` or the default
    sorting algorithm:

    >>> href = Href("/", sort=True)
    >>> href(a=1, b=2, c=3)
    '/?a=1&b=2&c=3'

    .. versionadded:: 0.5
        `sort` and `key` were added.
    """

    def __init__(self, base='./', charset='utf-8', sort=False, key=None):
        if not base:
            base = './'
        self.base = base
        self.charset = charset
        self.sort = sort
        self.key = key

    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)
        base = self.base
        if base[-1:] != '/':
            base += '/'
        return Href(urlparse.urljoin(base, name), self.charset, self.sort,
                    self.key)

    def __call__(self, *path, **query):
        if path and isinstance(path[-1], dict):
            if query:
                raise TypeError('keyword arguments and query-dicts '
                                'can\'t be combined')
            query, path = path[-1], path[:-1]
        elif query:
            query = dict([(k.endswith('_') and k[:-1] or k, v)
                          for k, v in query.items()])
        path = '/'.join([url_quote(x, self.charset) for x in path
                         if x is not None]).lstrip('/')
        rv = self.base
        if path:
            if not rv.endswith('/'):
                rv += '/'
            rv = urlparse.urljoin(rv, path)
        if query:
            rv += '?' + url_encode(query, self.charset, sort=self.sort,
                                   key=self.key)
        return str(rv)


# circular dependencies
from werkzeug.datastructures import MultiDict
