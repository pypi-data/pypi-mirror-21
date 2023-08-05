#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 SKA South Africa
#
# This file is part of hypercube.
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import collections
import itertools
import sys
import types
from weakref import WeakKeyDictionary

import numpy as np
from attrdict import AttrDict
from tabulate import tabulate

from hypercube.dims import create_dimension, Dimension
import hypercube.util as hcu

class PropertyDescriptor(object):
    """ Descriptor class for properties """
    def __init__(self, record_key, default=None, ):
        self.default = default
        self.record_key = record_key
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance,self.default)

    def __set__(self, instance, value):
        dtype = instance._properties[self.record_key].dtype
        self.data[instance] = dtype(value)

    def __delete__(self, instance):
        del self.data[instance]

class HyperCube(object):
    """ Hypercube. """

    def __init__(self, *args, **kwargs):
        """
        Hypercube Constructor
        """

        # Dictionaries to store records about our
        # dimensions, arrays and properties
        self._dims = collections.OrderedDict()
        self._arrays = collections.OrderedDict()
        self._properties = collections.OrderedDict()

        # Register any dimensions, arrays and
        # properties we're provided
        dims = kwargs.get('dimensions', None)
        arrays = kwargs.get('arrays', None)
        properties = kwargs.get('properties', None)

        if dims is not None:
            self.register_dimensions(dims)

        if arrays is not None:
            self.register_arrays(arrays)

        if properties is not None:
            self.register_properties(properties)


    def bytes_required(self):
        """
        :rtype: Estimated number of bytes required by arrays registered
                on the cube, taking their extents into account.
        """
        return np.sum([hcu.array_bytes(a) for a
            in self.arrays(reify=True).itervalues()])

    def mem_required(self):
        """
        :rtype: String approximately describing the memory
                required by arrays registered on the cube,
                taking their extents into account.
        """
        return hcu.fmt_bytes(self.bytes_required())

    def register_dimension(self, name, dim_data, **kwargs):
        """
        Registers a dimension on this cube.

        ::

            cube.register_dimension('ntime', 10000,
                        decription="Number of Timesteps",
                        lower_extent=100, upper_extent=200)

        :param dim_data: if an integer, this will be used to
            define the global_size of the dimension
            and possibly other attributes if they are
            not present in kwargs.
            If a Dimension, it will be updated with
            any appropriate keyword arguments
        :type dim_data: int or :class:`~hypercube.dims.Dimension`

        :param description: The description for this dimension.
            e.g. 'Number of timesteps'.
        :type description: str

        :param lower_extent: The lower extent of this dimension
                within the global space
        :type lower_extent: int
        :param upper_extent: The upper extent of this dimension
                within the global space
        :type upper_extent: int

        :rtype: A :class:`~hypercube.dims.Dimension` object
        """

        if name in self._dims:
            raise AttributeError((
                "Attempted to register dimension '{n}'' "
                "as an attribute of the cube, but "
                "it already exists. Please choose "
                "a different name!").format(n=name))

        # Create the dimension dictionary
        D = self._dims[name] = create_dimension(name,
            dim_data, **kwargs)

        return D

    def register_dimensions(self, dims):
        """
        Register multiple dimensions on the cube.

        :param dims: A list or dictionary of dimensions
        :type dims: list or dict

        ::

            cube.register_dimensions([
                {'name' : 'ntime', 'global_size' : 10, 'lower_extent' : 2, 'upper_extent' : 7 },
                {'name' : 'na', 'global_size' : 3, 'lower_extent' : 2, 'upper_extent' : 7 },
            ])
        """

        if isinstance(dims, collections.Mapping):
            dims = dims.itervalues()

        for dim in dims:
            self.register_dimension(dim.name, dim)

    def update_dimensions(self, dims):
        """
        Update multiple dimension on the cube.

        :param dims: A list or dictionary of dimension updates
        :type dims: list or dict:

        ::

            cube.update_dimensions([
                {'name' : 'ntime', 'global_size' : 10, 'lower_extent' : 2, 'upper_extent' : 7 },
                {'name' : 'na', 'global_size' : 3, 'lower_extent' : 2, 'upper_extent' : 7 },
            ])
        """

        if isinstance(dims, collections.Mapping):
            dims = dims.itervalues()

        for dim in dims:
            # Defer to update dimension for dictionaries
            if isinstance(dim, dict):
                self.update_dimension(**dim)
            # Replace if given a Dimension object
            elif isinstance(dim, Dimension):
                self._dims[dim.name] = dim
            else:
                raise TypeError("Unhandled type '{t}'"
                    "in update_dimensions".format(t=type(dim)))

    def update_dimension(self, name, **update_dict):
        """
        Update the dimension size and extents.

        :param update_dict: A dictionary containing keywords passed through to
            :meth:`~hypercube.dims.Dimension.update`
        :type update_dict: dict
        """
        if not name:
            raise AttributeError("A dimension name is required to update "
                "a dimension. Update dictionary {u}."
                    .format(u=update_dict))

        dim = self._dims.get(name, None)

        # Sanity check dimension existence
        if not dim:
            raise ValueError("'Dimension {n}' cannot be updated as it "
                "is not registered in the dimension dictionary."
                    .format(n=name))

        dim.update(**update_dict)

    def _dim_attribute(self, attr, *args, **kwargs):
        """
        Returns a list of dimension attribute attr, for the
        dimensions specified as strings in args.::

            ntime, nbl, nchan = cube._dim_attribute('global_size', ntime, 'nbl', 'nchan')

        or::

            ntime, nbl, nchan, nsrc = cube._dim_attribute('global_size', 'ntime,nbl:nchan nsrc')
        """

        import re

        # If we got a single string argument, try splitting it by separators
        if len(args) == 1 and isinstance(args[0], str):
            args = (s.strip() for s in re.split(',|:|;| ', args[0]))

        # Now get the specific attribute for each string dimension
        # Integers are returned as is
        result = [d if isinstance(d, (int, np.integer))
            else getattr(self._dims[d], attr) for d in args]

        # Return single element if length one and single else entire list
        return (result[0] if kwargs.get('single', True)
            and len(result) == 1 else result)

    def dim_global_size_dict(self):
        """ Returns a mapping of dimension name to global size """
        return { d.name: d.global_size for d in self._dims.itervalues()}

    def dim_lower_extent_dict(self):
        """ Returns a mapping of dimension name to lower_extent """
        return { d.name: d.lower_extent for d in self._dims.itervalues()}

    def dim_upper_extent_dict(self):
        """ Returns a mapping of dimension name to upper_extent """
        return { d.name: d.upper_extent for d in self._dims.itervalues()}

    def dim_global_size(self, *args, **kwargs):
        """
        Return the global size of the dimensions in *args.::

            ntime, nbl, nchan = cube.dim_global_size('ntime, 'nbl', 'nchan')

        or::

            ntime, nbl, nchan, nsrc = cube.dim_global_size('ntime,nbl:nchan nsrc')
        """

        return self._dim_attribute('global_size', *args, **kwargs)

    def dim_lower_extent(self, *args, **kwargs):
        """
        Returns the lower extent of the dimensions in *args.::


            t_ex, bl_ex, ch_ex = cube.dim_lower_extent('ntime,\ 'nbl', 'nchan')

        or::

            t_ex, bl_ex, ch_ex, src_ex = cube.dim_lower_extent('ntime,nbl:nchan nsrc')
        """

        # The lower extent of any integral dimension is 0 by default
        args = tuple(0 if isinstance(a, (int, np.integer))
            else a for a in args)
        return self._dim_attribute('lower_extent', *args, **kwargs)

    def dim_upper_extent(self, *args, **kwargs):
        """
        Returns the upper extent of the dimensions in *args.::

            t_ex, bl_ex, ch_ex = cube.dim_upper_extent('ntime, 'nbl', 'nchan')

        or::

            t_ex, bl_ex, ch_ex, src_ex = cube.dim_upper_extent('ntime,nbl:nchan nsrc')
        """

        return self._dim_attribute('upper_extent', *args, **kwargs)

    def dim_extents(self, *args, **kwargs):
        """
        Returns extent tuples of the dimensions in *args.::

            (tl, tu), (bl, bu) = cube.dim_extents('ntime, 'nbl')

        or::

            (tl, tu), (bl, bu) = cube.dim_upper_extent('ntime,nbl')
        """


        l = self.dim_lower_extent(*args, **kwargs)
        u = self.dim_upper_extent(*args, **kwargs)

        # Handle sequence and singles differently
        if isinstance(l, collections.Sequence):
            return zip(l, u)
        else:
            return (l, u)

    def dim_extent_size(self, *args, **kwargs):
        """
        Returns extent sizes of the dimensions in *args.::

            ts, bs, cs = cube.dim_extent_size('ntime, 'nbl', 'nchan')

        or::

            ts, bs, cs, ss = cube.dim_extent_size('ntime,nbl:nchan nsrc')
        """


        extents = self.dim_extents(*args, **kwargs)

        # Handle tuples and sequences differently
        if isinstance(extents, tuple):
            return extents[1] - extents[0]
        else: # isinstance(extents, collections.Sequence):
            return (u-l for l, u in extents)

    def register_array(self, name, shape, dtype, **kwargs):
        """
        Register an array with this cube.::

            cube.register_array("model_vis", ("ntime", "nbl", "nchan", 4), np.complex128)

        :param name: Array name
        :type name: str
        :param shape: Array shape schema
        :type shape: A tuple containing either Dimension names or ints
        :param dtype: Array data type
        :type dype: numpy dtype

        :rtype: A dictionary describing this array.
        """

        # Complain if array exists
        if name in self._arrays:
            raise ValueError(('Array %s is already registered '
                'on this cube object.') % name)

        # OK, create a record for this array
        A = self._arrays[name] = AttrDict(name=name,
            dtype=dtype, shape=shape,
            **kwargs)

        return A

    def register_arrays(self, arrays):
        """
        Register arrays using a list of dictionaries defining the arrays.

        The list should itself contain dictionaries. i.e.::

            D = [{ 'name':'uvw', 'shape':(3,'ntime','nbl'),'dtype':np.float32 },
                { 'name':'lm', 'shape':(2,'nsrc'),'dtype':np.float32 }]

        :param arrays: A list or dictionary of dictionaries describing arrays.
        :type arrays: A list or dict.

        """

        if isinstance(arrays, collections.Mapping):
            arrays = arrays.itervalues()

        for ary in arrays:
            self.register_array(**ary)

    def register_property(self, name, dtype, default, **kwargs):
        """
        Registers a property with this Solver object::

            cube.register_property("reference_frequency", np.float64, 1.4e9)

        :param name: The name of this property.
        :type name: str
        :param dtype: Numpy data type
        :type dtype: Numpy data type
        :param default: Default value for this value
        :type default: Should be convertable to dtype
        """
        if name in self._properties:
            raise ValueError(('Property %s is already registered '
                'on this cube object.') % name)

        P = self._properties[name] = AttrDict(name=name,
            dtype=dtype, default=default)

        #if not hasattr(HyperCube, name):
        if not HyperCube.__dict__.has_key(name):
                # Create the descriptor for this property on the class instance
            setattr(HyperCube, name, PropertyDescriptor(record_key=name, default=default))

        # Set the descriptor on this object instance
        setattr(self, name, default)

        # Should we create a setter for this property?
        setter = kwargs.get('setter_method', True)
        setter_name = hcu.setter_name(name)

        # Yes, create a default setter
        if isinstance(setter, types.BooleanType) and setter is True:
            def set(self, value):
                setattr(self,name,value)

            setter_method = types.MethodType(set, self)
            setattr(self, setter_name, setter_method)

            # Set up the docstring, using the supplied one
            # if it is present, otherwise generating a default
            setter_docstring = kwargs.get('setter_docstring', None)
            getattr(setter_method, '__func__').__doc__ = \
                """ Sets property %s to value. """ % (name) \
                if setter_docstring is None else setter_docstring

        elif isinstance(setter, types.MethodType):
            setattr(self, setter_name, setter)
        else:
            raise TypeError, ('setter keyword argument set',
                ' to an invalid type %s' % (type(setter)))

        return P

    def register_properties(self, properties):
        """
        Register properties using a list defining the properties.

        :param properties: A dictionary or list of dictionaries
            describingg properties
        :type properties: A dictionary or list

        The dictionary should itself contain dictionaries. i.e.::

            D = [
                { 'name':'ref_wave','dtype':np.float32,
                    'default':1.41e6 },
            ]
        """
        if isinstance(properties, collections.Mapping):
            properties = properties.itervalues()

        for prop in properties:
            self.register_property(**prop)

    def properties(self):
        """ :rtype: Returns a dictionary of properties """
        return self._properties

    def property(self, name):
        """ :rtype:  Returns a property """
        try:
            return self._properties[name]
        except KeyError:
            raise KeyError("Property '{n}' is not registered "
                "on this cube".format(n=name)), None, sys.exc_info()[2]

    def arrays(self, reify=False):
        """
        :rtype: Returns a dictionary of arrays. If reify is True,
            it will replace any dimension within the array shape with
            the extent_size of the dimension.
        """
        return (self._arrays if not reify else
            hcu.reify_arrays(self._arrays, self.dimensions(copy=False)))

    def array(self, name, reify=False):
        """
        :rtype:  Returns an array object. If reify is True,
            it will replace any dimension within the array shape with
            the extent_size of the dimension.
        """

        try:
            return (self._arrays[name] if not reify else
                hcu.reify_arrays({name : self._arrays[name]},
                    self.dimensions(copy=False))[name])
        except KeyError:
            raise KeyError("Array '{n}' is not registered on this cube"
                .format(n=name)), None, sys.exc_info()[2]

    def dimensions(self, copy=True):
        """
        Return a dictionary of :class:`~hypercube.dims.Dimension` objects.

        :param copy: Returns a copy of the dimension dictionary if True
        :type copy: boolean:

        :rtype: Returns the dimension dictionary
        """

        return self._dims.copy() if copy else self._dims

    def dimension(self, name, copy=True):
        """
        Returns the requested :class:`~hypercube.dims.Dimension` object

        :param name: Name of the :class:`~hypercube.dims.Dimension` object
        :type name: str
        :param copy: Returns a copy of the :class:`~hypercube.dims.Dimension` object if True
        :type copy: boolean

        :rtype: :class:`~hypercube.dims.Dimension` object.
        """

        try:
            return create_dimension(name, self._dims[name]) if copy else self._dims[name]
        except KeyError:
            raise KeyError("Dimension '{n}' is not registered "
                "on this cube".format(n=name)), None, sys.exc_info()[2]

    def copy(self):
        """ :rtype: Return a copy of the hypercube """
        return HyperCube(
            dimensions=self.dimensions(copy=False),
            arrays=self.arrays(),
            properties=self.properties())

    def _gen_dimension_table(self):
        """
        2D array describing each registered dimension
        together with headers - for use in __str__
        """
        headers = ['Dimension Name', 'Description',
            'Global Size', 'Extents']

        table = []
        for dimval in sorted(self.dimensions(copy=False).itervalues(),
                             key=lambda dval: dval.name.upper()):

            table.append([dimval.name,
                dimval.description,
                dimval.global_size,
                (dimval.lower_extent, dimval.upper_extent)])

        return table, headers

    def _gen_array_table(self):
        """
        2D array describing each registered array
        together with headers - for use in __str__
        """
        headers = ['Array Name', 'Size', 'Type', 'Shape']

        # Reify arrays to work out their actual size
        reified_arrays = self.arrays(reify=True)

        table = []
        for array in sorted(self.arrays().itervalues(),
                             key=lambda aval: aval.name.upper()):
            # Get the actual size of the array
            nbytes = hcu.array_bytes(reified_arrays[array.name])
            # Print shape tuples without spaces and single quotes
            sshape = '(%s)' % (','.join(map(str, array.shape)),)
            table.append([array.name,
                hcu.fmt_bytes(nbytes),
                np.dtype(array.dtype).name,
                sshape])

        return table, headers

    def _gen_property_table(self):
        """
        2D array describing each registered property
        together with headers - for use in __str__
        """
        headers = ['Property Name', 'Type', 'Value', 'Default Value']

        table = []
        for propval in sorted(self._properties.itervalues(),
                              key=lambda pval: pval.name.upper()):
            table.append([propval.name,
                np.dtype(propval.dtype).name,
                getattr(self, propval.name),
                propval.default])

        return table, headers

    def __str__(self):
        """ Outputs a string representation of this object """

        result = []

        if len(self._dims) > 0:
            table, headers = self._gen_dimension_table()
            result.append("Registered Dimensions:\n%s\n\n" % (
                tabulate(table, headers=headers),))

        if len(self._arrays) > 0:
            table, headers = self._gen_array_table()
            table.append(['Local Memory Usage', self.mem_required(), '', ''])
            result.append("Registered Arrays:\n%s\n\n" % (
                tabulate(table, headers=headers),))

        if len(self._properties) > 0:
            table, headers = self._gen_property_table()
            result.append("Registered Properties:\n%s\n\n" % (tabulate(
                table, headers=headers),))

        return ''.join(result)

    def endpoint_iter(self, *dim_strides, **kwargs):
        """
        Recursively iterate over the (dimension, stride)
        tuples specified in dim_strides, returning the start
        and end indices for each chunk.

        For example, the following call effectively produces
        2 loops over the 'ntime' and 'nchan' dimensions
        in chunks of 10 and 4 respectively.::

            for (ts, te), (cs, ce) in cube.endpoint_iter(('ntime', 10), ('nchan', 4))
                print 'Time range [{ts},{te}] Channel Range [{cs},{ce}]'.format(
                    ts=ts, te=te, cs=cs, ce=ce)

        :param dim_strides: list of (dimension, stride) tuples
        :type dim_strides: list

        :rtype: An iterator
        """

        def _dim_endpoints(size, stride):
            r = xrange(0, size, stride) if stride > 0 else xrange(0, size)
            return ((i, min(i+stride, size)) for i in r)

        dims = self.dimensions(copy=False)
        gens = (_dim_endpoints(dims[d].global_size, s) for d, s in dim_strides)
        return itertools.product(*gens)

    extent_iter = endpoint_iter

    def slice_iter(self, *dim_strides, **kwargs):
        """
        Recursively iterate over the (dimension, stride)
        tuples specified in dim_strides, returning the chunk
        start offsets for each specified dimensions.

        For example, the following call effectively produces
        2 loops over the 'ntime' and 'nchan' dimensions
        in chunks of 10 and 4 respectively.::

            A = np.ones(size=(100, 4))
            for ts, cs in cube.endpoint_iter(('ntime', 10), ('nchan', 4))
                A[ts, cs].sum()

            for i cube.endpoint_iter(('ntime', 10), ('nchan', 4))
                A[i].sum()

        :param dim_strides: list of (dimension, stride) tuples
        :type dim_strides: list

        :rtype: An iterator
        """
        def _create_slices(*args):
            return tuple(slice(s,e,1) for (s, e) in args)

        return (_create_slices(*s) for s in self.endpoint_iter(
            *dim_strides, **kwargs))

    def dim_iter(self, *dim_strides, **kwargs):
        """
        Recursively iterate over the (dimension, stride)
        tuples specified in dim_strides, returning a tuple
        of dictionaries describing a dimension update.

        For example, the following call effectively produces
        2 loops over the 'ntime' and 'nchan' dimensions
        in chunks of 10 and 4 respectively.::

            for d in cube.dim_iter(('ntime', 10), ('nchan', 4))
                cube.update_dimensions(d)

        :param dim_strides: list of (dimension, stride) tuples
        :type dim_strides: list

        :rtype: An iterator
        """

        # Extract dimension names
        dims = [ds[0] for ds in dim_strides]

        def _create_dim_dicts(*args):
            return tuple({ 'name': d,
                    'lower_extent': s,
                    'upper_extent': e
                } for (d, (s, e)) in args)

        # Return a tuple-dict-creating generator
        return (_create_dim_dicts(*zip(dims, s)) for s
            in self.endpoint_iter(*dim_strides, **kwargs))

    def cube_iter(self, *dim_strides, **kwargs):
        """
        Recursively iterate over the (dimension, stride)
        tuples specified in dim_strides, returning cloned hypercubes
        with each of the specified dimensions modified accordingly.

        For example, the following call effectively produces
        2 loops over the 'ntime' and 'nchan' dimensions
        in chunks of 10 and 4 respectively.::

            A = np.ones(size=(100, 4))
            for c in cube.cube_iter(('ntime', 10), ('nchan', 4))
                assert c.dim_extent_size('ntime', 'nchan') == (10, 4)

        :param dim_strides: list of (dimension, stride) tuples
        :type dim_strides: list

        :rtype: An iterator
        """

        def _make_cube(dims, arrays, *args):
            """
            Create a hypercube given dimensions and a list of
            (dim_name, dim_slice) tuples
            """

            # Create new hypercube, registering everything in dims
            cube = HyperCube()
            cube.register_dimensions(dims)
            cube.register_arrays(arrays)

            # Now update dimensions given slice information
            for (d, (s, e)) in args:
                cube.update_dimension(name=d,
                    global_size=dims[d].global_size,
                    lower_extent=s, upper_extent=e)

            return cube

        # Extract dimension names
        dim_names = [ds[0] for ds in dim_strides]
        arrays = (hcu.reify_arrays(self.arrays(), self.dimensions(copy=False))
            if kwargs.get('arrays', False) else {})

        # Return a cube-creating generator
        return (_make_cube(self.dimensions(), arrays, *zip(dim_names, s))
            for s in self.endpoint_iter(*dim_strides, **kwargs))

    def array_extents(self, array_name, **kwargs):
        """
        Return a list of lower and upper extents for
        the given array_name.

        :param array_name: Name of an array registered on this hypercube
        :type array_name: string


        :rtype: A list of (lower_extent, upper_extent) tuples
            associated with each dimension
        """

        A = self.array(array_name, reify=False)
        return self.dim_extents(*A.shape, single=False)

    def array_slice_index(self, array_name, **kwargs):
        """
        Returns a tuple of slices, each slice equal to the
        slice(lower_extent, upper_extent, 1) of the dimensions
        of array_name.

        :param array_name: Name of the array on this cube to slice
        :type array_name: str

        :rtype: A tuple of slice(lower,upper,1) objects
        """

        A = self.array(array_name, reify=False)
        return self.slice_index(*A.shape, single=False)

    def slice_index(self, *slice_dims, **kwargs):
        """
        Returns a tuple of slices, each slice equal to the
        slice(lower_extent, upper_extent, 1) of the dimensions
        supplied in slice_dims. If the dimension is integer d,
        slice(0, d, 1) will be used instead of the lower and upper extents::

            A = np.ones(ntime, na)
            idx = cube.slice_index('ntime','na', 3)
            A[idx].sum()
            ntime, na, components = cube.slice_index('ntime', 'na', 3)
            A[ntime, na, components].sum()

        :type dims: list
        :param dims: list of dimensions which should have slice
                        objects returned.

        :rtype: A tuple containing slices for each dimension in dims
        """
        return tuple(slice(l, u, 1) for l, u in zip(
            self.dim_lower_extent(*slice_dims, single=False),
            self.dim_upper_extent(*slice_dims, single=False)))