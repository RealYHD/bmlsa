import logging
from typing import Generator, Iterable
from Bio.Align import PairwiseAligner, substitution_matrices
from bmlsa.datatypes import QuerySequence

logger = logging.getLogger(__name__)


def align_many_to_one_ssw(
    reference_sequence: str,
    queries: Iterable[QuerySequence],
    extend_gap_score: int,
    open_gap_score: int,
    alignment_mode: str,
    substitution_matrix: str = "BLOSUM62",
) -> Generator[tuple[QuerySequence, QuerySequence], None, None]:
    """Aligns :obj:`bmlsa.datatypes.QuerySequence` objects to a given reference sequence

    :param reference_sequence: The reference sequence to align to
    :type reference_sequence: str
    :param queries: A iterable sequence of :obj:`bmlsa.datatypes.QuerySequence`
    :type queries: Iterable[QuerySequence]
    :param extend_gap_score: The gap score to use for alignment. Typically negative.
    :type extend_gap_score: int
    :param open_gap_score: The open gap score to use for alignment. Typically negative.
    :type open_gap_score: int
    :param alignment_mode: The alignment mode to use. Either "local" or "global".
    :type alignment_mode: str
    :param substitution_matrix: The name of the substitution matrix available
        in :mod:`Bio.Align`, defaults to "BLOSUM62"
    :type substitution_matrix: str, optional
    :yield: Pairs of :obj:`bmlsa.datatypes.QuerySequence` objects where the first is
        the original, and the second is the aligned version
    :rtype: a generator of :obj:`bmlsa.datatypes.QuerySequence` objects
    """
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
        for alignment in alignments:
            score, query_aligned = (alignment.score, alignment.aligned[0][0])
            aligned_start, aligned_end = query_aligned
            yield QuerySequence(
                query.id,
                query.sequence,
                query.name,
                query.description,
                query.start,
                query.end,
                query.score,
            ), QuerySequence(
                query.id,
                alignment.query,
                query.name,
                query.description,
                int(aligned_start) + 1,
                aligned_end,
                score,
            )
