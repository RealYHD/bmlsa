import pytest
from Bio import SeqIO
from bmlsa.aligner import align_many_to_one_ssw
from bmlsa.cli import DEFAULT_ALIGNMENT_PARAMETERS
from bmlsa.datatypes import AlignedSequence
from collections.abc import Iterable


@pytest.fixture
def reference_sequence():
    return str(
        list(SeqIO.parse("tests/resources/NC_045512_coding.fasta", "fasta"))[0].seq
    )


@pytest.fixture
def queries():
    return [
        AlignedSequence(
            "ORF10",
            "ATGGGCTATATAAACGTTTTCGCTTTTCCGTTTACGATATATAGTCTACTCTTGTGCAGAAT"
            "GAATTCTCGTAACTACATAGCACAAGTAGATGTAGTTAACTTTAATCTCACATAG",
            start=29558,
            end=29674,
        )
    ]


def test_align_many_to_one_returns_data(reference_sequence, queries):
    results = align_many_to_one_ssw(
        reference_sequence, queries, **DEFAULT_ALIGNMENT_PARAMETERS["BLASTp"]
    )
    assert isinstance(results, Iterable)


def test_align_many_to_one_returns_correct_data_structure(reference_sequence, queries):
    results = align_many_to_one_ssw(
        reference_sequence, queries, **DEFAULT_ALIGNMENT_PARAMETERS["BLASTp"]
    )
    for original, aligned_seq in results:
        assert isinstance(original, AlignedSequence)
        assert isinstance(aligned_seq, AlignedSequence)


def test_align_many_to_one_returns_correct_data(reference_sequence, queries):
    results = align_many_to_one_ssw(
        reference_sequence, queries, **DEFAULT_ALIGNMENT_PARAMETERS["BLASTp"]
    )
    for original, aligned_seq in results:
        assert original.start == aligned_seq.start
        assert original.end == aligned_seq.end
