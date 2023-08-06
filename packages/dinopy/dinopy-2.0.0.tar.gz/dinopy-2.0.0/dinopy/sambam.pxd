# -*- coding: utf-8 -*-
"""
Common declarations for SAM/BAM handling
"""

cdef struct Flag:
    int integer_representation,
    bint template_having_multiple_segments_in_sequencing, each_segment_properly_aligned, segment_unmapped, next_segment_in_template_unmapped, reverse_complemented, next_segment_reverse_complemented, first_segment, last_segment, secondary_alignment, not_passing_filters, pcr_or_optical_duplicate, supplementary_alignment  # TODO proper naming, esp: prefix with 'is_'?

cdef class AlignmentRecord:
    cdef public:
        str query_name, rname, cigar, rnext, query_sequence, qual
        int pos, mapping_quality, pnext, template_length
        dict optional
        Flag flag
    cdef readonly str optional_raw
    cpdef str get_sam_repr(self)

cdef str _raw_opt_string_from_dict(dict d)

cpdef int create_flag(bint template_having_multiple_segments_in_sequencing=*,
                      bint each_segment_properly_aligned=*,
                      bint segment_unmapped=*,
                      bint next_segment_in_template_unmapped=*,
                      bint reverse_complemented=*,
                      bint next_segment_reverse_complemented=*,
                      bint first_segment=*,
                      bint last_segment=*,
                      bint secondary_alignment=*,
                      bint not_passing_filters=*,
                      bint pcr_or_optical_duplicate=*,
                      bint supplementary_alignment=*)

cdef void _split_flag(AlignmentRecord al)
cdef void _combine_flag(AlignmentRecord ar)

cpdef str cigar_str_from_tuples(list tuples)
cpdef str cigar_str_from_pysam_cigartuples(list tuples)
cpdef list tuples_from_cigar_str(str cigar)
cpdef list pysam_cigartuples_from_cigar_str(str cigar)

cpdef str get_flag_description(AlignmentRecord al)
