Example
=======

The example project uses `uv <https://docs.astral.sh/uv/>`_ and picks up
``easy_maps`` and its dependencies straight from the repository's
``pyproject.toml`` — no separate install step needed.

Get a Google Maps API key
--------------------------

The example needs a Google Maps API key to actually render a map instead of
falling back to Google's error box. To get one:

1. Create (or pick) a project at
   https://console.cloud.google.com/projectselector2/home
2. Enable billing for it at https://console.cloud.google.com/billing —
   required even to stay within the free tier, but new accounts get a
   $300 / 90-day trial credit and this example uses nowhere near it.
3. In *APIs & Services > Library*, enable all three APIs this project uses:

   * Geocoding API
   * Maps JavaScript API
   * Maps Static API

4. In *APIs & Services > Credentials*, create an API key. Leave it
   unrestricted (or IP-restricted) rather than HTTP-referrer-restricted —
   the geocoding call happens server-side, so a referrer restriction will
   silently deny it.

Run it
------

.. code-block:: bash

    export EASY_MAPS_GOOGLE_KEY="your-api-key-here"
    uv run example/manage.py migrate
    uv run example/manage.py runserver

Then open http://127.0.0.1:8000/.

For the admin site (http://127.0.0.1:8000/admin/), also run:

.. code-block:: bash

    uv run example/manage.py createsuperuser

Good luck!
