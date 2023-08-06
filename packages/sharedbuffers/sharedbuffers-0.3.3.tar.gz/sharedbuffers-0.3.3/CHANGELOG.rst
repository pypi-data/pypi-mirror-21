Change Log
==========

All notable changes to this project will be documented here.

The format is largely inspired by keepachangelog_.

.. _0.1.1:

0.3.3 - 2017-04-25
==================

Bugfixes
--------

- Limit pack buffer expansion to avoid memory exhaustion on recurring errors
- Fix bitmap generation for objects with more than 30 attributes

0.3.2 - 2017-04-07
==================

Bugfixes
--------

- Fix unpacking of frozensets with big (beyond 32-bit) offsets

0.3.1 - 2016-11-09
==================

Bugfixes
--------

- Fix binary search functions to properly test the given array's dtype to avoid
  spurious NotImplementedError s

0.3.0 - 2016-11-08
==================

Added
-----

- Exported hinted_bsearch and bsearch functions (present when cythonized) that implement
  both hinted and regular binary search on numpy arrays. Unlike numpy's bsearch, they don't
  release the GIL, so they're faster for single lookups than numpy's counterparts
- Added sorted_contains and hinted_sorted_contains as useful helpers to use sorted numpy
  arrays as compact number sets

0.2.1 - 2016-10-18
==================

Bugfixes
--------

- Make requirements install requirements
- Add __version__
- Fix pure-python compatibility
- Implement more of the mapping interface on id mappers
- Add get_iter and __contains__ on multimappers that avoids materializing big sequences

0.2.0 - 2016-10-11
==================

Bugfixes
--------

- Fix requirements to include chorde_

Added
-----

- Add multimaps, binary compatible with simple mappings, 
  but return all matching values for a key rather than a single one
- Add approximate string multimaps

0.1.0
=====

*Note*: this release has dependency issues, use 0.2.0_ instead

Added
-----

- Initial release

.. _chorde: https://bitbucket.org/claudiofreire/chorde
.. _keepachangelog: http://keepachangelog.com/

