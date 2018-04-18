# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2014 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""moretools._mapper

Functions for creating sequence mapping functions from item mapping functions.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six.moves import map

__all__ = ['mapper']

from functools import partial


def mapper(func):
    """Create a sequence mapper function from given item mapper `func`.
    """
    def mapper(seq):
        return map(func, seq)

    mapper.__name__ = func.__name__
    mapper.__doc__ = func.__doc__
    return mapper


def mapmethod(func):
    def mapper(self):
        return map(partial(func, self), self)

    mapper.__name__ = func.__name__
    mapper.__doc__ = func.__doc__
    return mapper
