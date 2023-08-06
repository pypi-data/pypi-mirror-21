.. image:: banner.png
    :align: center


----

Python package to connect to `blitz.js framework
<https://github.com/nexus-devs/blitz.js/>`_.

----

Installation
------------
:code:`pip install blitz_js_query`

Usage
-----
.. code-block:: python

    from blitz_js_query.blitz import Blitz

    blitz_api = Blitz({
        "api_url": "https://api.nexus-stats.com",
        "api_port": "443"
    })
    blitz_api.get("/foo").then(lambda res: print(res))
    # Result: {'statusCode': 200, 'sent': True, 'body': 'bar'}

Configuration
-------------
.. code-block:: python

    # Default options
    options = {
        # Resource config
        "api_url": "http://localhost",
        "api_port": "3010",
        "auth_url": "http://localhost:3030/",

        # Connection Config
        "use_socket": True,
        "namespace": LoggingNamespace,

        # Authorization Config
        "user_key": None,
        "user_secret": None,
        "ignore_limiter": False
    }

    blitz_api = Blitz(options)