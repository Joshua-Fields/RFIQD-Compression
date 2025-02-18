#!/usr/bin/env python3

import PySimpleGUI as sg
import os
from Reduce_RFIQD_size import process_multiple_files

def run_gui():
    """
    A PySimpleGUI interface that:
      - Lets the user select one RFIQD file at a time,
      - Then 'Add File' to accumulate multiple files in a list.
      - Finally, processes all files in bulk when 'Process' is clicked.
    """

    sg.theme("SystemDefault")

    # We'll store all selected files in this Python list:
    added_files = []

    layout = [
        [sg.Text("Choose a single .rfiqd file:")],
        [
            sg.Input(key="-FILE-", size=(50,1), enable_events=True), 
            sg.FileBrowse(
                file_types=(("RFIQD Files","*.rfiqd"), ("All Files","*.*")),
                key="-BROWSE-"
            )
        ],
        [
            sg.Button("Add File", size=(10,1)), 
            sg.Button("Remove Selected", size=(15,1)), 
            sg.Button("Clear List", size=(10,1))
        ],
        [
            sg.Listbox(values=[], size=(60,6), key="-FILE_LIST-", enable_events=True)
        ],
        [
            sg.Text("Output Directory:"),
            sg.Input(default_text=".", key="-OUTDIR-", size=(50,1)),
            sg.FolderBrowse()
        ],
        [
            sg.Text("Header Size (bytes):"),
            sg.Input(default_text="4096", key="-HEADER-", size=(10,1))
        ],
        [
            sg.Text("Data Offset (bytes):"),
            sg.Input(default_text="65536", key="-OFFSET-", size=(10,1))
        ],
        [
            sg.Text("Data Sample Size (bytes):"),
            sg.Input(default_text="1048576", key="-SIZE-", size=(10,1))
        ],
        [
            sg.Button("Process", size=(10,1)),
            sg.Button("Exit", size=(10,1))
        ]
    ]

    window = sg.Window("RFIQD Reducer (Single-file Browse)", layout)

    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Add File":
            chosen_file = values["-FILE-"]
            if chosen_file:
                # If this file isn't already in the list, append it
                if chosen_file not in added_files:
                    added_files.append(chosen_file)
                    window["-FILE_LIST-"].update(added_files)
                else:
                    sg.popup("File is already in the list!", title="Duplicate")
            else:
                sg.popup_error("No file selected. Please browse for a file first.")

        elif event == "Remove Selected":
            # Remove whatever is highlighted in the listbox
            selected_items = values["-FILE_LIST-"]
            if not selected_items:
                sg.popup_error("No file selected in the list to remove.")
            else:
                added_files = [f for f in added_files if f not in selected_items]
                window["-FILE_LIST-"].update(added_files)

        elif event == "Clear List":
            added_files = []
            window["-FILE_LIST-"].update([])

        elif event == "Process":
            # Must have at least one file in the list
            if not added_files:
                sg.popup_error("No files have been added to the list.")
                continue

            outdir = values["-OUTDIR-"] or "."

            # Convert user inputs to integers
            try:
                header_size = int(values["-HEADER-"])
                offset = int(values["-OFFSET-"])
                size = int(values["-SIZE-"])
            except ValueError:
                sg.popup_error("Header size, offset, and data size must be integers.")
                continue

            # Process all files
            process_multiple_files(
                input_files=added_files,
                outdir=outdir,
                header_size=header_size,
                data_sample_offset=offset,
                data_sample_size=size
            )

            sg.popup("Processing complete!", f"Reduced files are in:\n{outdir}")

    window.close()

if __name__ == "__main__":
    run_gui()
