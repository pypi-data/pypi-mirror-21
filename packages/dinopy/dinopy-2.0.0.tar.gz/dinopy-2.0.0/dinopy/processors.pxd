# -*- coding: utf-8 -*-
from cpython cimport PyObject_CheckBuffer
cimport numpy as np
from libc.math cimport pow as cpow

from dinopy.definitions cimport *

from .conversion cimport encode, encode_twobit, encode_fourbit
from .shape cimport Shape
from .definitions cimport valid_dtypes
from .definitions cimport _iupac_mapping

cpdef reverse_complement(object seq)
cdef object _reverse_complement(object seq)
cpdef uint64 reverse_complement_2bit(uint64 seq, unsigned int seq_length=*, bint sentinel=*)
cpdef uint64 reverse_complement_4bit(uint64 seq, unsigned int seq_length=*, bint sentinel=*)
cpdef complement(object seq)
cdef object _forward_complement(object seq)
cdef unsigned char msb64(uint64 x)
cpdef uint64 complement_2bit(uint64 seq, unsigned int seq_length=*, bint sentinel=*)
cpdef uint64 complement_4bit(uint64 seq, unsigned int seq_length=*, bint sentinel=*)
cpdef np.uint64_t[:] suffix_array(object sequence)
