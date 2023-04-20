from skbio.alignment import StripedSmithWaterman

from datatypes import Annotation


def generate_annotated_positions(sequence: str, annotations: dict[str, Annotation]):
    annotation_pairs = {}
    align = StripedSmithWaterman(sequence)
    for id, annot in annotations.items():
        alignment = align(annot.sequence)
        score, aligned_start, aligned_end = (
            alignment.optimal_alignment_score,
            alignment.query_begin,
            alignment.query_end,
        )
        annotation_pairs[id] = Annotation(
            id,
            annot.sequence,
            annot.name,
            annot.description,
            annot.start,
            annot.end,
            annot.score,
        ), Annotation(
            id,
            alignment.aligned_target_sequence,
            annot.name,
            annot.description,
            aligned_start,
            aligned_end,
            score,
        )
    return annotation_pairs
