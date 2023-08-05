=====================
Outlyer plugin helper
=====================

A set of helper functions for using in Outlyer Python plugins

Adding the following two lines near the top of your plugin will automatically
patch the code to work against containers as well as hosts:

..  code-block:: python

    from outlyer.plugin_helper.container import patch_all
    patch_all()
