from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 0
_version_micro = '3'  # use '' for first of series, number for 1 and above
_version_extra = ''
#_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "skedm: Emperical Dynamic Modeling with a simple api"
# Long description will go up on the pypi page
long_description = """

skedm
========

Scikit Emperical Dynamic Modeling (skedm) can be used as a way to forecast time
series, spatio-temporal 2D arrays, and even discrete spatial arrangements. More
importantly, skedm can provide insight into the underlying dynamics of a system.
"""

NAME = "skedm"
MAINTAINER = "Nick Cortale"
MAINTAINER_EMAIL = "nickcortale@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/nickc1/skedm"
DOWNLOAD_URL = "https://github.com/nickc1/skedm/archive/v0.0.3.tar.gz"
LICENSE = "MIT"
AUTHOR = "Nick Cortale"
AUTHOR_EMAIL = "nickcortale@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['skedm']
PACKAGE_DATA = ""
REQUIRES = ["numpy","numba","scipy"]
