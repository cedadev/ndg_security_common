"""NDG Security ndg namespace package

NERC DataGrid Project

This is a setuptools namespace_package.  DO NOT place any other
code in this file!  There is no guarantee that it will be installed
with easy_install.  See:

http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages

... for details.
"""
__author__ = "P J Kershaw"
__date__ = "27/10/06"
__copyright__ = "(C) 2009 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
