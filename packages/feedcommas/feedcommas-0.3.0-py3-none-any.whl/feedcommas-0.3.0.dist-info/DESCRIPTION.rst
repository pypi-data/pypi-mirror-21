Feed Commas
===========

**WARNING**: Feed Commas is currently unstable. It means that there ARE still
ongoing interface changes and after version upgrade you might lose some or all
of your local RSS data.

Feed Commas is a client application for CommaFeed, a Google Reader inspired
self-hosted RSS reader (with its instance running on commafeed.com).

It's a terminal application, but with user-friendly, curses-based graphical
frontend. It looks like this, but with more colors:

.. code::

  ┌────────────────────────────────────────────────────────────────────────────┐
  │All                  │┌────────────────────────────────────────────────────┐│
  │Starred              ││How to make `lynx` fast?    Tue Mar  7 10:52:00 2017││
  │Daily read           ││                                                    ││
  │  /r/commandline(1)  ││   Anyone care share their lynx config?             ││
  │  Lorem ipsum        ││   For some reason, lynx on my computer cannot open ││
  │  The Codist         ││websites instantly.                                 ││
  │  Andrzej's C++ blog ││                                                    ││
  │  Ludic Linux        ││☐                          submitted by /u/blablabla││
  │Comics               │└────────────────────────────────────────────────────┘│
  │  MonkeyUser         │┌────────────────────────────────────────────────────┐│
  │  Geek&Poke          ││Lorem ipsum                 Mon Mar  6 23:52:14 2017││
  │  xkcd               ││                                                    ││
  │                     ││   Lorem ipsum dolor sit amet.                      ││
  │                     ││                                                    ││
  │                     ││★☑                                            author││
  │                     │└────────────────────────────────────────────────────┘│
  │                                                                            │
  │:show-unread                                                                │
  └────────────────────────────────────────────────────────────────────────────┘

For instructions on installation and usage, see the manual (in docs directory).
You can build HTML version of it by running:

.. code:: shell

    $ cd docs && make

Manual for the latest release is also available online at
http://pythonhosted.org/feedcommas/.


