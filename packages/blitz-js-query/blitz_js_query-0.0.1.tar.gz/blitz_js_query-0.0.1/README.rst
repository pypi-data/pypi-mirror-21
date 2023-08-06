.. image:: banner.png
    :align: center


----

Python package to connect to blitz.js framework

----

Installation
------------
:code:`pip install blitz_js_query`

Usage
-----
.. code:: python
    from blitz_js_query.blitz import Blitz

    blitz_api = Blitz({})
    blitz_api.get("http://localhost:3400/foo")