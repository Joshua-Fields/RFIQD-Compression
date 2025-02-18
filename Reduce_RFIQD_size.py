#!/usr/bin/env python3
import os
import argparse

def create_mock_rfiqd(
    input_path: str,
    output_path: str,
    header_size: int = 4096,
    data_sample_offset: int = 34816,
    data_sample_size: int = 1048576
):
    """
    Creates a smaller 'mock' .rfiqd file by copying:
      1) The initial header bytes (specified by header_size).
      2) A portion of the data (specified by data_sample_offset and data_sample_size).
    """
    # Check if input file exists
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return  # or raise an exception

    file_size = os.path.getsize(input_path)
    if file_size == 0:
        print(f"Error: The file '{input_path}' is empty.")
        return

    try:
        with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            # 1) Copy the header
            header = f_in.read(header_size)
            f_out.write(header)

            # 2) Seek to the data_sample_offset (if within the file)
            if data_sample_offset < file_size:
                f_in.seek(data_sample_offset)
                remaining_bytes = file_size - data_sample_offset
                read_size = min(data_sample_size, remaining_bytes)
                data_sample = f_in.read(read_size)
                f_out.write(data_sample)

        print(f"[OK] Created mock file: {output_path}")
    except Exception as e:
        print(f"[ERROR] {e}")


def process_multiple_files(
    input_files,
    outdir: str,
    header_size: int = 4096,
    data_sample_offset: int = 34816,
    data_sample_size: int = 1048576
):
    """
    Process multiple input RFIQD files, creating reduced versions in `outdir`.
    Files are named: <original_basename>_mock.rfiqd
    """
    # Ensure outdir exists
    os.makedirs(outdir, exist_ok=True)

    for inpath in input_files:
        filename = os.path.basename(inpath)
        base_noext, ext = os.path.splitext(filename)  # e.g. ("somefile", ".rfiqd")
        # Construct an output path
        outpath = os.path.join(outdir, f"{base_noext}_mock{ext}")

        print(f"Processing: {inpath}")
        create_mock_rfiqd(
            input_path=inpath,
            output_path=outpath,
            header_size=header_size,
            data_sample_offset=data_sample_offset,
            data_sample_size=data_sample_size
        )


def main():
    parser = argparse.ArgumentParser(
        description="Reduce the size of one or more .rfiqd files."
    )
    parser.add_argument(
        "input_files", 
        nargs="+", 
        help="One or more .rfiqd files to process."
    )
    parser.add_argument(
        "--outdir", 
        default="./Output",
        help="Directory where reduced files will be placed (default is current dir)."
    )
    parser.add_argument(
        "--header-size", 
        type=int, 
        default=4096, 
        help="Number of bytes to copy from the start (default 4096)."
    )
    parser.add_argument(
        "--data-sample-offset", 
        type=int, 
        default=65536, 
        help="Offset in bytes from which to begin copying data (default 65536)."
    )
    parser.add_argument(
        "--data-sample-size", 
        type=int, 
        default=1048576, 
        help="Number of bytes to copy after offset (default 1 MB)."
    )

    args = parser.parse_args()

    # Call the multi-file processing function
    process_multiple_files(
        input_files=args.input_files,
        outdir=args.outdir,
        header_size=args.header_size,
        data_sample_offset=args.data_sample_offset,
        data_sample_size=args.data_sample_size
    )


if __name__ == "__main__":
    main()
