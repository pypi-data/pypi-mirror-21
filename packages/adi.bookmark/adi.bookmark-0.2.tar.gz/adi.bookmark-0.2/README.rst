Introduction
============

Provide a bookmarklet for storing bookmarks as an Archetype-based link-item to
a given Plone-folder.


Why
---

Craved for a quick way to store interesting site-addresses to my Plonesite.


What
----

Provide a bookmarklet which, when clicked, will:

- Transfer the currently watched URL and store it as a link-item.

- Use the current Linux-date in seconds as the id for the link.

- Use the current window's title as the link-title, if not given falls back
  to the part of the URL after its last slash.

- Offer the user a prompt to enter an additional description and give a chance
  to cancel the whole operation.


How
---

Install this add-on to a Plone-site and call the folder where you want to store
bookmarks to, append '/adi_bookmark' to the URL in your browser, drag'n'drop
the offered link to your browser's bookmark-bar.

Optionally, you can get the bookmarklet without installing, from:
http://euve4703.vserver.de:8080/adi/static/public/repos/github/ida/adi.bookmark/adi/bookmark/skins/adi_bookmark/adi_bookmark.pt
There enter the Plone-folder-destination before drag'n'dropping the link.


Now, anytime you'll click that bookmarklet, it'll redirect you to the Plone-folder
and store the former watched URL as a link.


Caveats
-------

It is very unlikely but possible, that the generated link-id of the current
date could be taken already, however we (meh, myself and their royal majesties)
decided to take that risk. If the id exists already, the existing object would
be overwritten, possibly unintended, thy had been warned.


TODO
----

- Decode strings before passing as URL-params. Special characters will likely
  blow things up, not tested, yet.

- Support keywords a.k.a. tags.

