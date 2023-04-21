from Bio.Align import PairwiseAligner, substitution_matrices
from bmlsa.datatypes import AlignedSequence
from bmlsa.exceptions import UnexpectedAlignmentResult


def protein_align_many_to_one_ssw(sequence: str, queries: dict[str, AlignedSequence]):
    annotation_pairs = {}
    aligner = PairwiseAligner()
    aligner.mode = "local"
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.extend_gap_score = -1
    aligner.open_gap_score = -11
    for id, query in queries.items():
        try:
            alignments = aligner.align(sequence, query.sequence)
        except ValueError:
            continue
        if len(alignments) > 1:
            raise UnexpectedAlignmentResult(
                "More than one alignment resulted from a single query."
            )
        for alignment in alignments:
            score, query_aligned = (alignment.score, alignment.aligned[0][0])
            aligned_start, aligned_end = query_aligned
            annotation_pairs[id] = AlignedSequence(
                id,
                query.sequence,
                query.name,
                query.description,
                query.start,
                query.end,
                query.score,
            ), AlignedSequence(
                id,
                alignment.query,
                query.name,
                query.description,
                aligned_start,
                aligned_end,
                score,
            )
    return annotation_pairs
