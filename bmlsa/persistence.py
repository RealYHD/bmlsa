import csv

from bmlsa.datatypes import AlignedSequence


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
            annotations[id] = AlignedSequence(
                id,
                sequence,
                name,
                desc,
                int(start) if start else None,
                int(end) if end else None,
            )
    return annotations


def save_alignments_to_csv(
    aligned_pairs: dict[str, tuple[AlignedSequence, AlignedSequence]], output_path: str
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
