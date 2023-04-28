import csv
from typing import Generator, Iterable

from bmlsa.datatypes import QuerySequence


def queries_from_csv(
    csv_path: str,
    id_header: str,
    sequence_header: str,
    name_header: str = None,
    desc_header: str = None,
    start_header: str = None,
    end_header: str = None,
) -> Generator[QuerySequence, None, None]:
    """Generates and :obj:`bmlsa.datatypes.QuerySequence` instances from a CSV file.

    :param csv_path: Path to CSV to use
    :type csv_path: str
    :param id_header: The column title for the unique identifier for each query sequence
    :type id_header: str
    :param sequence_header: The column title for the sequences themselves
    :type sequence_header: str
    :param name_header: The column title for the name of the sequence, defaults to None
    :type name_header: str, optional
    :param desc_header: The column title for the description of the sequence,
    defaults to None
    :type desc_header: str, optional
    :param start_header: The column title for the start position of the sequence,
    defaults to None
    :type start_header: str, optional
    :param end_header: The column title for the end position of the sequence,
    defaults to None
    :type end_header: str, optional
    :yield: One :obj:`bmlsa.datatypes.QuerySequence` for each row
    :rtype: A generator that yields objects of :class:`bmlsa.datatypes.QuerySequence`
    """
    with open(csv_path, "r") as csv_fd:
        reader = csv.reader(csv_fd)
        id_ind = None
        sequence_ind = None
        name_ind = None
        desc_ind = None
        start_ind = None
        end_ind = None
        headers_parsed = False
        for row in reader:
            if not headers_parsed:
                id_ind = row.index(id_header)
                sequence_ind = row.index(sequence_header)
                name_ind = row.index(name_header) if name_header else None
                desc_ind = row.index(desc_header) if desc_header else None
                start_ind = row.index(start_header) if start_header else None
                end_ind = row.index(end_header) if end_header else None
                headers_parsed = True
                continue
            id = row[id_ind]
            sequence = row[sequence_ind]
            name = row[name_ind] if name_header else None
            desc = row[desc_ind] if desc_header else None
            start = row[start_ind] if start_header else None
            end = row[end_ind] if end_header else None
            yield QuerySequence(
                id,
                sequence,
                name,
                desc,
                int(start) if start else None,
                int(end) if end else None,
            )


def save_alignments_to_csv(
    aligned_pairs: Iterable[tuple[QuerySequence, QuerySequence]], output_path: str
) -> None:
    """Saves alignments to a CSV.

    :param aligned_pairs: An iterable of the original sequence and aligned sequences
    :type aligned_pairs: Iterable[tuple[AlignedSequence, AlignedSequence]]
    :param output_path: A path to the output directory
    :type output_path: str
    """
    with open(output_path, "w") as output_fd:
        writer = csv.writer(output_fd)
        header_wrote = False
        header_order = None
        for original, aligned in aligned_pairs:
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
