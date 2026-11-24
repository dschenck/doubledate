Changelog
========================
The source code is hosted and maintained on `github <https://github.com/dschenck/doubledate/>`_.

Version 0.1.0 (24 November 2026)
----------------------------------
Breaking changes

- requires Python 3.11 or later; Python 3.8, 3.9 and 3.10 (all end-of-life) are no longer supported
- :code:`Calendar.lb` and :code:`Calendar.fa` now raise a :code:`KeyError` (or return
  :code:`default`) when there is no date strictly before the first date / strictly after
  the last date. Previously :code:`lb` on the first date returned the *last* date of the
  calendar, and :code:`fa` on the last date raised an :code:`IndexError`
- :code:`Calendar.groupby("W")` groups by ISO year and week number, so the last days of
  December no longer fall in the same group as the first week of that year
- :code:`str(diem)` returns ISO 8601 format with zero-padding (e.g. :code:`--03-01`
  instead of :code:`--3-1`)
- :code:`Calendar` no longer type-checks its dates on creation, for performance
- :code:`weekdayof` requires its :code:`date` argument
- :code:`dayof`, :code:`daysfrom` and :code:`daysto` raise a :code:`ValueError` when
  given neither dates nor a calendar
- :code:`Calendar.create` raises a :code:`ValueError` for unknown frequency strings

New features

- type hints for the full public API, shipped with a :code:`py.typed` marker (PEP 561)
  for use with type checkers such as mypy
- slices of a calendar between two dates (:code:`calendar[date1:date2]`) are cached;
  the cache size is set by :code:`Calendar.SLICE_CACHE_SIZE` (default 256)
- :code:`Calendar.groupby` and :code:`Calendar.resample` accept :code:`"T"` (trimester)
- :code:`diem` objects are hashable, and :code:`diem.parse` accepts month names in
  any case (e.g. :code:`"Jan"`)
- :code:`Calendar.snap` accepts the :code:`"last"` and :code:`"following"` fallback
  aliases
- :code:`last` accepts integer weekdays (e.g. :code:`dtwo.MON`)

Bug fixes

- :code:`Calendar.create` failed with :code:`"W-MON"`-style frequencies or a single
  :code:`byweekday` value, and ignored :code:`dtype`
- :code:`Collection` created from a generator was always empty
- :code:`offset` no longer swallows unrelated exceptions when offsetting by months or years
- the quickstart example now removes holidays as intended
- corrected many docstring examples, argument descriptions and typos

Version 0.0.4 (7 March 2020)
----------------------------------
- renamed :code:`map` to :code:`apply`
- added :code:`weekdayof` utility function
- refactored :code:`utils.dayof`, :code:`utils.daysfrom` and :code:`utils.daysto`
- removed :code:`add` method to maintain immutability
- removed :code:`length` property (use :code:`len(calendar)` instead)

Version 0.0.3 (1 March 2020)
----------------------------------
- added :code:`utils.dayof`, :code:`utils.daysto` and :code:`utils.daysfrom`
- exposed :code:`datetime.datetime` as module
- added constants
- fixed a bug in :code:`utils.floor` and :code:`utils.ceil` on weekly frequencies
- replaced :code:`internals.isdatelike` by simple :code:`isinstance` type-check

Version 0.0.2 (22 February 2020)
----------------------------------
- added Calendar.split

Version 0.0.1 (22 February 2020)
----------------------------------
- added Calendar class
- added utility functions to compute semester, trimester and quarter of given date
- added utility functions to compute start and end of period (e.g. month)
