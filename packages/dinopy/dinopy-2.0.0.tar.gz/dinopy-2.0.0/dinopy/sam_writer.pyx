# -*- coding: utf-8 -*-
from collections import OrderedDict

from .sambam cimport AlignmentRecord
from .output_opener cimport OutputOpener

cdef class SamWriter(OutputOpener):
    """Class for writing `AlignmentRecord` to a SAM-file.

     Examples:

        Writing records from a list::

            from dinopy.sambam import AlignmentRecord
            from dinopy import SamWriter
            records = [AlignmentRecord.fromvalues('r003', 0, 'ref', 9, 30, '5S6M', '*', 0, 0, 'GCCTAAGCTAA', '*', {'SA': 'ref,29,-,6H5M,17,0;'}),
                       AlignmentRecord.fromvalues('r004', 0, 'ref', 16, 30, '6M14N5M', '*', 0, 0, 'ATAGCTTCAGC', '*', None) ]
            with dinopy.SamWriter("somefile.sam") as saw:
                saw.write_records(records)

        Writing a SAM file header generated from reference names and lengths (similar to pysam)::

            from dinopy import SamWriter
            with dinopy.SamWriter("somefile.sam") as saw:
                saw.write_sq_header(reference_names, reference_lengths)

        Writing a custom SAM file header:

            from dinopy import SamWriter
            lines = [('HD', {'VN': 1.5, 'SO': 'coordinate'}), ('@SQ', {'SN': 'ref', 'LN': 45})]
            with dinopy.SamWriter("somefile.sam") as saw:
                saw.write_header([('HD', {'VN': 1.5, 'SO': 'coordinate'}),
                                  ('SQ', {'SN': 'ref1', 'LN': 45}),
                                  ('SQ', {'SN': 'ref2', 'LN': 42})
                                 ]
                                )
            

    """
    def __init__(self, fp, append=False, force_overwrite=False):
        # set desired write mode and save append / overwrite policy
        super().__init__(fp, 't' + ('a' if append else ('f' if force_overwrite else '')))

    cpdef void write_header_line(self, str tag, dict items):
        """Writes a single header line to the SAM file. Does not perform any validation.

        Arguments:
            tag (str): the two character tag, with or without leading '@'.
            items (dict): a dictionary containing the actual information. For example, for a tag of '@HD', items could be ``{'VN': 1.5, 'SO': 'coordinate'}``.

        Examples:

            1. Write a single header line::

                from dinopy import SamWriter
                with dinopy.SamWriter("somefile.sam") as saw:
                    saw.write_header_line('HD', {'VN': 1.5, 'SO': 'coordinate'})

            2. Write a single header line using tuple unpacking::

                from dinopy import SamWriter
                with dinopy.SamWriter("somefile.sam") as saw:
                    saw.write_header_line(*('@SQ', {'SN': 'ref', 'LN': 45}))
        """
        if self.is_open():
            self.writer.write('{}{}\t{}\n'.format('@' if not tag.startswith('@') else '', tag, '\t'.join(['{}:{}'.format(k, v) for k, v in items.items()])))  # oh well
        else:
            raise IOError("Cannot write to {}. Writer has not been opened. Forgot to use with-environment?".format(self.sink))

    cpdef list create_header_sq_lines(self, list reference_names, list reference_lengths):
        """

        Args:
            reference_names: A list of reference names
            reference_lengths:  A list of reference lengths

        Returns:
            a list of ``('SQ', {'SN': refname, 'LN': reflen})`` tuples to be used in conjunction with `write_header`
        """
        return [('SQ', OrderedDict([('SN', refname), ('LN', reflen)])) for refname, reflen in zip(reference_names, reference_lengths)]

    cpdef void write_sq_header(self, list reference_names, list reference_lengths):
        """ Same as ``write_header(create_header_sq_lines(reference_names, reference_lengths))``.
        
        Args:
            reference_names: A list of reference names
            reference_lengths:  A list of reference lengths 
        """
        self.write_header(self.create_header_sq_lines(reference_names, reference_lengths))

    cpdef void write_header(self, list lines):
        """Writes the given header lines to the SAM file. Does not perform any validation.

        Arguments:
            lines (list): a list of ``(str, dict)`` tuples

        Examples:

            1. Write some header lines::

                from dinopy import SamWriter
                lines = [('HD', {'VN': 1.5, 'SO': 'coordinate'}), ('@SQ', {'SN': 'ref', 'LN': 45})]
                with dinopy.SamWriter("somefile.sam") as saw:
                    saw.write_header(lines)
        """
        if self.is_open():
            for line in lines:
                tag, items = line
                self.writer.write('{}{}\t{}\n'.format('@' if not tag.startswith('@') else '', tag, '\t'.join(['{}:{}'.format(k, v) for k, v in items.items()])))
        else:
            raise IOError("Cannot write to {}. Writer has not been opened. Forgot to use with-environment?".format(self.sink))

    cpdef void write_record(self, AlignmentRecord ar):
        """Writes a single `AlignmentRecord` to the output sink.

        Arguments:
            ar (AlignmentRecord): `AlignmentRecord` that is to be written to the output.

        Examples:

            1. Write a single record::

                from dinopy import SamWriter
                ar = AlignmentRecord.fromstr("r003	2064	ref	29	17	6H5M	*	0	0	TAGGC	*	SA:Z:ref,9,+,5S6M,30,1;")
                with dinopy.SamWriter("somefile.sam") as saw:
                    saw.write_record(ar)
        """
        if self.is_open():
            self.writer.write(ar.get_sam_repr())
            self.writer.write('\n')
        else:
            raise IOError("Cannot write to {}. Writer has not been opened. Forgot to use with-environment?".format(self.sink))

    cpdef void write_records(self, c):
        """Writes a collection of `AlignmentRecord` to the output sink.

        Arguments:
            c: a collection or iterable of `AlignmentRecord`.

        Examples:

            1. Write some records::

                from dinopy import SamWriter
                records = [AlignmentRecord.fromvalues('r004', 0, 'ref', 16, 30, '6M14N5M', '*', 0, 0, 'ATAGCTTCAGC', '*', None),
                           AlignmentRecord.fromstr("r003	2064	ref	29	17	6H5M	*	0	0	TAGGC	*	SA:Z:ref,9,+,5S6M,30,1;"),
                           AlignmentRecord.fromstr("r001	147	ref	37	30	9M	=	7	-39	CAGCGGCAT	*	NM:i:1"), ]
                with dinopy.SamWriter("somefile.sam") as saw:
                    saw.write_records(records)
        """
        cdef AlignmentRecord ar
        if self.is_open():
            for ar in c:
                self.writer.write(ar.get_sam_repr())
                self.writer.write('\n')
        else:
            raise IOError("Cannot write to {}. Writer has not been opened. Forgot to use with-environment?".format(self.target))

    cpdef __enter__(self):
        OutputOpener.__enter__(self)
        return self

    cpdef close(self):
        """Close the file (after writing).

        Note:
            This should only be used if the exact number of files is not known
            at development time. Otherwise the use of the environment is
            encouraged, as it is much harder to 'forget' closing an opened file.
        """
        OutputOpener.close(self)
