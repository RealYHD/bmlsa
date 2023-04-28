import logging
from typing import Iterable
from Bio.Align import PairwiseAligner, substitution_matrices
from bmlsa.datatypes import AlignedSequence
from bmlsa.exceptions import UnexpectedAlignmentResult

logger = logging.getLogger(__name__)


def align_many_to_one_ssw(
    reference_sequence: str,
    queries: Iterable[AlignedSequence],
    extend_gap_score: int,
    open_gap_score: int,
    alignment_mode: str,
    substitution_matrix: str = "BLOSUM62",
):
    # TODO Consider using the built in "scoring" parameter
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load(substitution_matrix)
    aligner.extend_gap_score = extend_gap_score
    aligner.open_gap_score = open_gap_score
    aligner.mode = alignment_mode
    for query in queries:
        try:
            alignments = aligner.align(reference_sequence, query.sequence)
        except ValueError:
            logger.warning(
                'Skipping sequence with id "%s" due to invalid characters', query.id
            )
            continue
        # TODO Implement comparison with input positions to choose best
        if len(alignments) > 1:
            raise UnexpectedAlignmentResult(
                "More than one alignment resulted from a single query."
            )
        for alignment in alignments:
            score, query_aligned = (alignment.score, alignment.aligned[0][0])
            aligned_start, aligned_end = query_aligned
            yield AlignedSequence(
                query.id,
                query.sequence,
                query.name,
                query.description,
                query.start,
                query.end,
                query.score,
            ), AlignedSequence(
                query.id,
                alignment.query,
                query.name,
                query.description,
                int(aligned_start) + 1,
                aligned_end,
                score,
            )
