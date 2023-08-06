# -*- coding: utf-8 -*-
"""For reading SAM files, duh.

"""
from .input_opener cimport InputOpener as InputOpener
from .sambam cimport AlignmentRecord

cdef dict _parse_any_header_line(str line)  # for conversion of "k1:v1\tk2:v2\t...\kn:vn" to {k1: v1, k2: v2, ..., kn: vn}
cdef tuple _parse_header_line(str line)  # basically just (tag, _parse_any_header_line(line))

cdef AlignmentRecord parse_alignment_record(str line)

cdef class SamReader:
    cdef str _samfile
    cpdef list get_header(self)
