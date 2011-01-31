Python EasyRec Binding for REST API
===================================

This package is almost entirely untested.  Use with caution.

What Works
----------

* **`signin`**: Sign into an EasyRec server to get a security token.

### Actions:

* **`view`**: Register an item `view` in a given user session.
* **`buy`**: Register an item `buy` by a given user.
* **`rate`**: Register an item `rate` by a given user.

### Recommendations:

* **`otherusersalsoviewed`**: Get recommendations based on what other users also viewed.
* **`otherusersalsobought`**: Get recommendations based on what other users also bought.
* **`itemsratedgoodbyotherusers`**: Get recommendations based on what items were rated good by other users.
* **`recommendationsforuser`**: Get recommendations from the engine based on the `view`, `buy`, `rate`, and `importrule` history.

### Community Rankings:

* **`mostvieweditems`**: Get the most viewed items.
* **`mostboughtitems`**: Get the most bought items.
* **`mostrateditems`**: Get the most rated items.
* **`bestrateditems`**: Get the best rated items.
* **`worstrateditems`**: Get the worst rated items.

### Import API:

* **`importrule`**: Set weights between items manually.
* **`importitem`**: Import an item into EasyRec.

Dependencies
------------

This should work with Python 2.6.x and 2.7.x and requires no external dependencies.

Install
-------

Install as a standard distutils package:

    easy_install pyeasyrec

