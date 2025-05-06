import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, Iterator, Set, TextIO


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert Pocket CSV export to Netscape Bookmark HTML format."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the input Pocket CSV file (e.g., part_000000.csv).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("bookmarks.html"),
        help="Path to the output Netscape Bookmark HTML file.",
    )
    args: argparse.Namespace = parser.parse_args()

    input_file: Path = args.input_file
    output_file: Path = args.output

    if not input_file.is_file():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    html_header: str = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!--This is an automatically generated file.
It will be read and overwritten.
Do Not Edit! -->
<META HTTP-EQUIV="Content-Type" Content="text/html; charset=UTF-8">
<Title>Bookmarks</Title>
<H1>Bookmarks</H1>
<DL><p>
"""
    html_footer: str = "</DL><p>\n"
    item_template: str = (
        '    <DT><A HREF="{url}" ADD_DATE="{date}" LAST_VISIT="{date}" LAST_MODIFIED="{date}">{title}</A>'
    )

    try:
        with (
            open(input_file, "r", encoding="utf-8") as infile,
            open(output_file, "w", encoding="utf-8") as outfile,
        ):
            # Explicitly type file handles
            infile_typed: TextIO = infile
            outfile_typed: TextIO = outfile

            outfile_typed.write(html_header)

            reader: csv.DictReader = csv.DictReader(infile_typed)
            required_columns: Set[str] = {"title", "url", "time_added"}
            # Ensure reader.fieldnames is treated correctly when it might be None
            fieldnames: Set[str] = (
                set(reader.fieldnames) if reader.fieldnames else set()
            )
            if not required_columns.issubset(fieldnames):
                missing: Set[str] = required_columns - fieldnames
                print(
                    f"Error: Input CSV missing required columns: {', '.join(missing)}",
                    file=sys.stderr,
                )
                sys.exit(1)

            # Type the iterator from DictReader
            row_iterator: Iterator[Dict[str, str]] = reader
            for row in row_iterator:
                url: str = row.get("url", "").strip()
                if not url:
                    # Skip rows without a URL
                    continue

                title: str = row.get("title", "").strip()
                if not title:
                    # Use URL as title if title is missing
                    title = url

                # Escape HTML special characters in title
                title = (
                    title.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                )

                time_added_str: str = row.get("time_added", "0").strip()
                date_added: int
                try:
                    # Pocket export uses Unix timestamp (seconds since epoch)
                    date_added = int(time_added_str) if time_added_str else 0
                except ValueError:
                    print(
                        f"Warning: Invalid time_added value '{time_added_str}' for URL {url}. Using 0.",
                        file=sys.stderr,
                    )
                    date_added = 0

                # The format requires LAST_VISIT and LAST_MODIFIED as well,
                # using ADD_DATE for these as Pocket export doesn't provide them.
                item_html: str = item_template.format(
                    url=url.replace("&", "&amp;"),  # Also escape ampersands in URL
                    date=date_added,
                    title=title,
                )
                outfile_typed.write(item_html + "\n")

            outfile_typed.write(html_footer)

        print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError as e_fnf:
        # This case is handled by the initial check, but kept for robustness
        print(f"Error: Input file not found: {input_file} ({e_fnf})", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e_csv:
        print(f"Error reading CSV file {input_file}: {e_csv}", file=sys.stderr)
        sys.exit(1)
    except IOError as e_io:
        print(f"Error writing to output file {output_file}: {e_io}", file=sys.stderr)
        sys.exit(1)
    except Exception as e_generic:
        print(f"An unexpected error occurred: {e_generic}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
