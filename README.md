FidusWriter-Website
===================

FidusWriter-Website is a Fidus Writer plugin to allow for making
documents available directly to the general public from within Fidus
Writer on the frontpage of Fidus Writer itself.

# Installation

1)  Install Fidus Writer like this:

    > pip install fiduswriter\[website\]

2)  Add "book" to your INSTALLED\_APPS setting in the configuration.py
    file like this:

        INSTALLED_APPS += (
            ...
            'website',
        )

3)  Run `fiduswriter setup` to create the needed database tables and to
    create the needed JavaScript files.

4)  (Re)start your Fidus Writer server

# Assign editor status

Assign editor status by giving users the permissions `website.change_publication` (to change existing posts on website) and/or `website.add_publication` (to add completely new posts to website).

By default, a group with both access rights is created with the name "Website Editors". You can add users to this group to obtain
the two types of access rights.

Super users will also be treated as editors.
