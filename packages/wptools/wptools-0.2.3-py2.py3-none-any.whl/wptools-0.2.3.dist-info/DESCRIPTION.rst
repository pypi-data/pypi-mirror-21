Wikipedia tools (for Humans)
============================

.. image:: https://img.shields.io/pypi/v/wptools.svg
        :target: https://pypi.python.org/pypi/wptools/

.. image:: https://travis-ci.org/siznax/wptools.svg?branch=master
        :target: https://travis-ci.org/siznax/wptools

.. image:: https://coveralls.io/repos/github/siznax/wptools/badge.svg?branch=master
        :target: https://coveralls.io/github/siznax/wptools

Python and command-line MediaWiki access for Humans.

- get an HTML or plain text "extract" (lead or summary)
- get a representative image (pageimage, thumb, etc.)
- get an Infobox as a python dictionary
- get any/all Wikidata by title
- get info in any language
- get random info

This package is intended to make it as easy as possible to get data
from MediaWiki instances, expose more Wikidata, and extend Wikimedia
APIs just for kicks. We say (for Humans) because that is a goal_.
Questions, feedback, and especially contributions_ are welcome!


Install
-------

.. code-block:: bash

    $ pip install wptools
    ✨🦄✨


Example
-------

.. code-block:: python

    >>> import wptools
    >>> p = wptools.page('Gandhi').get()
    Gandhi (en)
    {
      lang: en
      title: Gandhi
    }
    en.wikipedia.org (query) Gandhi
    en.wikipedia.org (parse) 19379
    www.wikidata.org (wikidata) Q1001
    www.wikidata.org (claims) Q5|Q129286|Q6512732|Q668
    en.wikipedia.org (imageinfo) File:Portrait Gandhi.jpg|File:MKGandhi.jpg
    Mahatma_Gandhi (en)
    {
      cache: <dict(5)> {claims, imageinfo, parse, query, wikidata}
      claims: <dict(4)> {Q129286, Q5, Q6512732, Q668}
      description: pre-eminent leader of Indian nationalism during British-ruled India
      extext: <str(3200)> **Mohandas Karamchand Gandhi** (/ˈɡɑːndi, ˈɡæn...
      extract: <str(3875)> <p><b>Mohandas Karamchand Gandhi</b> (<span><...
      images: <list(4)>
      infobox: <dict(21)> {alma_mater, alt, birth_date, birth_name, birt...
      label: Mahatma Gandhi
      lang: en
      links: <list(10)>
      modified: <dict(2)> {page, wikidata}
      pageid: 19379
      parsetree: <str(239926)> <root><template><title>Redirect</title><p...
      props: <dict(7)> {P18, P27, P31, P345, P569, P570, P910}
      random: Mirco Baldacci
      title: Mahatma_Gandhi
      url: https://en.wikipedia.org/wiki/Mahatma_Gandhi
      url_raw: https://en.wikipedia.org/wiki/Mahatma_Gandhi?action=raw
      what: human
      wikibase: Q1001
      wikidata: <dict(7)> {IMDB, birth, category, citizenship, death, im...
      wikidata_url: https://www.wikidata.org/wiki/Q1001
      wikitext: <str(182553)> {{Redirect|Gandhi}}{{pp-move-indef}}{{pp-s...
    }


Documentation
-------------

See our wiki_.


Please enjoy!


@siznax 👹


.. _contributions: https://github.com/siznax/wptools/blob/master/CONTRIBUTING.md
.. _goal: http://docs.python-requests.org/en/master/user/intro/
.. _wiki: https://github.com/siznax/wptools/wiki


.. :changelog:

Release History
---------------

0.2.3 (2017-04-17)
++++++++++++++++++

* Merge @aplz improvement: fetch full lists in infobox values (#62)
* Get extract as HTML
* Fix AttributeError bug (#47)
* Refactoring fixes


0.2.0 (2016-11-06)
++++++++++++++++++

* Many fixes/improvements with help of @seansay (thank you!)
* Raise LookupError on API missing page/title
* Consolidated images and caches
* Support get_query() by pageid
* Support proxy, timeout on all API entrypoints
* Support for language variants (e.g. variant='zh-cn')
* Support for non-https wikis via wiki='http://example.com'
* Automatically get_imageinfo() via MediaWiki API:Imageinfo
* moved NOTES.md to wiki


0.1.7 (2016-09-20)
++++++++++++++++++

* Minor fixes
* Provide local SSL certs with python-certifi
* Enabled extending Wikidata properties
* Improved cache checking


0.1.4 (2016-09-06)
++++++++++++++++++

* Python 3 support!
* Implemented get_claims()
* Patch get_rest() path, tests/test_advanced
* Implemented get_wikidata() by title, lang
* Geo coordinates Property:P625 from Wikidata
* Added RESTBase support, lead attribute
* Made wptools.page() the atomic object


0.1.0 (2016-08-25)
++++++++++++++++++

* Many fixes, enhancements.
* ONE CLI SCRIPT TO RULE THEM ALL: wptool.
* Much testing of random (title, lang, and wiki).
* Allow chaining get_s or just get().
* Enabled full-hydration from wikibase only.
* Block further requests on fatal error.
* Get 240x thumbnails instead of default 50x.
* Harmonized silent and verbose arguments.
* Mock-up tests/test_advanced.py.
* Made NOTES.md a knowledge base.
* Use _humans_ in README examples. ;-)


0.0.5 (2016-08-23)
++++++++++++++++++

* Major re-write.
* Exposed core.WPTools as entrypoint.
* Added get_parse(), get_query(), and get_wikidata().
* Added get(self) to query all APIs.
* Added show(self) method to display fetched attrs.
* Show instance attributes after each request.
* Ignore requests if attrs will not be updated.
* Enabled language support across APIs.
* Gets random article if no arguments.
* CLI scripts and tests disabled pending update.


0.0.4 (2016-08-16)
++++++++++++++++++

* Added wptools.lead.
* Added safe_exit() to CLI scripts.
* Removed a fair amount of unused code.


0.0.3 (2016-08-12)
++++++++++++++++++

* Implemented wptools.image choices.
* Added wptools.api to simplify python i/f and CLI scripts.
* Merged @0x9900's CLI dist fixes.
* A little more test coverage.
* Starting to look like a legit module.


0.0.1 (2015)
++++++++++++

* Still better than alternatives for working with articles.


0.0.0 (2012)
++++++++++++

* It seems to work!


