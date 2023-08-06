# -*- coding: utf-8 -*-
from .output_opener cimport OutputOpener
from .sambam cimport AlignmentRecord

cdef class SamWriter(OutputOpener):
    cpdef void write_header_line(self, str tag, dict items)
    cpdef void write_header(self, list lines)
    cpdef void write_sq_header(self, list reference_names, list reference_lengths)
    cpdef list create_header_sq_lines(self, list reference_names, list reference_lengths)
    cpdef void write_record(self, AlignmentRecord ar)
    cpdef void write_records(self, c)
