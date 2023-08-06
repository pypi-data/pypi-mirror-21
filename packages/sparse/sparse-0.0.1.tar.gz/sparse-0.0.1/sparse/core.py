import operator
from numbers import Number
import numpy as np
import scipy.sparse


class COO(object):
    """ A Sparse Multidimensional Array

    This is stored in COO format.  It depends on NumPy and Scipy.sparse for
    computation, but supports arrays of arbitrary dimension.

    Parameters
    ----------
    coords: np.ndarray (ndim, nnz)
        An array holding the index locations of every value
        Should have shape (number of dimensions, number of non-zeros)
    data: np.array (nnz,)
        An array of Values
    shape: tuple (ndim,), optional
        The shape of the array

    Examples
    --------
    >>> x = np.eye(4)
    >>> x[2, 3] = 5
    >>> s = COO.from_numpy(x)
    >>> s
    <COO: shape=(4, 4), dtype=float64, nnz=5>
    >>> s.data
    array([ 1.,  1.,  1.,  5.,  1.])
    >>> s.coords
    array([[0, 1, 2, 2, 3],
           [0, 1, 2, 3, 3]], dtype=uint8)

    >>> s.dot(s.T).sum(axis=0).todense()
    array([  1.,   1.,  31.,   6.])

    Make a sparse array by passing in an array of coordinates and an array of
    values.

    >>> coords = [[0, 0, 0, 1, 1],
    ...           [0, 1, 2, 0, 3],
    ...           [0, 3, 2, 0, 1]]
    >>> data = [1, 2, 3, 4, 5]
    >>> y = COO(coords, data, shape=(3, 4, 5))
    >>> y
    <COO: shape=(3, 4, 5), dtype=int64, nnz=5>
    >>> tensordot(x, y, axes=(0, 1))
    <COO: shape=(4, 3, 5), dtype=float64, nnz=6>

    See Also
    --------
    COO.from_numpy
    COO.from_scipy_sparse
    """
    def __init__(self, coords, data=None, shape=None, has_duplicates=True):
        if shape is None:
            shape = tuple(ind.max(axis=0).tolist())
        if data is None and isinstance(coords, (tuple, list)):
            if coords:
                assert len(coords[0]) == 2
            data = list(pluck(1, coords))
            coords = list(pluck(0, coords))

        self.shape = tuple(shape)
        self.data = np.asarray(data)
        self.coords = np.asarray(coords)
        self.coords = self.coords.astype(np.min_scalar_type(max(self.shape)))
        assert len(data) == self.coords.shape[1]
        self.has_duplicates = has_duplicates

    @classmethod
    def from_numpy(cls, x):
        coords = np.where(x)
        data = x[coords]
        coords = np.vstack(coords)
        return cls(coords, data, shape=x.shape)

    def todense(self):
        self = self.sum_duplicates()
        x = np.zeros(shape=self.shape, dtype=self.dtype)
        coords = tuple([self.coords[i, :] for i in range(self.ndim)])
        x[coords] = self.data
        return x

    @classmethod
    def from_scipy_sparse(cls, x):
        x = scipy.sparse.coo_matrix(x)
        coords = np.empty((2, x.nnz), dtype=x.row.dtype)
        coords[0, :] = x.row
        coords[1, :] = x.col
        return COO(coords, x.data, shape=x.shape, has_duplicates=x.has_canonical_format)

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def nnz(self):
        return self.coords.shape[1]

    @property
    def nbytes(self):
        return self.data.nbytes + self.coords.nbytes

    def __getitem__(self, index):
        if not isinstance(index, tuple):
            index = (index,)
        index = tuple(ind + self.shape[i] if isinstance(ind, int) and ind < 0 else ind
                      for i, ind in enumerate(index))
        mask = np.ones(self.nnz, dtype=bool)
        for i, ind in enumerate([i for i in index if i is not None]):
            if ind == slice(None, None):
                continue
            mask &= _mask(self.coords[i], ind)

        n = mask.sum()
        coords = []
        shape = []
        i = 0
        for ind in index:
            if isinstance(ind, int):
                i += 1
                continue
            elif isinstance(ind, slice):
                shape.append(min(ind.stop, self.shape[i]) - ind.start)
                coords.append(self.coords[i][mask] - ind.start)
                i += 1
            elif isinstance(ind, list):
                old = self.coords[i][mask]
                new = np.empty(shape=old.shape, dtype=old.dtype)
                for j, item in enumerate(ind):
                    new[old == item] = j
                coords.append(new)
                shape.append(len(ind))
                i += 1
            elif ind is None:
                coords.append(np.zeros(n))
                shape.append(1)

        for j in range(i, self.ndim):
            coords.append(self.coords[j][mask])
            shape.append(self.shape[j])

        coords = np.stack(coords, axis=0)
        shape = tuple(shape)
        data = self.data[mask]

        return COO(coords, data, shape=shape, has_duplicates=self.has_duplicates)

    def __str__(self):
        return "<COO: shape=%s, dtype=%s, nnz=%d>" % (self.shape, self.dtype,
                self.nnz)

    __repr__ = __str__

    def reduction(self, method, axis=None, keepdims=False):
        if axis is None:
            axis = tuple(range(self.ndim))

        if isinstance(axis, int):
            axis = (axis,)

        if set(axis) == set(range(self.ndim)):
            result = getattr(self.data, method)()
        else:
            axis = tuple(axis)

            neg_axis = list(range(self.ndim))
            for ax in axis:
                neg_axis.remove(ax)
            neg_axis = tuple(neg_axis)

            a = self.transpose(axis + neg_axis)
            a = a.reshape((np.prod([self.shape[d] for d in axis]),
                           np.prod([self.shape[d] for d in neg_axis])))

            a = a.to_scipy_sparse()
            a = getattr(a, method)(axis=0)
            a = COO.from_scipy_sparse(a)
            a = a.reshape([self.shape[d] for d in neg_axis])
            result = a

        if keepdims:
            result = _keepdims(self, result, axis)
        return result

    def sum(self, axis=None, keepdims=False):
        return self.reduction('sum', axis=axis, keepdims=keepdims)

    def max(self, axis=None, keepdims=False):
        x = self.reduction('max', axis=axis, keepdims=keepdims)
        # TODO: verify that there are some missing elements in each entry
        if isinstance(x, COO):
            x.data[x.data < 0] = 0
            return x
        elif isinstance(x, np.ndarray):
            x[x < 0] = 0
            return x
        else:
            return np.max(x, 0)

    def transpose(self, axes=None):
        if axes is None:
            axes = tuple(reversed(range(self.ndim)))

        shape = tuple(self.shape[ax] for ax in axes)
        return COO(self.coords[axes, :], self.data, shape)

    @property
    def T(self):
        return self.transpose(list(range(self.ndim))[::-1])

    def dot(self, other):
        return tensordot(self, other,
                         axes=((self.ndim - 1,), (other.ndim - 2,)))

    def reshape(self, shape):
        if any(d == -1 for d in shape):
            extra = int(np.prod(self.shape) /
                        np.prod([d for d in shape if d != -1]))
            shape = tuple([d if d != -1 else extra for d in shape])
        linear_loc = np.zeros(self.nnz, dtype=np.min_scalar_type(np.prod(self.shape)))
        strides = 1
        for i, d in enumerate(self.shape[::-1]):
            linear_loc += self.coords[-(i + 1), :] * strides
            strides *= d

        coords = np.empty((len(shape), self.nnz), dtype=self.coords.dtype)
        strides = 1
        for i, d in enumerate(shape[::-1]):
            coords[-(i + 1), :] = linear_loc // strides % d
            strides *= d

        return COO(coords, self.data, shape, has_duplicates=self.has_duplicates)

    def to_scipy_sparse(self):
        assert self.ndim == 2
        import scipy.sparse
        return scipy.sparse.coo_matrix((self.data,
                                        (self.coords[0],
                                         self.coords[1])),
                                        shape=self.shape)

    def sum_duplicates(self):
        if not self.has_duplicates:
            return self
        x = (self.reshape((np.prod(self.shape), 1))
                 .to_scipy_sparse())
        x.sum_duplicates()
        # TODO: we may be able to do this faster
        result = COO.from_scipy_sparse(x).reshape(self.shape)
        result.has_duplicates = False
        return result

    def __add__(self, other):
        if not isinstance(other, COO):
            raise NotImplementedError(
                "adding to scalars or dense arrays would cause the result "
                "to be dense")
        if self.shape == other.shape:
            return COO(np.concatenate([self.coords, other.coords], axis=1),
                       np.concatenate([self.data, other.data]),
                       self.shape, has_duplicates=True)
        else:
            raise NotImplementedError("Broadcasting not yet supported")

    def __neg__(self):
        return COO(self.coords, -self.data, self.shape, self.has_duplicates)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return self.elemwise(operator.mul, other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self.elemwise(operator.truediv, other)

    def __floordiv__(self, other):
        return self.elemwise(operator.floordiv, other)

    __div__ = __truediv__

    def __pow__(self, other):
        return self.elemwise(operator.pow, other)

    def elemwise(self, func, *args, **kwargs):
        if func(0, *args, **kwargs) != 0:
            raise ValueError("Performing this operation would produce "
                    "a dense result: %s" % str(func))
        return COO(self.coords, func(self.data, *args, **kwargs),
                   shape=self.shape, has_duplicates=self.has_duplicates)

    def expm1(self):
        return self.elemwise(np.expm1)

    def log1p(self):
        return self.elemwise(np.log1p)

    def sin(self):
        return self.elemwise(np.sin)

    def sinh(self):
        return self.elemwise(np.sinh)

    def tan(self):
        return self.elemwise(np.tan)

    def tanh(self):
        return self.elemwise(np.tanh)

    def sqrt(self):
        return self.elemwise(np.sqrt)

    def ceil(self):
        return self.elemwise(np.ceil)

    def floor(self):
        return self.elemwise(np.floor)

    def round(self, decimals=0):
        return self.elemwise(np.round, decimals)

    def rint(self):
        return self.elemwise(np.rint)

    def conj(self):
        return self.elemwise(np.conj)

    def conjugate(self):
        return self.elemwise(np.conjugate)

    def astype(self, dtype):
        return self.elemwise(np.astype, dtype)

    def __gt__(self, other):
        if not isinstance(other, Number):
            raise NotImplementedError("Only scalars supported")
        if other < 0:
            raise ValueError("Comparison with negative number would produce "
                             "dense result")
        return self.elemwise(operator.gt, other)

    def __ge__(self, other):
        if not isinstance(other, Number):
            raise NotImplementedError("Only scalars supported")
        if other <= 0:
            raise ValueError("Comparison with negative number would produce "
                             "dense result")
        return self.elemwise(operator.ge, other)


def tensordot(a, b, axes=2):
    # Much of this is stolen from numpy/core/numeric.py::tensordot
    # Please see license at https://github.com/numpy/numpy/blob/master/LICENSE.txt
    try:
        iter(axes)
    except:
        axes_a = list(range(-axes, 0))
        axes_b = list(range(0, axes))
    else:
        axes_a, axes_b = axes
    try:
        na = len(axes_a)
        axes_a = list(axes_a)
    except TypeError:
        axes_a = [axes_a]
        na = 1
    try:
        nb = len(axes_b)
        axes_b = list(axes_b)
    except TypeError:
        axes_b = [axes_b]
        nb = 1

    # a, b = asarray(a), asarray(b)  # <--- modified
    as_ = a.shape
    nda = a.ndim
    bs = b.shape
    ndb = b.ndim
    equal = True
    if na != nb:
        equal = False
    else:
        for k in range(na):
            if as_[axes_a[k]] != bs[axes_b[k]]:
                equal = False
                break
            if axes_a[k] < 0:
                axes_a[k] += nda
            if axes_b[k] < 0:
                axes_b[k] += ndb
    if not equal:
        raise ValueError("shape-mismatch for sum")

    # Move the axes to sum over to the end of "a"
    # and to the front of "b"
    notin = [k for k in range(nda) if k not in axes_a]
    newaxes_a = notin + axes_a
    N2 = 1
    for axis in axes_a:
        N2 *= as_[axis]
    newshape_a = (-1, N2)
    olda = [as_[axis] for axis in notin]

    notin = [k for k in range(ndb) if k not in axes_b]
    newaxes_b = axes_b + notin
    N2 = 1
    for axis in axes_b:
        N2 *= bs[axis]
    newshape_b = (N2, -1)
    oldb = [bs[axis] for axis in notin]

    at = a.transpose(newaxes_a).reshape(newshape_a)
    bt = b.transpose(newaxes_b).reshape(newshape_b)
    res = dot(at, bt)
    res = COO.from_scipy_sparse(res)  # <--- modified
    return res.reshape(olda + oldb)


def dot(a, b):
    if isinstance(b, COO) and not isinstance(a, COO):
        return dot(b.T, a.T).T
    aa = a.to_scipy_sparse()
    aa.has_canonical_format = a.has_duplicates
    aa = aa.tocsr()

    b_original = b
    if isinstance(b, COO):
        b = b.to_scipy_sparse()
    if isinstance(b, scipy.sparse.spmatrix):
        b.has_canonical_format = b_original.has_duplicates
        b = b.tocsc()
    return aa.dot(b)


def _keepdims(original, new, axis):
    shape = list(original.shape)
    for ax in axis:
        shape[ax] = 1
    return new.reshape(shape)


def _mask(coords, idx):
    if isinstance(idx, int):
        return coords == idx
    elif isinstance(idx, slice):
        if idx.step not in (1, None):
            raise NotImplementedError("Steped slices not implemented")
        return (coords >= idx.start) & (coords < idx.stop)
    elif isinstance(idx, list):
        mask = np.zeros(len(coords), dtype=bool)
        for item in idx:
            mask |= coords == item
        return mask


def concatenate(arrays, axis=0):
    if axis < 0:
        axis = axis + arrays[0].ndim
    assert all(x.shape[ax] == arrays[0].shape[ax]
               for x in arrays
               for ax in set(range(arrays[0].ndim)) - {axis})
    data = np.concatenate([x.data for x in arrays])
    coords = np.concatenate([x.coords for x in arrays], axis=1)

    nnz = 0
    dim = 0
    for x in arrays:
        if dim:
            coords[axis, nnz:x.nnz + nnz] += dim
        dim += x.shape[axis]
        nnz += x.nnz

    shape = list(arrays[0].shape)
    shape[axis] = dim
    has_duplicates = any(x.has_duplicates for x in arrays)

    return COO(coords, data, shape=shape, has_duplicates=has_duplicates)


def stack(arrays, axis=0):
    assert len(set(x.shape for x in arrays)) == 1
    if axis < 0:
        axis = axis + arrays[0].ndim + 1
    data = np.concatenate([x.data for x in arrays])
    coords = np.concatenate([x.coords for x in arrays], axis=1)

    nnz = 0
    dim = 0
    new = np.empty(shape=(coords.shape[1],), dtype=coords.dtype)
    for x in arrays:
        new[nnz:x.nnz + nnz] = dim
        dim += 1
        nnz += x.nnz

    shape = list(arrays[0].shape)
    shape.insert(axis, len(arrays))
    has_duplicates = any(x.has_duplicates for x in arrays)
    coords = [coords[i] for i in range(coords.shape[0])]
    coords.insert(axis, new)
    coords = np.stack(coords, axis=0)

    return COO(coords, data, shape=shape, has_duplicates=has_duplicates)
