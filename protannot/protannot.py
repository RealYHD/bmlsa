import csv
import os
from skbio.alignment import StripedSmithWaterman
import argparse
from Bio import SeqIO

from Datatypes import Annotation


def read_annotations_from_csv(
    csv_path: str,
    id_header: str,
    name_header: str,
    desc_header: str,
    start_header: str,
    end_header: str,
    sequence_header: str,
):
    annotations = {}
    with open(csv_path, "r") as csv_fd:
        reader = csv.reader(csv_fd)
        id_ind = None
        name_ind = None
        desc_ind = None
        start_ind = None
        end_ind = None
        sequence_ind = None
        headers_parsed = False
        for row in reader:
            if not headers_parsed:
                id_ind = row.index(id_header)
                name_ind = row.index(name_header) if name_header else None
                desc_ind = row.index(desc_header) if desc_header else None
                start_ind = row.index(start_header) if start_header else None
                end_ind = row.index(end_header) if end_header else None
                sequence_ind = row.index(sequence_header)
                headers_parsed = True
                continue
            id = row[id_ind]
            name = row[name_ind] if name_header else None
            desc = row[desc_ind] if desc_header else None
            start = row[start_ind] if start_header else None
            end = row[end_ind] if end_header else None
            sequence = row[sequence_ind]
            annotations[id] = Annotation(
                id,
                sequence,
                name,
                desc,
                int(start) if start else None,
                int(end) if end else None,
            )
    return annotations


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


def save_alignments_to_csv(
    aligned_pairs: dict[str, tuple[Annotation, Annotation]], output_path: str
):
    with open(output_path, "w") as output_fd:
        writer = csv.writer(output_fd)
        header_wrote = False
        header_order = None
        for id, annotations in aligned_pairs.items():
            original, aligned = annotations
            original_vars = vars(original)
            aligned_vars = vars(aligned)
            if not header_wrote:
                header_order = list(original_vars.keys())
                header = ["original" + key for key in header_order]
                header.extend(["aligned" + key for key in header_order])
                writer.writerow(header)
                header_wrote = True
            row_data = [original_vars[header] for header in header_order]
            row_data.extend([aligned_vars[header] for header in header_order])
            writer.writerow(row_data)


def main():
    argparser = argparse.ArgumentParser("protannot")
    argparser.add_argument(
        "annotations",
        type=str,
        help=(
            "Path to CSV containing the sequences to align as well as the "
            "annotations for the respective sequences"
        ),
        metavar="a",
    )
    argparser.add_argument(
        "sequence",
        type=str,
        help=(
            "Path to the sequence to annotate in FASTA format. "
            "If multiple sequences are present, annotations will be run on each"
        ),
        metavar="s",
    )
    argparser.add_argument(
        "output", type=str, help="Path to output location", metavar="o"
    )
    argparser.add_argument(
        "-I", "--id-header", type=str, help="The header for the ID of the annotation"
    )
    argparser.add_argument(
        "-N",
        "--name-header",
        type=str,
        help="The header for the name of the annotation",
        required=False,
    )
    argparser.add_argument(
        "-D",
        "--desc-header",
        type=str,
        help="The header for the description of the annotation",
        required=False,
    )
    argparser.add_argument(
        "-T",
        "--start-header",
        type=str,
        help="The header for the start of the annotation",
        required=False,
    )
    argparser.add_argument(
        "-E",
        "--end-header",
        type=str,
        help="The header for the end of the annotation",
        required=False,
    )
    argparser.add_argument(
        "-S",
        "--seq-header",
        type=str,
        help="The header for the sequence of the annotation",
    )
    args = argparser.parse_args()
    given_annotations = read_annotations_from_csv(
        args.annotations,
        args.id_header,
        args.name_header,
        args.desc_header,
        args.start_header,
        args.end_header,
        args.seq_header,
    )
    with open(args.sequence, "r") as sequence_fd:
        for sequence in SeqIO.parse(sequence_fd, "fasta"):
            aligned_annotations = generate_annotated_positions(
                str(sequence.seq), given_annotations
            )
            save_alignments_to_csv(
                aligned_annotations,
                os.path.join(
                    args.output,
                    sequence.id.replace("|", "+").replace(".", "_") + ".csv",
                ),
            )


if __name__ == "__main__":
    main()
