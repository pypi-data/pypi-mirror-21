"""This module handles the parsing of name lines.
You can either use an instance of the `NamelineParser` class to handle picking
the correct parsing function for you or choose a specific parsing function yourself:

    1. Let `NamelineParser` do the work for you::

        from dinopy import NamelineParser
        parser = NamelineParser()
        line1 = parser.parse(b"@NS500639:6:H3MYMAFXX:1:11101:9262:1124 1:N:0:TAATGC")  # this is a Casava 1.8+ style nameline
        line2 = parser.parse(b"@NS500639:6:H3MYMAFXX:1:11101:9262:1124 1:N:0:TAATGC")  # this is yet another Casava 1.8+ style nameline
        # line 3 = parser.parse(b"@HWUSI-EAS100R:6:73:941:1973#0/1")  # this is a Casava <1.8 style nameline and parsing this will result in a `ValueError`.

    2. Pick a specific parsing function yourself::

        from dinopy.nameline_parser import parse_casava_18_line, parse_casava_pre18_line, parse_ncbi_line
        line1 = parse_casava_18_line(b"@NS500639:6:H3MYMAFXX:1:11101:9262:1124 1:N:0:TAATGC")  # this is a Casava 1.8+ style nameline
        line2 = parse_casava_18_line(b"@NS500639:6:H3MYMAFXX:1:11101:9262:1124 1:N:0:TAATGC")  # this is yet another Casava 1.8+ style nameline
        # line3 = parse_casava_18_line(b"@HWUSI-EAS100R:6:73:941:1973#0/1")  # this is a Casava <1.8 style nameline and parsing this will result in a `ValueError`
        line4 = parse_casava_pre18_line(b"@HWUSI-EAS100R:6:73:941:1973#0/1")  # this however will work.

    3. Workflow::

        from dinopy import FastqReader, NamelineParser
        nameline_parser = NamelineParser()
        with FastqReader("file.fastq") as fqr:
            for seq, name, _ in fqr.reads():
                nameline = nameline_parser.parse(name)
                print(nameline.tile)
                # do_stuff(nameline)
                # do_other_stuff(seq)

The following nameline-conventions are supported:

    1. Casava < 1.8: ``@instrument:flowcell_lane:tile:cluster_x:cluster_y#index_sequence/pair_member``

    2. Casava ≥ 1.8: ``@unique_instrument_name:run_id:flowecell_id:flowcell_lane:tile:cluster_x:cluster_y pair_member:filtered:control_number:index_sequence``

    3. 454: 14 character string, encoding ``plate|region|xy``

    4. Helicos: ``flowcell-channel-field-camera-position``

    5. IonTorrent: ``run_id chip_row chip_column``

    6. NCBI-SRA: ``SRA-id anyoftheabove length=n``

    7. Unknown formats: will be wrapped in a `_DummyLine` which only holds the line as a ``bytes`` reference, which can either be accessed via ``some_dummy_line.line``, ``some_dummy_line[0]`` or retrieved as a str via ``str(some_dummy_line)``.

"""
cdef class _NameLine:
    pass

cdef class _DummyLine(_NameLine):
    def __cinit__(self, bytes line):
        self.line = line

    def __str__(self):
        return self.line.decode()

    def __getitem__(self, int item):
        if item == 0:
            return self.line
        else:
            raise IndexError()

cdef class _CasavaPre18Line(_NameLine):
    def __cinit__(self, bytes instrument, int flowcell_lane, int tile, int cluster_x, int cluster_y, bytes index_sequence, int pair_member, list additional_info):
        self.instrument = instrument
        self.flowcell_lane = flowcell_lane
        self.tile = tile
        self.cluster_x = cluster_x
        self.cluster_y = cluster_y
        self.index_sequence = index_sequence
        self.pair_member = pair_member
        self.additional_info = additional_info

    def __str__(self):
        return "instrument: {}, flowcell_lane: {}, tile: {}, cluster_x: {}, cluster_y: {}, index_sequence: {}, pair_member: {}, additional_info: {}".format(self.instrument, self.flowcell_lane, self.tile, self.cluster_x, self.cluster_y, self.index_sequence, self.pair_member, self.additional_info)

    def __getitem__(self, int item):
        if item == 0:
            return self.instrument
        elif item == 1:
            return self.flowcell_lane
        elif item == 2:
            return self.tile
        elif item == 3:
            return self.cluster_x
        elif item == 4:
            return self.cluster_y
        elif item == 5:
            return self.index_sequence
        elif item == 6:
            return self.pair_member
        elif item == 7:
            return self.additional_info
        else:
            raise IndexError("No such item {}".format(item))

cdef class _Casava18Line(_NameLine):
    def __cinit__(self, bytes instrument, int run, bytes flowcell_id, int lane, int tile, int cluster_x, int cluster_y, int pair_member, bint filtered, int control_number, bytes index_sequence, list additional_info):
        self.instrument = instrument
        self.run = run
        self.flowcell_id = flowcell_id
        self.lane = lane
        self.tile = tile
        self.cluster_x = cluster_x
        self.cluster_y = cluster_y
        self.pair_member = pair_member
        self.filtered = filtered
        self.control_number = control_number
        self.index_sequence = index_sequence
        self.additional_info = additional_info

    def __str__(self):
        return "instrument: {}, run: {}, flowcell_id: {}, lane: {}, tile: {}, cluster_x: {}, cluster_y: {}, pair_member: {}, filtered: {}, control_number: {}, index_sequence: {}, additional_info: {}".format(self.instrument, self.run, self.flowcell_id, self.lane, self.tile, self.cluster_x, self.cluster_y, self.pair_member, self.filtered, self.control_number, self.index_sequence, self.additional_info)

    def __getitem__(self, int item):
        if item == 0:
            return self.instrument
        elif item == 1:
            return self.run
        elif item == 2:
            return self.flowcell_id
        elif item == 3:
            return self.lane
        elif item == 4:
            return self.tile
        elif item == 5:
            return self.cluster_x
        elif item == 6:
            return self.cluster_y
        elif item == 7:
            return self.pair_member
        elif item == 8:
            return self.filtered
        elif item == 9:
            return self.control_number
        elif item == 10:
            return self.index_sequence
        elif item == 11:
            return self.additional_info
        else:
            raise IndexError("No such item {}".format(item))

cdef _NameLine _parse_casava_18_line(bytes line):
    cdef:
        bytes hardware_info
        bytes instrument, run, flowcell_id, lane, tile, cluster_x, cluster_y
        bytes mate_pair_info
        bytes pair_member, filtered, control_number, index_sequence
        list additional_info
        _Casava18Line name_line

    hardware_info, mate_pair_info, *additional_info = line.split(b" ", maxsplit=2)

    # check if additional info is present, for example generated by RAGE and if so, split it.
    if additional_info:
        additional_info = additional_info[0].split(b", ")

    instrument, run, flowcell_id, lane, tile, cluster_x, cluster_y = hardware_info.split(b":")
    pair_member, filtered, control_number, index_sequence = mate_pair_info.split(b":")
    # Note: The index sequence can also be an integer (index number)

    name_line = _Casava18Line(
        instrument[1:],
        int(run),
        flowcell_id,
        int(lane),
        int(tile),
        int(cluster_x),
        int(cluster_y),
        int(pair_member),
        filtered == b"Y",
        int(control_number),
        index_sequence,
        additional_info,
    )
    return name_line

cdef _NameLine _parse_casava_pre18_line(bytes line):
    cdef:
        bytes hardware_info
        bytes instrument, flowcell_id, lane, tile, cluster_x, cluster_y
        bytes mate_pair_info
        bytes pair_member, filtered, control_number, index
        list additional_info
        _CasavaPre18Line name_line

    hardware_info, *additional_info = line.split(b" ", maxsplit=1)
    hardware_info, mate_pair = hardware_info.split(b"/")
    hardware_info, index = hardware_info.split(b"#")

    # check if additional info is present, for example generated by RAGE and if so, split it.
    if additional_info:
        additional_info = additional_info[0].split(b", ")

    instrument, flowcell_lane, tile, cluster_x, cluster_y = hardware_info.split(b":")

    name_line = _CasavaPre18Line(
        instrument[1:],
        int(flowcell_lane),
        int(tile),
        int(cluster_x),
        int(cluster_y),
        index,
        int(mate_pair),
        additional_info,
    )
    return name_line

cdef class _454Line(_NameLine):
    def __cinit__(self, bytes timestamp, unsigned char hash_value, unsigned char region, unsigned int well_x, unsigned int well_y):
        self.timestamp = timestamp
        self.hash_value = hash_value
        self.region = region
        self.well_x = well_x
        self.well_y = well_y

    def __str__(self):
        return "timestamp: {}, hash_value: {}, region: {}, well_x: {}, well_y: {}".format(self.timestamp, self.hash_value, self.region, self.well_x, self.well_y)

    def __getitem__(self, int item):
        if item == 0:
            return self.timestamp
        elif item == 1:
            return self.hash_value
        elif item == 2:
            return self.region
        elif item == 3:
            return self.well_x
        elif item == 4:
            return self.well_y
        else:
            raise IndexError("No such item {}".format(item))

cdef _NameLine _parse_454_line(bytes line):
    cdef:
        bytes l = line[1:]  # strip leading @
        unsigned int well_xy = int(l[9:14], 36)
    return _454Line(l[:6], int(l[6]), int(l[7:9]), well_xy // 4096, well_xy % 4096)

cdef class _HelicosLine(_NameLine):
    def __cinit__(self, bytes flowcell, unsigned char channel, unsigned int field, unsigned char camera, unsigned int position):
        self.flowcell = flowcell
        self.channel = channel
        self.field = field
        self.camera = camera
        self.position = position

    def __str__(self):
        return "flowcell: {}, channel: {}, field: {}, camera: {}, position: {}".format(self.flowcell, self.channel, self.field, self.camera, self.position)

    def __getitem__(self, int item):
        if item == 0:
            return self.flowcell
        elif item == 1:
            return self.channel
        elif item == 2:
            return self.field
        elif item == 3:
            return self.camera
        elif item == 4:
            return self.position
        else:
            raise IndexError("No such item {}".format(item))

cdef _NameLine _parse_helicos_line(bytes line):
    cdef:
        list parts = line.split(b'-')
    return _HelicosLine(parts[0] + parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))

cdef class _IonTorrentLine(_NameLine):
    def __cinit__(self, bytes run_id, unsigned int chip_row, unsigned int chip_column):
        self.run_id = run_id
        self.chip_row = chip_row
        self.chip_column = chip_column

    def __str__(self):
        return "run_id: {}, chip_row: {}, chip_column: {}".format(self.run_id, self.chip_row, self.chip_column)

    def __getitem__(self, int item):
        if item == 0:
            return self.run_id
        elif item == 1:
            return self.chip_row
        elif item == 2:
            return self.chip_column
        else:
            raise IndexError("No such item {}".format(item))

cdef _NameLine _parse_ion_torrent_line(bytes line):
    cdef:
        list parts = line.split(b' ')
    return _IonTorrentLine(parts[0], int(parts[1]), int(parts[2]))

cdef class _NCBIline(_NameLine):
    def __cinit__(self, bytes ncbi_id, _NameLine name, int length):
        self.ncbi_id = ncbi_id
        self.name = name
        self.length = length

    def __str__(self):
        return "ncbi_id: {}, name: {} ({}), length: {}".format(self.ncbi_id, self.name, type(self.name), self.length)

    def __getitem__(self, int item):
        if item == 0:
            return self.ncbi_id
        elif item == 1:
            return self.name
        elif item == 2:
            return self.length
        else:
            raise IndexError("No such item {}".format(item))

cdef _NameLine _parse_ncbi_line(bytes line):
    cdef:
        list parts = line.split(b' ')
        int num_parts = len(parts), length
        bytes ncbi_id
        _NameLine casava
    if num_parts == 3:
        ncbi_id = parts[0]
        name = NamelineParser._pick_parser(parts[1])(parts[1])
        length = int(parts[2][7:])
        return _NCBILine(ncbi_id, name, length)
    else:
        return _DummyLine(line)

cdef _NameLine _parse_dummy_line(bytes line):
    return _DummyLine(line)

# Exporting python functions without leading underscore; also necessary because cpdef functions cannot be typed using parser_function-type
cpdef _NameLine parse_casava_18_line(bytes line):
    """Split a Casava 1.8+ Style illumina fastq header.
    `Documentation p. 50 <http://support.illumina.com/content/dam/illumina-support/documents/myillumina/feb3d85a-6c63-467d-aa86-18abd5e880f3/casava_ug_15011196b.pdf>`_.

    Arguments:
        line (bytes): A casava style header line.

    Returns:
        Nameline: Containing all information of the casava line. These are:

            - instrument (bytes)
            - run (int)
            - flowcell_id (int)
            - lane (int)
            - tile (int)
            - cluster_x (int)
            - cluster_y (int)
            - pair_member (int)
            - filtered (bool)
            - control_nr (int)
            - index_sequence (bytes)
            - additional information after the casava line (empty most of the time) (list)
    """
    return _parse_casava_18_line(line)

cpdef _NameLine parse_casava_pre18_line(bytes line):
    """Split a Casava <1.8 Style illumina fastq header.
    `Documentation p. 50 <http://support.illumina.com/content/dam/illumina-support/documents/myillumina/feb3d85a-6c63-467d-aa86-18abd5e880f3/casava_ug_15011196b.pdf>`_.

    Arguments:
        line (bytes): A casava style header line.

    Returns:
        Nameline: Containing all information of the casava line. These are:

            - instrument (bytes)
            - flowcell lane (int)
            - tile (int)
            - cluster_x (int)
            - cluster_y (int)
            - index_sequence (bytes)
            - pair_member (int)
            - additional information after the casava line (empty most of the time) (list)
    """
    return _parse_casava_pre18_line(line)

cpdef _NameLine parse_ncbi_line(bytes line):
    return _parse_ncbi_line(line)

cdef class NamelineParser:
    """Used for automagically parsing either of Casava 1.8+-, Casava <1.8- or NCBI-style namelines.


    Examples:

        1. Parse Casava <1.8 style namelines::

            from dinopy import NamelineParser
            parser = NamelineParser()
            line = parser.parse(b"@HWUSI-EAS100R:6:73:941:1973#0/1")
            print(line)  # "instrument: b'HWUSI-EAS100R', flowcell_lane: 6, tile: 73, cluster_x: 941, cluster_y: 1973, index_sequence: b'TODO', pair_member: -1, additional_info: []"
            print(line.tile)  # 73

        2. Parse Casava 1.8+ style namelines::

            from dinopy import NamelineParser
            parser = NamelineParser()
            line = parser.parse(b"@NS500639:6:H3MYMAFXX:1:11101:9262:1124 1:N:0:TAATGC")
            print(line)  # "instrument: b'NS500639', run: 6, flowcell_id: b'H3MYMAFXX', lane: 1, tile: 11101, cluster_x: 9262, cluster_y: 1124, pair_member: 1, filtered: False, control_number: 0, index_sequence: b'TAATGC', additional_info: []"
            print(line.instrument)  # b'NS500639'

        3. Parse NCBI style namelines (defunct)::

            from dinopy import NamelineParser
            parser = NamelineParser()
            line = parser.parse(b"@SRR001666.1 071112_SLXA-EAS1_s_7:5:1:817:345 length=36")
            print(line)  # TODO

        4. Unknown nameline styles::

            from dinopy import NamelineParser
            parser = NamelineParser()
            line = parser.parse(b"@Something:Entirely Different")
            print(line)  # "@Something:Entirely Different"

    """
    def __init__(self):
        # nothing interesting
        self._first_call = True
        self._parse = _parse_dummy_line

    @staticmethod
    cdef parse_function _pick_parser(bytes line):
        cdef:
            list parts = line.split(b' ')  # split by ' '
        if len(parts) == 1 and len(line[1:]) == 14:  # 454
            return _parse_454_line
        elif len(parts) == 1 and line.count(b'-') == 5:  # helicos
            return _parse_helicos_line
        elif len(parts) == 1 and line.count(b':') == 4 and line.rindex(b':') < line.find(b'#') < line.find(b'/'):  # Casava Pre 1.8
            return _parse_casava_pre18_line
        elif len(parts) == 2 and line.count(b':') == 9:  # Casava
            return _parse_casava_18_line
        elif len(parts) == 3 and parts[2].startswith(b'length='):  # NCBI
            return _parse_ncbi_line
        elif len(parts) == 3:  # IonTorrent
            return _parse_ion_torrent_line
        else:
            return _parse_dummy_line

    cpdef _NameLine parse(self, bytes line):
        if self._first_call:
            self._parse = NamelineParser._pick_parser(line)
            self._first_call = False
        return self._parse(line)
