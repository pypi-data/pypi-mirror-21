Ducker
======

What the duck is Ducker?
------------------------

Ducker is a lightweight program that makes internet searches with DuckDuckGo
from the command line. It can display the search results in your terminal or
directly in DuckDuckGo's website with your browser.

Usage
-----

Just execute it in your shell with keywords you want to use. The following
example searchs for classical music by opening the search results in your
default browser.

.. code-block:: bash

    $ duck classical music

There are options to search specifically for images, videos or websites.

There is also an interactive mode, which lets you make use of more advanced
options. Open the interactive mode by calling Ducker without arguments.

When you make a search in the interactive mode, the search results
are displayed in your terminal. Each result consist of a number, a title,
a URL and an abstract. After making the search you can open the URL of the
first result by entering `1`. Your default browser will open that URL
(opening a new tab if it's already running) and the program will prompt you
again until you decide to exit. You can quit the program entering `q`.

To check out every option execute the program with the
`--help` or `-h` arguments.


Installation
------------

You don't have to install Ducker to run it. Just install Python 3.3 or later
(if you don't have it installed) and execute the `run_ducker.py` file.

However, you can install Ducker if you want with pip:

.. code-block:: bash

    $ pip install ducker

Customization
-------------

You can always use your favourite command-line options of Ducker using Bash
aliases or other utilities available for your shell. Let's say we want to
add an option to search for articles in Wikipedia; we could create a Bash
alias for that.

.. code-block:: bash

    $ alias wikipedia='ducker \!w'

Calling ``wikipedia`` in the shell would open the main page of wikipedia, and
calling ``wikipedia free software`` would open the `"Free software" article
from wikipedia`_. Note that we're using `DuckDuckGo bangs`_ and that the
exclamation mark (!) must be escaped in Bash.

Similarly, you can create an alias to never use JavaScript when using Ducker.

.. code-block:: bash

    $ alias duck='ducker --no-javascript'

Related projects
----------------

- `ddgr`_: Power tool to use DuckDuckGo from the command-line.
- `DuckDuckGo`_: Search engine which doesn't track its users.
- `googler`_: Power tool to Google (Web & News) and Google Site Search from the command-line.

.. _DuckDuckGo bangs: https://duckduckgo.com/bang
.. _"Free software" article from wikipedia: https://en.wikipedia.org/wiki/Free_software
.. _ddgr: https://github.com/jarun/ddgr/
.. _DuckDuckGo: https://duckduckgo.com/
.. _googler: https://github.com/jarun/googler/
