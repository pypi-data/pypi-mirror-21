# -*- coding: utf-8 -*-
"""From the `SAM format specification <https://samtools.github.io/hts-specs/SAMv1.pdf>`_:

    SAM stands for Sequence Alignment/Map format. It is a TAB-delimited text format consisting of a header
    section, which is optional, and an alignment section. If present, the header must be prior to the alignments.
    Header lines start with ‘@’, while alignment lines do not. Each alignment line has 11 mandatory fields for
    essential alignment information such as mapping position, and variable number of optional fields for flexible
    or aligner specific information.

"""
cimport numpy as np
import numpy as np

try:
    from binascii import unhexlify
except ImportError:
    def unhexlify(ovalue):
        """Fallback function if binascii is not installed.
        
        Arguments:
            ovalue(bytes): Hex string of an optional entry of a sam/bam file.
        """
        # matches '[0-9A-F]+'
        num_values = len(ovalue) // 2
        arr = bytearray(num_values)
        for i in range(num_values):
            arr[i] = int(ovalue[i:i + 2], 16)

from .sambam cimport _split_flag

cdef dict _parse_any_header_line(str line):
    """Parses any SAM header line of the format '@XY\tk1:v1\tk2:v2\t...\tkn:vn'.

    Arguments:
        line: a SAM header line starting with a 2 character tag prefixed by '@', e.g. '@XY\tk1:v1\tk2:v2\t...\tkn:vn'

    Returns:
        a dictionary with all keys and values of type `str`, i.e. '@XY\tk1:v1\tk2:v2\t...\tkn:vn' → `{'k1': 'v1', 'k2': 'v2', ..., 'kn': 'vn'}`.
    """
    # The @HD line should be present, with either the SO tag or the GO tag (but not both) specified.
    cdef:
        list parts
        dict result

    if line[:3] == "@CO":  # One-line text comment. Unordered multiple @CO lines are allowed.
        return line[3:].strip()

    parts = line[3:].strip().split('\t')  # Everything else looks like "k1:v1\tk2:v2\t...\kn:vn"

    result = {}  # for now, just return a dict
    for part in parts:
        tag, value = part.split(":")
        result[tag] = value
    return result

cdef tuple _parse_header_line(str line):
    """Similar to `_parse_any_header_line` but combines the 2 character tag with leading '@' with the results of `_parse_any_header_line(line)`
    into a tuple `(tag, _parse_any_header_line(line))`.

    Arguments:
        line: a SAM header line starting with a 2 character tag prefixed by '@', e.g. '@XY\tk1:v1\tk2:v2\t...\tkn:vn'

    Returns: `(tag, _parse_any_header_line(line))`.

    """
    cdef str tag = line[:3]
    return tag, _parse_any_header_line(line)

cdef AlignmentRecord parse_alignment_record(str line):
    cdef:
        list parts = line.strip().split("\t"), optional_parts = []
        AlignmentRecord result = AlignmentRecord()
        int num_fields = 11, flag, num_values, i
        str otag, otype, ovalue, type_char
        dict value_type

    if len(parts) > num_fields:
        optional_parts = parts[num_fields:]
        parts = parts[:num_fields]

    if len(parts) != num_fields:
        raise ValueError("Expected exactly {} columns, got {}".format(num_fields, len(parts)))

    # explicitly assign attributes
    result.query_name = parts[0]
    result.flag.integer_representation = int(parts[1])
    result.rname = parts[2]
    result.pos = int(parts[3]) - 1  # SAM files are 1 based, BAM files 0 based; we store 0 based positions internally
    result.mapping_quality = int(parts[4])
    result.cigar = parts[5]
    result.rnext = parts[6]
    result.pnext = int(parts[7]) - 1  # see above
    result.template_length = int(parts[8])
    result.query_sequence = parts[9]
    result.qual = parts[10]

    # interpret flag
    _split_flag(result)

    result.optional = {}
    for opt_part in optional_parts:
        otag, otype, ovalue = opt_part.split(':')

        def opt_parse(str ovalue, str otype):
            # TODO proper parsing
            if otype == 'A':  # Printable character
                # matches '[!-~]'.
                return ovalue
            elif otype == 'i':  # Signed integer
                # matches '[-+]?[0-9]+'
                return int(ovalue)
            elif otype == 'f':  # Single-precision floating number
                # matches '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                return float(ovalue)
            elif otype == 'Z':  # Printable string, including spaces
                # matches '[ !-~]+'
                return ovalue
            elif otype == 'H':  # Byte array in the Hex format
                # matches '[0-9A-F]+'
                # num_values = len(ovalue) // 2
                # arr = bytearray(num_values)
                # for i in range(num_values):
                #     arr[i] = int(ovalue[i:i + 2], 16)
                return unhexlify(ovalue)
            elif otype == 'B':  # Integer or numeric array
                # matches '[cCsSiIf](,[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)+'
                # c: int8_t
                # C: uint8_t
                # s: int16_t
                # S: uint16_t
                # i: int32_t
                # I: uint32_t
                # f: float
                num_values = ovalue.count(',') + 1
                value_type = {'c': np.int8, 'C': np.uint8, 's': np.int16, 'S': np.uint16, 'i': np.int32, 'I': np.uint32, 'f': np.float}
                type_char = ovalue[0]
                arr = np.empty(num_values, dtype=value_type[type_char])  # TODO: numpy.ndarray or python list?
                if num_values > 1:
                    str_values = ovalue[1:].split(',')
                else:
                    str_values = ovalue[1:]

                if type_char == 'f':
                    for i, str_value in enumerate(str_values):
                        arr[i] = float(str_value)
                elif type_char in {'c', 'C', 's', 'S', 'i', 'I'}:
                    for i, str_value in enumerate(str_values):
                        arr[i] = int(str_value)
                else:
                    raise ValueError("Unknown type '{}' in {}.".format(type_char, ovalue))
                return arr

            return ovalue
        result.optional[otag] = opt_parse(ovalue, otype)
    result.optional_raw = "\t".join(optional_parts)

    return result

cdef class SamReader:
    """Class for reading SAM files.

    Examples:
        1. Open SAM file and print all records::

            from dinopy import SamReader
            sr = SamReader(filepath)
            for ar in sr.get_alignment_records():
                print(ar.get_sam_repr())

        2. Read and print SAM header::

            from dinopy import SamReader
            sr = SamReader(filepath)
            print(sr.get_header())

    .. note: Does not yet parse all known optional column-types properly.
    """

    def __init__(self, filepath):
        self._samfile = filepath

    cpdef list get_header(self):
        """Reads and returns the SAM-file's header.

        Returns:  a list of header entries.
        """
        cdef list header = []
        cdef bytes line
        cdef str str_line
        with InputOpener(self._samfile) as f:
            for line in f:
                str_line = line.decode('utf-8')
                if str_line.startswith("@"):
                    header.append(_parse_header_line(str_line))
                else:
                    break
        return header

    def records(self):
        """Reads and parses the SAM alignment records from the file iteratively.

        Yields:
            `AlignmentRecord`
        """
        cdef bytes line
        cdef str str_line
        with InputOpener(self._samfile) as f:
            for line in f:
                str_line = line.decode('utf-8')
                if str_line.startswith("@"):
                    continue
                yield parse_alignment_record(str_line)
