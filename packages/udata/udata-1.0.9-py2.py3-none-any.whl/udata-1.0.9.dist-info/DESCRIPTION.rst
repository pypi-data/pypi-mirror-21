uData
=====





.. image:: https://readthedocs.org/projects/udata/badge/?version=v1.0.9
    :target: https://udata.readthedocs.io/en/v1.0.9/
    :alt: Read the documentation

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/opendatateam/udata
    :alt: Join the chat at https://gitter.im/opendatateam/udata


Customizable and skinnable social platform dedicated to (open)data.

The `full documentation <https://udata.readthedocs.io/en/v1.0.9/>`_ is hosted on Read the Docs.

.. _circleci-url: https://circleci.com/gh/opendatateam/udata
.. _circleci-badge: https://circleci.com/gh/opendatateam/udata.svg?style=shield
.. _requires-io-url: https://requires.io/github/opendatateam/udata/requirements/?tag=v1.0.9
.. _requires-io-badge: https://requires.io/github/opendatateam/udata/requirements.svg?tag=v1.0.9
.. _david-dm-url: https://david-dm.org/opendatateam/udata
.. _david-dm-badge: https://img.shields.io/david/opendatateam/udata.svg
.. _david-dm-dev-url: https://david-dm.org/opendatateam/udata#info=devDependencies
.. _david-dm-dev-badge: https://david-dm.org/opendatateam/udata/dev-status.svg
.. _gitter-badge: https://badges.gitter.im/Join%20Chat.svg
.. _gitter-url: https://gitter.im/opendatateam/udata
.. _readthedocs-badge: https://readthedocs.org/projects/udata/badge/?version=v1.0.9
.. _readthedocs-url: https://udata.readthedocs.io/en/v1.0.9/

Changelog
=========

1.0.9 (2017-04-23)
------------------

- Fix broken post view
  `#877 <https://github.com/opendatateam/udata/pull/877>`_
- Fix new issue submission
  `#874 <https://github.com/opendatateam/udata/issues/874>`_
- Display full images/logo/avatars URL in references too
  `#824 <https://github.com/opendatateam/udata/issues/824>`_

1.0.8 (2017-04-14)
------------------

- Allow more headers in cors preflight headers
  `#857 <https://github.com/opendatateam/udata/pull/857>`_
  `#860 <https://github.com/opendatateam/udata/pull/860>`_
- Fix editorialization admin
  `#863 <https://github.com/opendatateam/udata/pull/863>`_
- Fix missing completer images and ensure completion API is usable on a different domain
  `#864 <https://github.com/opendatateam/udata/pull/864>`_

1.0.7 (2017-04-07)
------------------

- Fix display for zone completer existing values
  `#845 <https://github.com/opendatateam/udata/issues/845>`_
- Proper badge display on dataset and organization page
  `#849 <https://github.com/opendatateam/udata/issues/849>`_
- Remove useless `discussions` from views contexts.
  `#850 <https://github.com/opendatateam/udata/pull/850>`_
- Fix the inline resource edit button not redirecting to admin
  `#852 <https://github.com/opendatateam/udata/pull/852>`_
- Fix broken checksum component
  `#846 <https://github.com/opendatateam/udata/issues/846>`_

1.0.6 (2017-04-01)
------------------

- Default values are properly displayed on dataset form
  `#745 <https://github.com/opendatateam/udata/issues/745>`_
- Prevent a redirect on discussion fetch
  `#795 <https://github.com/opendatateam/udata/issues/795>`_
- API exposes both original and biggest thumbnail for organization logo, reuse image and user avatar
  `#824 <https://github.com/opendatateam/udata/issues/824>`_
- Restore the broken URL check feature
  `#840 <https://github.com/opendatateam/udata/issues/840>`_
- Temporarily ignore INSPIRE in ODS harvester
  `#837 <https://github.com/opendatateam/udata/pull/837>`_
- Allow `X-API-KEY` and `X-Fields` in cors preflight headers
  `#841 <https://github.com/opendatateam/udata/pull/841>`_

1.0.5 (2017-03-27)
------------------

- Fixes error display in forms `#830 <https://github.com/opendatateam/udata/pull/830>`_
- Fixes date range picker dates validation `#830 <https://github.com/opendatateam/udata/pull/830>`_
- Fix badges entries not showing in admin `#825 <https://github.com/opendatateam/udata/pull/825>`_

1.0.4 (2017-03-01)
------------------

- Fix badges trying to use API too early
  `#799 <https://github.com/opendatateam/udata/pull/799>`_
- Some minor tuning on generic references
  `#801 <https://github.com/opendatateam/udata/pull/801>`_
- Cleanup factories
  `#808 <https://github.com/opendatateam/udata/pull/808>`_
- Fix user default metrics not being set [migration]
  `#809 <https://github.com/opendatateam/udata/pull/809>`_
- Fix metric update after transfer
  `#810 <https://github.com/opendatateam/udata/pull/810>`_
- Improve spatial completion ponderation (spatial zones reindexation required)
  `#811 <https://github.com/opendatateam/udata/pull/811>`_

1.0.3 (2017-02-21)
------------------

- Fix JavaScript locales handling `#786 <https://github.com/opendatateam/udata/pull/786>`_
- Optimize images sizes for territory placeholders `#788 <https://github.com/opendatateam/udata/issues/788>`_
- Restore placeholders in search suggestions, fix `#790 <https://github.com/opendatateam/udata/issues/790>`_
- Fix share popover in production build `#793 <https://github.com/opendatateam/udata/pull/793>`_

1.0.2 (2017-02-20)
------------------

- Fix assets packaging for production `#763 <https://github.com/opendatateam/udata/pull/763>`_ `#765 <https://github.com/opendatateam/udata/pull/765>`_
- Transform `udata_version` jinja global into a reusable (by themes) `package_version` `#768 <https://github.com/opendatateam/udata/pull/768>`_
- Ensure topics datasets and reuses can display event with a topic parameter `#769 <https://github.com/opendatateam/udata/pull/769>`_
- Raise a `400 Bad Request` when a bad `class` attribute is provided to the API
  (for entry point not using forms). `#772 <https://github.com/opendatateam/udata/issues/772>`_
- Fix datasets with spatial coverage not being indexed `#778 <https://github.com/opendatateam/udata/issues/778>`_
- Ensure theme assets cache is versionned (and flushed when necessary)
  `#781 <https://github.com/opendatateam/udata/pull/781>`_
- Raise maximum tag length to 96 in order to at least support
  `official INSPIRE tags <http://inspire.ec.europa.eu/theme>`_
  `#782 <https://github.com/opendatateam/udata/pull/782>`_
- Properly raise 400 error on transfer API in case of bad subject or recipient
  `#784 <https://github.com/opendatateam/udata/pull/784>`_
- Fix broken OEmbed rendering `#783 <https://github.com/opendatateam/udata/issues/783>`_
- Improve crawlers behavior by adding some `meta[name=robots]` on pages requiring it
  `#777 <https://github.com/opendatateam/udata/pull/777>`_

1.0.1 (2017-02-16)
------------------

- Pin PyMongo version (only compatible with PyMongo 3+)

1.0.0 (2017-02-16)
------------------

Breaking Changes
****************

* 2016-05-11: Upgrade of ElasticSearch from 1.7 to 2.3 `#449 <https://github.com/opendatateam/udata/pull/449>`_

You have to re-initialize the index from scratch, not just use the `reindex` command given that ElasticSearch 2+ doesn't provide a way to `delete mappings <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-delete-mapping.html>`_ anymore. The command is `udata search init` and may take some time given the amount of data you are dealing with.

* 2017-01-18: User search and listing has been removed (privacy concern)

New & Improved
**************

* 2017-01-06: Add some dataset ponderation factor: temporal coverage, spatial coverage,
  certified provenance and more weight for featured ones. Need reindexation to be taken into account.

* 2016-12-20: Use all the `Dublin Core Frequencies <http://dublincore.org/groups/collections/frequency/>`_
  plus some extra frequencies.

* 2016-12-01: Add the possibility for a user to delete its account in the admin interface

In some configurations, this feature should be deactivated, typically when
there is an SSO in front of udata which may cause some inconsistencies. In
that case, the configuration parameter DELETE_ME should be set to False (True
by default).

* 2016-05-12: Add fields masks to reduce API payloads `#451 <https://github.com/opendatateam/udata/pull/451>`_

The addition of `fields masks <http://flask-restplus.readthedocs.io/en/stable/mask.html>`_ in Flask-RESTPlus allows us to reduce the retrieved payload within the admin — especially for datasets — and results in a performances boost.

Fixes
*****

* 2016-11-29: Mark active users as confirmed `#619 <https://github.com/opendatateam/udata/pull/618>`_
* 2016-11-28: Merge duplicate users `#617 <https://github.com/opendatateam/udata/pull/617>`_
  (A reindexation is necessary after this migration)

Deprecation
***********

Theses are deprecated and support will be removed in some feature release.
See `Deprecation Policy <https://udata.readthedocs.io/en/stable/versionning/#deprecation-policy>`_.

* Theses frequencies are deprecated for their Dublin Core counter part:
    * `fortnighly` ⇨ `biweekly`
    * `biannual` ⇨ `semiannual`
    * `realtime` ⇨ `continuous`


0.9.0 (2017-01-10)
------------------

- First published version



