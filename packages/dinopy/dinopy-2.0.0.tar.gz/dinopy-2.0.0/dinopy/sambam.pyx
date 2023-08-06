# -*- coding: utf-8 -*-
"""
Common declarations for SAM/BAM handling, most prominently `AlignmentReord` which corresponds to a single line in a standard SAM file.
"""
from binascii import hexlify

from .sam_reader cimport parse_alignment_record
import numpy as np
cimport numpy as np

cdef class AlignmentRecord:
    """An AlignmentRecord resembles a single line in a SAM file and consists of exactly 11 (*or 12*) columns:

        ========== ==== ===== === =============== ===== ===== ===== =============== === ==== ==========
        query_name flag rname pos mapping_quality cigar rnext pnext template_length seq qual (optional)
        ========== ==== ===== === =============== ===== ===== ===== =============== === ==== ==========

       AlignmentRecords are not orderable but can be compared for (in-)equality: Two AlignmentRecords are equal
       iff all of their fields are equal. For example::

            ar1 = AlignmentRecord.fromvalues('r004', 0, 'ref', 16, 30, '6M14N5M', '*', 0, 0, 'ATAGCTTCAGC', '*', None)
            ar2 = AlignmentRecord.fromvalues('r003', 0, 'ref', 16, 30, '6M14N5M', '*', 0, 0, 'ATAGCTTCAGC', '*', None)
            assert(ar1 != ar2)  # True
    """
    def __init__(self):
        pass

    @classmethod
    def fromstr(cls, str s):
        """Create a new `AlignmentRecord` from a given string (as found in SAM files, i.e. 11+ tab delimited columns),
        with **1-based** positions. AlignmentRecords are 0-based internally, only SAM string representations use 1-based
        positions (as per SAM specifications).

        Arguments:
            s (str): A string describing an AlignmentRecord (as found in SAM files, i.e. 11+ tab delimited columns)

        Examples:

            1. No optional column, literal tabs::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromstr("r001	99	ref	7	30	8M2I4M1D3M	=	37	39	TTAGATAAAGGATACTG	*")

            2. No optional column, escaped tabs::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromstr("r004\\t0\\tref\\t16\\t30\\t6M14N5M\\t*\\t0\\t0\\tATAGCTTCAGC\\t*")

            3. With optional column, literal tabs::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromstr("r003	2064	ref	29	17	6H5M	*	0	0	TAGGC	*	SA:Z:ref,9,+,5S6M,30,1;")
        """
        return parse_alignment_record(s)

    @classmethod
    def fromdict(cls, dict d, bint fill_missing=True):
        """Create a new `AlignmentRecord` from a given dictionary. **0-based** positions.

        Arguments:

            d (dict): dictionary containing necessary information to create an AlignmentRecord, i.e.
                      ``{'query_name': a, 'flag': b, 'rname': c, 'pos': d, 'mapping_quality': e, 'cigar': f, 'rnext': g, 'pnext': h, 'template_length': i, 'query_sequence': j, 'qual': k, 'optional': l}``
                      where some of the fields may be omitted (see ``fill_missing``).

            fill_missing (bool): If ``False``, missing fields will raise a KeyError.
                                 If ``True``, missing fields will be assigned their respective default value.
                                 (Default: ``True``).

                                 The following fields, if omitted, will be replaced by their respective default values:

                                 =============== =============
                                 Field           Default value
                                 --------------- -------------
                                 query_name      '*'
                                 rname           '*'
                                 cigar           '*'
                                 rnext           '*'
                                 qual            '*'
                                 seq             '*'
                                 mapping_quality  255
                                 pos              0
                                 pnext            0
                                 template_length  0
                                 =============== =============

        Other validations performed by this method:

          - length of *qual* and *seq* must match
          - if *qual* and *seq* are given and *qual* is not '*', *seq* must not be '*'

        Other operations performed by this method:

          - The value of *flag* will both get stored in AlignmentRecord.flag.integer_representation and split into its parts (i.e. all of the other fields in `AlignmentRecord.flag`.

        Examples:

            1. No optional column::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromdict({'query_name': 'r001', 'flag': 99, 'rname': 'ref', 'pos': 7, 'mapping_quality': 30, 'cigar': '8M2I4M1D3M', 'rnext': '=', 'pnext': 37, 'template_length': 39, 'query_sequence': 'TTAGATAAAGGATACTG', 'qual': '*', 'optional': None})

        """
        cdef AlignmentRecord record = cls()
        cdef str k, s, i
        cdef set opt_str, opt_int
        cdef int i_default

        opt_str = {'query_name', 'rname', 'cigar', 'rnext', 'qual', 'query_sequence'}
        opt_int = {('mapping_quality', 255), ('pos', 0), ('pnext', 0), ('template_length', 0)}

        for s in opt_str:
            if s not in d:
                if fill_missing:
                    d[s] = '*'
                else:
                    raise KeyError("Missing information for {}".format(s))
        for (i, i_default) in opt_int:
            if i not in d:
                if fill_missing:
                    d[i] = i_default
                else:
                    raise KeyError("Missing information for {}".format(s))

        if 'qual' in d and 'query_sequence' in d:
            if d['query_sequence'] == '*' and d['qual'] != '*':
                raise ValueError("query_sequence must not be '*' when qual is not '*'.")
            if d['qual'] != '*' and len(d['qual']) != len(d['query_sequence']):
                raise ValueError("Length of query_sequence ({}) and qual ({}) need to match.".format(len(d['query_sequence']), len(d['qual'])))

        for k, v in d.items():
            if k is 'flag':
                record.flag.integer_representation = v
                _split_flag(record)
            else:
                record.__setattr__(k, v)
        if 'optional' in d:
            record.optional_raw = _raw_opt_string_from_dict(d['optional'])
        else:
            record.optional_raw = None
        return record

    @classmethod
    def fromkeywords(cls, str qname="*", int flag=0, str rname="*", int pos=0, int mapq=255, str cigar="*", str rnext="*", int pnext=0, int tlen=0, str seq="*", str qual="*", dict optional=None):
        """Same as `AlignmentRecord.fromvalues` but with keyword arguments instead. **0-based** positions.

        Arguments:
            qname (str): Default ``"*"``.
            flag (int): Default ``0``.
            rname (str): Default ``"*"``.
            pos (int): Default ``0``.
            mapq (int): Default ``255``.
            cigar (str): Default ``"*"``.
            rnext (str): Default ``"*"``.
            pnext (int): Default ``0``.
            tlen (int): Default ``0``.
            seq (str): Default ``"*"``.
            qual (str): Default ``"*"``.
            optional (dict): Default ``None``.

        Examples:

            1. Specifying everything::

                from dinopy.sambam import AlignmentRecord
                # r001	99	ref	7	30	8M2I4M1D3M	=	37	39	TTAGATAAAGGATACTG	*
                ar = AlignmentRecord.fromkeywords(qname="r001", flag=99, rname="ref", pos=7, mapq=30, cigar="8M2I4M1D3M", rnext="=", pnext=37, tlen=39, seq="TTAGATAAAGGATACTG", qual="*", optional=None)

            2. Only specify arguments that do not have the default values::

                from dinopy.sambam import AlignmentRecord
                # r002	0	ref	9	30	3S6M1P1I4M	*	0	0	AAAAGATAAGGATA	*
                ar = AlignmentRecord.fromkeywords(qname="r002", rname="ref", pos=9, mapq=30, cigar="3S6M1P1I4M", seq="AAAAGATAAGGATA", optional=None)

        """
        return AlignmentRecord.fromvalues(qname, flag, rname, pos, mapq, cigar, rnext, pnext, tlen, seq, qual, optional)

    @classmethod
    def fromvalues(cls, str qname, int flag, str rname, int pos, int mapq, str cigar, str rnext, int pnext, int tlen, str seq, str qual, dict optional):
        """Create a new `AlignmentRecord` using the specified arguments.
        `optional` is a dictionary of the form ``{'XY' : Z, }`` (where ``'XY'`` is a two character *tag* and Z its value, omitting the type usually found in SAM files because it can be inferred) with any optional (surprise!) columns. For more information on optional columns, see the `SAM specification <https://samtools.github.io/hts-specs/SAMv1.pdf>`_.
        Also see `create_flag` for a convenient way to calculate the *flag* argument.
        **0-based** positions.


        Examples:

            1. No optional column::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromvalues('r004', 0, 'ref', 16, 30, '6M14N5M', '*', 0, 0, 'ATAGCTTCAGC', '*', None)

            2. With optional column::

                from dinopy.sambam import AlignmentRecord
                ar = AlignmentRecord.fromvalues('r003', 0, 'ref', 9, 30, '5S6M', '*', 0, 0, 'GCCTAAGCTAA', '*', {'SA': 'ref,29,-,6H5M,17,0;'})

        .. important:: Does not perform any validation whatsoever.

        """
        cdef AlignmentRecord record = cls()
        # TODO mandatory vs optional column handling
        record.query_name = qname
        record.flag.integer_representation = flag
        _split_flag(record)
        record.rname = rname
        record.pos = pos
        record.mapping_quality = mapq
        record.cigar = cigar
        record.rnext = rnext
        record.pnext = pnext
        record.template_length = tlen
        record.query_sequence = seq
        record.qual = qual
        record.optional = optional
        record.optional_raw = _raw_opt_string_from_dict(optional)
        return record

    def __repr__(self):
        return self.get_sam_repr()

    def __richcmp__(self, AlignmentRecord record, int cmp_type):
        cdef bint eq = True
        cdef Flag flag = self.flag
        if cmp_type == 2 or cmp_type == 3:  # 2 for equality, 3 for inequality, negated later
            eq &= record.query_name == self.query_name
            eq &= record.flag.integer_representation == flag.integer_representation  # somehow, fully qualified names for structs breaks things, i.e. self.flag.integer_representation does not work
            eq &= record.rname == self.rname
            eq &= record.pos == self.pos
            eq &= record.mapping_quality == self.mapping_quality
            eq &= record.cigar == self.cigar
            eq &= record.rnext == self.rnext
            eq &= record.pnext == self.pnext
            eq &= record.template_length == self.template_length
            eq &= record.query_sequence == self.query_sequence
            eq &= record.qual == self.qual

            def cmp_dict(dict a, dict b):  # Sadly, this is needed because dicts *may* contain `np.ndarray` values which don't result in a boolean when compared using `==`.
                equal = True
                if np.ndarray in set(map(type, a.values())) | set(map(type, b.values())):
                    for key in a.keys() | b.keys():
                        if key in a and key in b and type(a[key]) == np.array and type(b[key]) == np.array:
                            equal &= np.all(a[key] == b[key])
                        elif (key in a and key not in b) or (key not in a and key in b):
                            equal = False
                            break
                        elif key in a and key in b:
                            equal &= a[key] == [key]
                else:
                    equal = a == b
                return equal

            if record.optional and self.optional:
                eq &= cmp_dict(record.optional, self.optional)
            elif record.optional_raw and self.optional_raw:
                eq &= record.optional_raw == self.optional_raw
            elif record.optional and self.optional_raw:
                eq &= _raw_opt_string_from_dict(record.optional) == self.optional_raw
            elif record.optional_raw and self.optional:
                eq &= record.optional_raw == _raw_opt_string_from_dict(self.optional)

        else:
            raise ValueError("AlignmentRecords can only be tested for (in-)equality; they can't be ordered.")
        if cmp_type == 3:
            return not eq
        return eq

    cpdef str get_sam_repr(self):
        """Returns the AlignmentRecords representation as seen in SAM files, i.e. 11 TAB-delimited values if the optional (column) is None, 12 TAB-delimited values otherwise.
        Note that positions are stored 0-based internally but displayed as 1-based positions as per the SAM specification. 
        """
        if self.optional == {} or self.optional is None:
            return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                self.query_name, self.flag.integer_representation, self.rname, self.pos + 1, self.mapping_quality, self.cigar, self.rnext, self.pnext + 1, self.template_length,
                self.query_sequence, self.qual)
        else:
            return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                self.query_name, self.flag.integer_representation, self.rname, self.pos + 1, self.mapping_quality, self.cigar, self.rnext, self.pnext + 1, self.template_length,
                self.query_sequence, self.qual, self.optional_raw if self.optional_raw else _raw_opt_string_from_dict(self.optional))

    def __str__(self):
        return self.__repr__()

cdef str _raw_opt_string_from_dict(dict d):
    """Creates a SAM representation of given optional columns.
    Dictionary entries of the form ``'XY': Z`` are expected, where ``'XY'`` is a two-character *tag* (see `SAM specification <https://samtools.github.io/hts-specs/SAMv1.pdf>`_ for more information)
    and ``Z`` is its value. The SAM specification actually stores additional columns in the form ``XY:T:Z`` -- in addition to tag and value,
    it also expects a type ``T``. As this can be derived from the value, there is no need to explicitly specify the type.

    Args:
        d:

    Returns:

    """
    cdef dict type_char_lookup = {str: 'Z', int: 'i', float: 'f'}, type_value  # char: 'A'
    cdef type t
    cdef list raw_opt_list = []
    if d is None or len(d) == 0:
        return None
    for key, value in d.items():
        t = type(value)
        if t in type_char_lookup:
            if t is str and len(value) == 1:  # there is no character datatype in python; characters are length 1 strings.
                raw_opt_list.append("{}:A:{}".format(key, value))
            else:
                raw_opt_list.append("{}:{}:{}".format(key, type_char_lookup[t], value))
        else:  # H, Byte array in the Hex format; B, Integer or numeric array  --  not yet supported
            if t in (bytes, bytearray):
                raw_opt_list.append("{}:H:{}".format(key, hexlify(value).decode('ascii')))
            elif t in (list, np.ndarray):
                type_value = {np.uint16: 'S', np.int16: 's', np.uint32: 'I', np.int32: 'i', np.uint8: 'C', np.float: 'f', np.int8: 'c', int: 'i', float: 'f'}
                raw_opt_list.append("{}:B:{}{}".format(key, type_value[type(value[0])], ','.join(map(str, value))))
            else:
                raise TypeError("Unsupported type {} for value {}".format(type(value), value))
    return "\t".join(raw_opt_list).rstrip()

cpdef int create_flag(bint template_having_multiple_segments_in_sequencing=False,
                      bint each_segment_properly_aligned=False,
                      bint segment_unmapped=False,
                      bint next_segment_in_template_unmapped=False,
                      bint reverse_complemented=False,
                      bint next_segment_reverse_complemented=False,
                      bint first_segment=False,
                      bint last_segment=False,
                      bint secondary_alignment=False,
                      bint not_passing_filters=False,
                      bint pcr_or_optical_duplicate=False,
                      bint supplementary_alignment=False):
    """Calculates the integer representation ("Flag") of the combination of given boolean attributes

    Arguments:
        template_having_multiple_segments_in_sequencing:
        each_segment_properly_aligned:
        segment_unmapped:
        next_segment_in_template_unmapped:
        reverse_complemented:
        next_segment_reverse_complemented:
        first_segment:
        last_segment:
        secondary_alignment:
        not_passing_filters:
        pcr_or_optical_duplicate:
        supplementary_alignment:

    Returns:
        the integer representation ("Flag") of the combination of given boolean attributes

    Examples:

        1. Integer describing the flag when ``reverse_complemented`` and ``first_segment`` are set::

            from dinopy.sambam import create_flag
            create_flag(reverse_complemented=True, first_segment=True)  # 80 == 16 + 64 == 0b1000000 | 0b0010000

    """
    cdef int integer_representation = 0
    if template_having_multiple_segments_in_sequencing:
        integer_representation |= 0x1
    if each_segment_properly_aligned:
        integer_representation |= 0x2
    if segment_unmapped:
        integer_representation |= 0x4
    if next_segment_in_template_unmapped:
        integer_representation |= 0x8
    if reverse_complemented:
        integer_representation |= 0x10
    if next_segment_reverse_complemented:
        integer_representation |= 0x20
    if first_segment:
        integer_representation |= 0x40
    if last_segment:
        integer_representation |= 0x80
    if secondary_alignment:
        integer_representation |= 0x100
    if not_passing_filters:
        integer_representation |= 0x200
    if pcr_or_optical_duplicate:
        integer_representation |= 0x400
    if supplementary_alignment:
        integer_representation |= 0x800
    return integer_representation

cdef void _split_flag(AlignmentRecord ar):
    """Splits a flag - or more precisely its integer_representation - into single attributes as defined in `Flag`.

    Arguments:
        ar (AlignmentRecord): Object with a set value for the ``flag.integer_representation`` attribute.
    """
    flag = ar.flag.integer_representation
    ar.flag.template_having_multiple_segments_in_sequencing = flag & 0x1
    ar.flag.each_segment_properly_aligned = flag & 0x2
    ar.flag.segment_unmapped = flag & 0x4
    ar.flag.next_segment_in_template_unmapped = flag & 0x8
    ar.flag.reverse_complemented = flag & 0x10
    ar.flag.next_segment_reverse_complemented = flag & 0x20
    ar.flag.first_segment = flag & 0x40
    ar.flag.last_segment = flag & 0x80
    ar.flag.secondary_alignment = flag & 0x100
    ar.flag.not_passing_filters = flag & 0x200
    ar.flag.pcr_or_optical_duplicate = flag & 0x400
    ar.flag.supplementary_alignment = flag & 0x800

cdef void _combine_flag(AlignmentRecord ar):
    """

    Arguments:
        ar:

    Returns:

    .. important:: overrides ``ar.flag.integer_representation``.
    """
    if ar.flag.integer_representation != 0:
        # TODO issue warning that integer_representation will be overriden?
        pass
    ar.flag.integer_representation = 0
    if ar.flag.template_having_multiple_segments_in_sequencing:
        ar.flag.integer_representation |= 0x1
    if ar.flag.each_segment_properly_aligned:
        ar.flag.integer_representation |= 0x2
    if ar.flag.segment_unmapped:
        ar.flag.integer_representation |= 0x4
    if ar.flag.next_segment_in_template_unmapped:
        ar.flag.integer_representation |= 0x8
    if ar.flag.reverse_complemented:
        ar.flag.integer_representation |= 0x10
    if ar.flag.next_segment_reverse_complemented:
        ar.flag.integer_representation |= 0x20
    if ar.flag.first_segment:
        ar.flag.integer_representation |= 0x40
    if ar.flag.last_segment:
        ar.flag.integer_representation |= 0x80
    if ar.flag.secondary_alignment:
        ar.flag.integer_representation |= 0x100
    if ar.flag.not_passing_filters:
        ar.flag.integer_representation |= 0x200
    if ar.flag.pcr_or_optical_duplicate:
        ar.flag.integer_representation |= 0x400
    if ar.flag.supplementary_alignment:
        ar.flag.integer_representation |= 0x800

cpdef str cigar_str_from_tuples(list tuples):
    cdef:
        int count
        char symbol
        str result

    result = "".join(["{}{}".format(count if count > 1 else "", symbol) for count, symbol in tuples])
    return result

cpdef list tuples_from_cigar_str(str cigar):
    cdef:
        list result = []  # MIDNSHP=X
        str count_str = ""
        int count
        str symbol

    for symbol in cigar:
        if str.isdigit(symbol):
            count_str += symbol
        else:
            if symbol not in "MIDNSHP=X":
                raise ValueError("Unknown operation {}. Expected one of 'MIDNSHP=X'.".format(symbol))
            if not count_str:
                count = 1
            else:
                count = int(count_str)
            count_str = ""
            result.append((count, symbol))
    return result

cpdef list pysam_cigartuples_from_cigar_str(str cigar):
    cdef:
        list result = []  # MIDNSHP=X
        str count_str = ""
        int count
        str symbol
        dict conversion = {"M": 0, "I": 1, "D": 2, "N": 3, "S": 4, "H": 5, "P": 6, "=": 7, "X": 8}

    for symbol in cigar:
        if str.isdigit(symbol):
            count_str += symbol
        else:
            if symbol not in "MIDNSHP=X":
                raise ValueError("Unknown operation {}. Expected one of 'MIDNSHP=X'.".format(symbol))
            if not count_str:
                count = 1
            else:
                count = int(count_str)
            count_str = ""
            result.append((conversion[symbol], count))
    return result

cpdef str cigar_str_from_pysam_cigartuples(list tuples):
    cdef:
        int count, symbol
        str result, MIDNSHPEX = "MIDNSHP=X"  #["M", "I", "D", "N", "S", "H", "P", "=", "X"]

    result = "".join(["{}{}".format(count if count > 1 else "", MIDNSHPEX[symbol]) for symbol, count in tuples])
    return result

cpdef str get_flag_description(AlignmentRecord al):
    """Returns a human-readable version of an `AlignmentRecord`s flag attribute.

    Arguments:
        al:

    Returns:
        a human-readable version of the `AlignmentRecord` flag attribute.
        A flag value of ``17 == 0x11 == 0x10 | 0x1`` corresponds to *template_having_multiple_segments_in_sequencing* and *reverse_complemented*,
        so the resulting string will equal 'template_having_multiple_segments_in_sequencing, reverse_complemented'.

    """
    cdef list l = []
    cdef Flag flag = al.flag
    cdef str k
    cdef bint v
    for k, v in flag.items():
        if k is 'integer_representation':
            continue
        if v:
            l.append(k)
    return ", ".join(l)
