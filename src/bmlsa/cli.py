import os
import argparse
from Bio import SeqIO
import logging
from bmlsa.aligner import align_many_to_one_ssw

from bmlsa.io import read_annotations_from_csv, save_alignments_to_csv

logger = logging.getLogger(__name__)

DEFAULT_ALIGNMENT_PARAMETERS = {
    "BLASTp": {
        "extend_gap_score": -1,
        "open_gap_score": -11,
        "substitution_matrix": "BLOSUM62",
        "alignment_mode": "local",
    }
}


def run(args):
    if (
        not (args.extend_gap_score and args.open_gap_score and args.alignment_mode)
        and not args.behave_as
    ):
        logger.error(
            'Must either specify all of "--extend-gap-score", "--open-gap-score", '
            '"--alignment-mode", or, at least "--behave-as". See help (-h) for '
            "more information."
        )
        exit(1)
    queries = read_annotations_from_csv(
        args.annotations,
        args.id_header,
        args.seq_header,
        args.name_header,
        args.desc_header,
        args.start_header,
        args.end_header,
    )

    scoring_parameter = (
        {
            "extend_gap_score": args.extend_gap_score,
            "open_gap_score": args.open_gap_score,
            "alignment_mode": args.alignment_mode,
            "substitution_matrix": args.substitution_matrix
            if args.substitution_matrix is not None
            else "BLOSUM62",
        }
        if args.behave_as not in DEFAULT_ALIGNMENT_PARAMETERS
        else DEFAULT_ALIGNMENT_PARAMETERS[args.behave_as]
    )

    with open(args.sequence, "r") as sequence_fd:
        for sequence in SeqIO.parse(sequence_fd, "fasta"):
            aligned_annotations = align_many_to_one_ssw(
                str(sequence.seq), queries, **scoring_parameter
            )
            save_alignments_to_csv(
                aligned_annotations,
                os.path.join(
                    args.output,
                    sequence.id.replace("|", "+").replace(".", "_") + ".csv",
                ),
            )


def main():
    arg_parser = argparse.ArgumentParser("bmlsa")
    arg_parser.add_argument(
        "annotations",
        type=str,
        help=(
            "Path to CSV containing the sequences to align as well as the "
            "annotations for the respective sequences."
        ),
        metavar="a",
    )
    arg_parser.add_argument(
        "sequence",
        type=str,
        help=(
            "Path to the sequence to use as reference in FASTA format. "
            "If multiple sequences are present in the same FASTA file, "
            "each will be used as a separate reference sequence for separate "
            "runs automatically."
        ),
        metavar="s",
    )
    arg_parser.add_argument(
        "output", type=str, help="Path to output location", metavar="o"
    )
    arg_parser.add_argument(
        "-I",
        "--id-header",
        type=str,
        help="The header of the column for the ID of the sequence to align to "
        "the reference sequence.",
        required=True,
    )
    arg_parser.add_argument(
        "-N",
        "--name-header",
        type=str,
        help="The header of the column for the name of the sequence to align to "
        "the reference sequence.",
        required=False,
    )
    arg_parser.add_argument(
        "-D",
        "--desc-header",
        type=str,
        help="The header of the column for the description of the sequence to "
        "align to the reference sequence.",
        required=False,
    )
    arg_parser.add_argument(
        "-T",
        "--start-header",
        type=str,
        help="The header of the column for the start position of the sequence to "
        "align to the reference sequence.",
        required=False,
    )
    arg_parser.add_argument(
        "-E",
        "--end-header",
        type=str,
        help="The header of the column for end position of the sequence to "
        "align to the reference sequence.",
        required=False,
    )
    arg_parser.add_argument(
        "-S",
        "--seq-header",
        type=str,
        help="The header of the column for the actual sequence to align to the "
        "reference sequence.",
        required=True,
    )
    arg_parser.add_argument(
        "-e",
        "--extend-gap-score",
        type=int,
        help="The scoring for extending a gap.",
        required=False,
        default=None,
    )
    arg_parser.add_argument(
        "-o",
        "--open-gap-score",
        type=int,
        help="The scoring for opening a gap.",
        required=False,
        default=None,
    )
    arg_parser.add_argument(
        "-M",
        "--alignment-mode",
        type=str,
        help="The alignment mode.",
        choices=["local", "global"],
        required=False,
    )
    arg_parser.add_argument(
        "-m",
        "--substitution-matrix",
        type=str,
        help="The name of the substitution matrix.",
        required=False,
        default=None,
    )
    arg_parser.add_argument(
        "-B",
        "--behave-as",
        type=str,
        help="Use built-in parameters for alignment scoring. If this is specified "
        "along either of the scoring arguments, the alignment parameter arguments "
        '("--open-gap-score" and/or "--extend-gab-score" and "--alignment-mode") '
        "will override any defaults set by this argument.",
        required=False,
        default=None,
    )
    args = arg_parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
