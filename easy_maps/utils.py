# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured


def importpath(path, error_text=None):
    """
    Import value by specified ``path``.
    Value can represent module, class, object, attribute or method.
    If ``error_text`` is not None and import will
    raise ImproperlyConfigured with user friendly text.

    """
    result = None
    attrs = []
    parts = path.split('.')
    exception = None
    while parts:
        try:
            result = __import__('.'.join(parts), {}, {}, [''])
        except ImportError as e:
            if exception is None:
                exception = e
            attrs = parts[-1:] + attrs
            parts = parts[:-1]
        else:
            break
    for attr in attrs:
        try:
            result = getattr(result, attr)
        except (AttributeError, ValueError) as e:
            if error_text is not None:
                raise ImproperlyConfigured('Error: %s can import "%s"' % (
                    error_text, path))
            else:
                raise exception
    return result
