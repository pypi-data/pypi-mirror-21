#!/usr/bin/env python
#
# map2d.py
# A generic interface to a 2D dust reddening map.
#
# Copyright (C) 2016  Gregory M. Green
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import print_function, division

import numpy as np
import healpy as hp
import astropy.coordinates as coordinates
import astropy.units as units

from functools import wraps

from . import dustexceptions


def coord2healpix(coords, frame, nside, nest=True):
    """
    Calculate HEALPix indices from an astropy SkyCoord. Assume the HEALPix
    system is defined on the coordinate frame `frame`.

    Args:
        coords (astropy.coordinates.SkyCoord): The input coordinates.
        frame (str): The frame in which the HEALPix system is defined.
        nside (int): The HEALPix nside parameter to use. Must be a power of 2.
        nest (Optional[bool]): `True` (the default) if nested HEALPix ordering
            is desired. `False` for ring ordering.

    Returns:
        An array of pixel indices (integers), with the same shape as the input
        SkyCoord coordinates (`coords.shape`).

    Raises:
        dustexceptions.CoordFrameError: If the specified frame is not supported.
    """
    c = coords.transform_to(frame)

    if hasattr(c, 'ra'):
        phi = c.ra.rad
        theta = 0.5*np.pi - c.dec.rad
        return hp.pixelfunc.ang2pix(nside, theta, phi, nest=nest)
    elif hasattr(c, 'l'):
        phi = c.l.rad
        theta = 0.5*np.pi - c.b.rad
        return hp.pixelfunc.ang2pix(nside, theta, phi, nest=nest)
    elif hasattr(c, 'x'):
        return hp.pixelfunc.vec2pix(nside, c.x.kpc, c.y.kpc, c.z.kpc, nest=nest)
    elif hasattr(c, 'w'):
        return hp.pixelfunc.vec2pix(nside, c.w.kpc, c.u.kpc, c.v.kpc, nest=nest)
    else:
        raise dustexceptions.CoordFrameError(
            'No method to transform from coordinate frame "{}" to HEALPix.'.format(
                frame))


def ensure_coord_type(f):
    """
    A decorator for class methods of the form

    .. code-block:: python

        Class.method(self, coords, **kwargs)

    where ``coords`` is an ``astropy.coordinates.SkyCoord`` object.

    The decorator raises a ``TypeError`` if the ``coords`` that gets passed to
    ``Class.method`` is not an ``astropy.coordinates.SkyCoord`` instance.

    Args:
        f (class method): A function with the signature
            ``(self, coords, **kwargs)``, where ``coords`` is a ``SkyCoord``
            object containing an array.

    Returns:
        A function that raises a ``TypeError`` if ``coord`` is not an
            ``astropy.coordinates.SkyCoord`` object, but which otherwise behaves
            the same as the decorated function.
    """
    @wraps(f)
    def _wrapper_func(self, coords, **kwargs):
        if not isinstance(coords, coordinates.SkyCoord):
            raise TypeError('`coords` must be an astropy.coordinates.SkyCoord object.')
        return f(self, coords, **kwargs)
    return _wrapper_func


def reshape_coords(coords, shape):
    pos_attr = ['l', 'b', 'ra', 'dec', 'x', 'y', 'z', 'w', 'u', 'v', 'distance']
    pos_kwargs = {}

    for attr in pos_attr:
        if hasattr(coords, pos_attr):
            pos_kwargs[attr] = np.reshape()
            # TODO: finish reshape


def coords_to_shape(gal, shape):
    l = np.reshape(gal.l.deg, shape) * units.deg
    b = np.reshape(gal.b.deg, shape) * units.deg

    has_dist = hasattr(gal.distance, 'kpc')
    d = np.reshape(gal.distance.kpc, shape) * units.kpc if has_dist else None

    return coordinates.SkyCoord(l, b, distance=d, frame='galactic')


def ensure_flat_frame(f, frame):
    def _wrapper_func(self, coords, **kwargs):
        coords_transf = coords.transform_to(frame)

        is_array = not coords.isscalar
        if is_array:
            orig_shape = coords.shape
            shape_flat = (np.prod(orig_shape),)
            coords_transf = coords_to_shape(coords_transf, shape_flat)
        else:
            coords_transf = coords_to_shape(coords_transf, (1,))

        out = f(self, gal, **kwargs)

        if is_array:
            out.shape = orig_shape + out.shape[1:]
        else:
            out = out[0]

        return out

    return _wrapper_func


def gal_to_shape(gal, shape):
    l = np.reshape(gal.l.deg, shape)*units.deg
    b = np.reshape(gal.b.deg, shape)*units.deg

    has_dist = hasattr(gal.distance, 'kpc')
    d = np.reshape(gal.distance.kpc, shape)*units.kpc if has_dist else None

    return coordinates.SkyCoord(l, b, distance=d, frame='galactic')


def ensure_flat_galactic(f):
    """
    A decorator for class methods of the form

    .. code-block:: python

        Class.method(self, coords, **kwargs)

    where ``coords`` is an ``astropy.coordinates.SkyCoord`` object.

    The decorator ensures that the ``coords`` that gets passed to
    ``Class.method`` is a flat array of Galactic coordinates. It also reshapes
    the output of ``Class.method`` to have the same shape (possibly scalar) as
    the input ``coords``. If the output of ``Class.method`` is a tuple or list
    (instead of an array), each element in the output is reshaped instead.

    Args:
        f (class method): A function with the signature
            ``(self, coords, **kwargs)``, where ``coords`` is a ``SkyCoord``
            object containing an array.

    Returns:
        A function that takes ``SkyCoord`` input with any shape (including
        scalar).
    """

    @wraps(f)
    def _wrapper_func(self, coords, **kwargs):
        gal = coords.transform_to('galactic')

        is_array = not coords.isscalar
        if is_array:
            orig_shape = coords.shape
            shape_flat = (np.prod(orig_shape),)
            # print 'Original shape: {}'.format(orig_shape)
            # print 'Flattened shape: {}'.format(shape_flat)
            gal = gal_to_shape(gal, shape_flat)
        else:
            gal = gal_to_shape(gal, (1,))

        out = f(self, gal, **kwargs)

        if is_array:
            if isinstance(out, list) or isinstance(out, tuple):
                # Apply to each array in output list
                for o in out:
                    o.shape = orig_shape + o.shape[1:]
            else:   # Only one array in output
                out.shape = orig_shape + out.shape[1:]
        else:
            if isinstance(out, list) or isinstance(out, tuple):
                # Apply to each array in output list
                for o in out:
                    o = o[0]
            else:   # Only one array in output
                out = out[0]

        return out

    return _wrapper_func


class DustMap(object):
    """
    Base class for querying dust maps. For each individual dust map, a different
    subclass should be written, implementing the `query` function.
    """

    def __init__(self):
        pass

    @ensure_coord_type
    def __call__(self, coords, **kwargs):
        """
        An alias for ``DustMap.query``.
        """
        return self.query(coords, **kwargs)

    def query(self, coords, **kwargs):
        """
        Query the map at a set of coordinates.

        Args:
            coords (`astropy.coordinates.SkyCoord`): The coordinates at which to
                query the map.

        Raises:
            NotImplementedError: This function must be defined by derived
                classes.
        """
        raise NotImplementedError(
            '`DustMap.query` must be implemented by subclasses.\n'
            'The `DustMap` base class should not itself be used.')

    def query_gal(self, l, b, d=None, **kwargs):
        """
        Query using Galactic coordinates.

        Args:
            l (float, scalar or array-like): Galactic longitude, in degrees.
            b (float, scalar or array-like): Galactic latitude, in degrees.
            d (Optinal[float, scalar or array-like]): Distance from the Solar
                System. Defaults to `None`, meaning no distance is specified.
            **kwargs: Any additional keyword arguments accepted by derived
                classes.

        Returns:
            The results of the query, which must be implemented by derived
            classes.
        """

        if d is None:
            coords = coordinates.SkyCoord(l, b, frame='galactic', unit='deg')
        else:
            coords = coordinates.SkyCoord(
                l, b,
                distance=d,
                frame='galactic',
                unit='deg')

        return self.query(coords, **kwargs)

    def query_equ(self, ra, dec, d=None, frame='icrs', **kwargs):
        """
        Query using Equatorial coordinates. By default, the ICRS frame is used,
        although other frames implemented by `astropy.coordinates` may also be
        specified.

        Args:
            ra (float, scalar or array-like): Galactic longitude, in degrees.
            dec (float, scalar or array-like): Galactic latitude, in degrees.
            d (Optinal[float, scalar or array-like]): Distance from the Solar
                System. Defaults to `None`, meaning no distance is specified.
            frame (Optional[icrs]): The coordinate system. Can be 'icrs' (the
                default), 'fk5', 'fk4' or 'fk4noeterms'.
            **kwargs: Any additional keyword arguments accepted by derived
                classes.

        Returns:
            The results of the query, which must be implemented by derived
            classes.
        """

        valid_frames = ['icrs', 'fk4', 'fk5', 'fk4noeterms']

        if frame not in valid_frames:
            raise ValueError(
                '`frame` not understood. Must be one of {}.'.format(valid_frames))

        if d is None:
            coords = coordinates.SkyCoord(ra, dec, frame='icrs', unit='deg')
        else:
            coords = coordinates.SkyCoord(
                ra, dec,
                distance=d,
                frame='icrs',
                unit='deg')

        return self.query(coords, **kwargs)
