Python EasyRec Binding for REST API
===================================

What Works
----------

* **`signin`**: Sign into an EasyRec server to get a security token.
* **`importitem`**: Import an item into EasyRec.
* **`importrule`**: Set weights between items manually.
* **`view`**: Register an item `view` in a given user session.
* **`buy`**: Register an item `buy` by a given user.
* **`rate`**: Register an item `rate` by a given user.
* **`recommendationsforuser`**: Get recommendations from the engine based on the `view`, `buy`, `rate`, and `importrule` history.

Dependencies
------------

This should work with Python 2.6.x and 2.7.x and requires no external dependencies.

Install
-------
Put `easyrec.py` on your PYTHONPATH.  I am planning on creating a setuptools package soon.

