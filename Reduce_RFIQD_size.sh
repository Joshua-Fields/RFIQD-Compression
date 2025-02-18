#!/bin/bash
#
# Usage: 
#   ./Reduce_RFIQD_size.sh file1.rfiqd file2.rfiqd ... [--outdir DIR] ...
#
# Description:
#   This script calls the updated Python code (`Reduce_RFIQD_size.py`) 
#   which can process multiple RFIQD files at once. It accepts any 
#   number of .rfiqd files plus optional flags (e.g. --outdir, --header-size).
#   All arguments are forwarded directly to the Python script.
#
# Example:
#   ./Reduce_RFIQD_size.sh /d/Data/A.rfiqd /d/Data/B.rfiqd --outdir /d/ReducedOut

# 1) Figure out where this shell script is located
script_dir="$(cd "$(dirname "$0")" && pwd)"

# 2) Move into that directory so the Python script is found
pushd "$script_dir" > /dev/null

# 3) Forward all script arguments ($@) to the Python script
#    This means if the user types:
#       ./Reduce_RFIQD_size.sh file1.rfiqd file2.rfiqd --outdir output ...
#    we simply pass all those arguments along to Python.
python "$script_dir/Reduce_RFIQD_size.py" "$@"

# 4) Return to the original directory
popd > /dev/null
