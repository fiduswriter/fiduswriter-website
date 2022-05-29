FidusWriter-Publish
=================

FidusWriter-Publish is a Fidus Writer plugin to allow for makign documents available
directly to the general public from within Fidus Writer.

**NOTE: This plugin is alphaware and is not currentlyt ready to be used.**


Installation
------------

1) Install Fidus Writer like this:

    pip install fiduswriter[publish]

2) Add "book" to your INSTALLED_APPS setting in the
   configuration.py file like this::

    INSTALLED_APPS += (
        ...
        'publish',
    )

3) Run ``fiduswriter setup`` to create the needed database tables and to create the needed JavaScript files.

4) (Re)start your Fidus Writer server
