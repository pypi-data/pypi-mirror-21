===============
timezonefinderL
===============

.. image:: https://img.shields.io/travis/MrMinimal64/timezonefinderL.svg?branch=master
    :target: https://travis-ci.org/MrMinimal64/timezonefinderL

.. image:: https://img.shields.io/pypi/wheel/timezonefinderL.svg
    :target: https://pypi.python.org/pypi/timezonefinderL

.. image:: https://img.shields.io/pypi/v/timezonefinderL.svg
    :target: https://pypi.python.org/pypi/timezonefinderL


timezonefinderL is the faster and lightweight version of the original `timezonefinder <https://github.com/MrMinimal64/timezonefinder>`__. 
The data takes up 9MB (instead of 19,5MB as with timezonefinder).
Around 56% of the coordinates of the timezone polygons have been simplified and around 60% of the polygons (mostly small islands) have been included in the simplified polygons.


NOTE: In contrast to ``timezonefinder`` with this package the borders of a timezone are stored simplified
when there is no directly neighbouring timezone. So on shorelines the polygons look a lot different now!
This consequently means that the functions **certain_timezone_at()** and **closest_timezone_at()** are not really useful any more!

Check out the GUI and API at: `TimezonefinderL GUI <http://timezonefinder.michelfe.it/gui>`__

For everything else please refer to the `DOCUMENTATION <https://github.com/MrMinimal64/timezonefinder>`__.

Of course the commands need to modified:

::

    pip install timezonefinderL
    from timezonefinderL import TimezoneFinder
    ...



Also see:
`GitHub <https://github.com/MrMinimal64/timezonefinderL>`__. 
`PyPI <https://pypi.python.org/pypi/timezonefinderL/>`__


License
=======

``timezonefinderL`` is distributed under the terms of the MIT license
(see LICENSE.txt).



Speed Comparison
================

::

    shapely: ON (tzwhere)
    Numba: ON (timezonefinderL)


    TIMES for  10000 realistic points
    tzwhere: 0:00:00.608965
    timezonefinder: 0:00:00.564314
    0.08 times faster


    TIMES for  10000 random points
    tzwhere: 0:00:00.650164
    timezonefinder: 0:00:00.508654
    0.28 times faster


Changelog
=========


2.0.1 (2017-04-08)
------------------

* added missing package data entries (2.0.0 didn't include all necessary .bin files)


2.0.0 (2017-04-07)
------------------

* introduction of this version of `timezonefinder <https://github.com/MrMinimal64/timezonefinder/>`__
* data has been simplified which affects speed and data size. Around 56% of the coordinates of the timezone polygons have been deleted and around 60% of the polygons (mostly small islands) have been included in the simplified polygons. For any coordinate on landmass the results should stay the same, but accuracy at the shorelines is lost. This eradicates the usefulness of closest_timezone_at() and certain_timezone_at() but the main use case for this package (= determining the timezone of a point on landmass) is improved.
* file_converter.py has been complemented and modified to perform those simplifications
* introduction of new function get_geometry() for querying timezones for their geometric shape
* added shortcuts_unique_id.bin for instantly returning an id if the shortcut corresponding to the coords only contains polygons of one zone
* data is now stored in separate binaries for ease of debugging and readability
* polygons are stored sorted after their timezone id and size
* timezonefinder can now be called directly as a script (experimental with reduced functionality, see readme)
* optimisations on point in polygon algorithm
* small simplifications in the helper functions
* clarification of the readme
* clarification of the comments in the code
* referenced the new conda-feedstock in the readme
* referenced the new timezonefinder API/GUI


for older versions refer to `timezonefinder <https://github.com/MrMinimal64/timezonefinder/>`__.


