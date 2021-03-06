# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# python-moretools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-moretools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-moretools.  If not, see <http://www.gnu.org/licenses/>.

"""moretools._undefined

Defines the `undefined` object,
which is used internally by several moretools functions
as a default value for optional arguments instead of None,
to allow None as a regular argument value.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

__all__ = ['undefined']


class undefined(object):
    """The class for the `undefined` object.
    """
    def __str__(self):
        raise RuntimeError(
          "undefined has no string conversion. It is undefined :)")

    def __repr__(self):
        return 'undefined'


undefined = undefined()
