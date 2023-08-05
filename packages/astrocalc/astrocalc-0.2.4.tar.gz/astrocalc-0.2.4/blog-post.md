astrocalc
=========

*An astronomer’s calculator used to perform common calculations, conversions and measurements.*.

Usage
=====

``` sourceCode
astrocalc [-c] coordflip <ra> <dec>
astrocalc sep <ra1> <dec1> <ra2> <dec2>
astrocalc timeflip <datetime>
astrocalc trans <ra> <dec> <north> <east>
astrocalc now mjd
astrocalc dist (-z | -m) <distVal> [--hc=hVal --wm=OmegaMatter --wv=OmegaVacuum]


COMMANDS:
========
    coordflip             flip coordinates between decimal degrees and sexegesimal and vice-versa
    sep                   calculate the separation between two locations in the sky.
    timeflip              flip time between UT and MJD.
    trans                 translate a location across the sky (north and east in arcsec)
    now                   report current time in various formats
    dist                  convert distance between mpc to z

VARIABLES:
==========
    ra, ra1, ra2          right-ascension in deciaml degrees or sexegesimal format
    dec, dec1, dec2       declination in deciaml degrees or sexegesimal format
    datetime              modified julian date (mjd) or universal time (UT). UT can be formated 20150415113334.343 or "20150415 11:33:34.343" (spaces require quotes)
    north, east           vector components in arcsec
    distVal               a distance value in Mpc (-mpc) or redshift (-z)
    hVal                  hubble constant value. Default=70 km/s/Mpc
    OmegaMatter           Omega Matter. Default=0.3
    OmegaVacuum           Omega Vacuum. Default=0.7

-h, --help            show this help message
-m, --mpc             distance in mpc
-z, --redshift        redshift distance
-c, --cartesian       convert to cartesian coordinates
```

Installation
============

The easiest way to install astrocalc us to use `pip`:

``` sourceCode
pip install astrocalc
```

Or you can clone the [github repo](https://github.com/thespacedoctor/astrocalc) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/astrocalc.git
cd astrocalc
python setup.py install
```

To upgrade to the latest version of astrocalc use the command:

``` sourceCode
pip install astrocalc --upgrade
```

Documentation
=============

Documentation for astrocalc is hosted by [Read the Docs](http://astrocalc.readthedocs.org/en/stable/) (last [stable version](http://astrocalc.readthedocs.org/en/stable/) and [latest version](http://astrocalc.readthedocs.org/en/latest/)).

Tutorial
========
