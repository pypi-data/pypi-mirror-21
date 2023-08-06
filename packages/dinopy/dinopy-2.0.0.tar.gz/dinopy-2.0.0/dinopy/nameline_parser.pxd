cdef class _NameLine:
    pass

cdef class _Casava18Line(_NameLine):
    cdef readonly:
        bytes instrument, flowcell_id, index_sequence,
        int run, lane, control_number, tile, cluster_x, cluster_y, pair_member,
        bint filtered
        list additional_info

cdef class _CasavaPre18Line(_NameLine):
    cdef readonly:
        bytes instrument, index_sequence
        int flowcell_lane, tile, cluster_x, cluster_y, pair_member,
        list additional_info

cdef class _454Line(_NameLine):
    cdef readonly:
        bytes timestamp
        unsigned char hash_value, region
        unsigned int well_x, well_y

cdef class _HelicosLine(_NameLine):
    cdef readonly:
        bytes flowcell
        unsigned char channel
        unsigned int field
        unsigned char camera
        unsigned int position

cdef class _IonTorrentLine(_NameLine):
    cdef readonly:
        bytes run_id
        unsigned int chip_row, chip_column

cdef class _DummyLine(_NameLine):
    cdef readonly bytes line

cdef class _NCBILine(_NameLine):
    cdef readonly:
        bytes ncbi_id
        int length
        _NameLine name

ctypedef _NameLine (*parse_function)(bytes)

cdef _NameLine _parse_casava_18_line(bytes line)
cdef _NameLine _parse_casava_pre18_line(bytes line)
cdef _NameLine _parse_ncbi_line(bytes line)
cdef _NameLine _parse_dummy_line(bytes line)

cpdef _NameLine parse_casava_18_line(bytes line)
cpdef _NameLine parse_casava_pre18_line(bytes line)
cpdef _NameLine parse_ncbi_line(bytes line)

cdef class NamelineParser:  # class that actually picks a parser and delegates the parsing
    cdef bint _first_call
    cdef parse_function _parse

    @staticmethod
    cdef parse_function _pick_parser(bytes line)
    cpdef _NameLine parse(self, bytes line)
