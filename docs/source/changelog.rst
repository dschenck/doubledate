Changelog
========================

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
