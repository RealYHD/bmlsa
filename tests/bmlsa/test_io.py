from csv import reader
from os import path
from bmlsa.datatypes import QuerySequence
from bmlsa.io import queries_from_csv, save_alignments_to_csv
from collections.abc import Iterable


def test_queries_from_csv_has_data():
    results = queries_from_csv("tests/resources/SARS_CoV-2_genes.csv", "id", "sequence")
    assert isinstance(results, Iterable)


def test_queries_from_csv_data_valid():
    results = queries_from_csv("tests/resources/SARS_CoV-2_genes.csv", "id", "sequence")
    for aligned_seq in results:
        assert isinstance(aligned_seq.id, str)
        assert isinstance(aligned_seq.sequence, str)


def test_save_alignments_to_csv_produces_correct_headers_in_csv(tmpdir):
    output_path = path.join(tmpdir, "alignment_results.csv")
    dummy_sequence = QuerySequence("DUMMY", "ATACTGGAAAA", name="test_sequence")
    alignments = [(dummy_sequence, dummy_sequence)]
    save_alignments_to_csv(alignments, output_path)

    with open(output_path, "r") as csv_fd:
        results = list(reader(csv_fd))
        vars_to_check = list(vars(dummy_sequence).keys())
        for var_to_check in vars_to_check:
            assert "original" + var_to_check in results[0]
            assert "aligned" + var_to_check in results[0]
