import os
import argparse
from Bio import SeqIO
from bmlsa.aligner import protein_align_many_to_one_ssw

from bmlsa.persistence import read_annotations_from_csv, save_alignments_to_csv


def main():
    argparser = argparse.ArgumentParser("blmsa")
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
            aligned_annotations = protein_align_many_to_one_ssw(
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
