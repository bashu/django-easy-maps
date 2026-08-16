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
    parts = path.split(".")
    exception = None
    while parts:
        try:
            result = __import__(".".join(parts), {}, {}, [""])
        except ImportError as exc:  # noqa: PERF203
            if exception is None:
                exception = exc
            attrs = parts[-1:] + attrs
            parts = parts[:-1]
        else:
            break
    try:
        for attr in attrs:
            result = getattr(result, attr)
    except (AttributeError, ValueError) as exc:
        if error_text is not None:
            msg = f'Error: {error_text} can import "{path}"'
            raise ImproperlyConfigured(msg) from exc
        raise exception from exc
    return result
