#!/usr/bin/env python3

import os
import threading   # <-- animation for progress bar
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from functools import partial
from PIL import Image, ImageTk

from Reduce_RFIQD_size import process_multiple_files, BYTES_PER_MB

def run_gui():
    # ----- Customizable Settings -----
    WINDOW_WIDTH = 680
    WINDOW_HEIGHT = 520
    BG_COLOR = "#4acbcb"
    BUTTON_COLOR = "#ff8f8f"
    FONT_FAMILY = "Times"
    FONT_SIZE = 10

    LOGO_PATH = "../Images/RFIQD_Compressor_Logo.png"

    root = tk.Tk()
    root.title("RFIQD Reducer")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(True, True)

    root.option_add("*Font", f"{FONT_FAMILY} {FONT_SIZE}")
    root.configure(bg=BG_COLOR)

    selected_files = []

    def add_files():
        file_paths = filedialog.askopenfilenames(
            title="Select RFIQD file(s)",
            filetypes=[("RFIQD Files", "*.rfiqd"), ("All Files", "*.*")]
        )
        for fp in file_paths:
            if fp not in selected_files:
                selected_files.append(fp)
        update_file_listbox()

    def remove_selected():
        sel = file_listbox.curselection()
        if not sel:
            messagebox.showerror("No selection", "Please select at least one file to remove.")
            return
        for index in reversed(sel):
            selected_files.pop(index)
        update_file_listbox()

    def clear_list():
        selected_files.clear()
        update_file_listbox()

    def update_file_listbox():
        file_listbox.delete(0, tk.END)
        for f in selected_files:
            file_listbox.insert(tk.END, f)

    def choose_outdir():
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            outdir_var.set(dir_path)

    def process_files():
        """Start the progress bar & spawn a background thread to do the actual processing."""
        if not selected_files:
            messagebox.showerror("No Files", "Please select at least one .rfiqd file.")
            return
        outdir = outdir_var.get().strip()
        if not outdir:
            messagebox.showerror("No Output Directory", "Please choose an output directory.")
            return

        try:
            header_size = int(header_size_var.get())
            offset = int(data_sample_offset_var.get())
            mb_value = int(data_sample_size_mb_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Header size, offset, and MB size must be integers.")
            return

        if mb_value < 0 or header_size < 0 or offset < 0:
            messagebox.showerror("Negative Value", "Values cannot be negative.")
            return

        data_sample_size_bytes = mb_value * BYTES_PER_MB

        if not os.path.isdir(outdir):
            try:
                os.makedirs(outdir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Directory Error", f"Could not create {outdir}\n{e}")
                return

        # Start the progress bar (indeterminate)
        progress_bar.configure(mode='indeterminate')
        progress_bar.start(10)  # animate every 10ms
        process_btn.config(state=tk.DISABLED)

        # Define a function that will run in the background thread
        def do_processing():
            try:
                process_multiple_files(
                    input_files=selected_files,
                    outdir=outdir,
                    header_size=header_size,
                    data_sample_offset=offset,
                    data_sample_size=data_sample_size_bytes
                )
            except Exception as ex:
                # Must show messagebox in the main thread
                root.after(0, lambda: messagebox.showerror("Processing Error", str(ex)))
            else:
                root.after(0, lambda: messagebox.showinfo("Done", "Mock RFIQD file(s) created successfully!"))
            finally:
                # Stop the progress bar in the main thread
                root.after(0, on_processing_complete)

        def on_processing_complete():
            """Stop the progress bar and enable the button."""
            progress_bar.stop()
            process_btn.config(state=tk.NORMAL)

        # Create and start a background thread
        threading.Thread(target=do_processing, daemon=True).start()

    # ----- UI Layout -----

    file_frame = tk.LabelFrame(root, text="Select .rfiqd File(s)", bg=BG_COLOR)
    file_frame.place(x=10, y=10, width=320, height=270)

    add_file_btn = tk.Button(file_frame, text="Add File(s)", command=add_files, width=15, bg=BUTTON_COLOR, fg="white")
    add_file_btn.pack(pady=5)

    remove_file_btn = tk.Button(file_frame, text="Remove Selected", command=remove_selected, width=15, bg=BUTTON_COLOR, fg="white")
    remove_file_btn.pack(pady=5)

    clear_file_btn = tk.Button(file_frame, text="Clear List", command=clear_list, width=15, bg=BUTTON_COLOR, fg="white")
    clear_file_btn.pack(pady=5)

    file_listbox = tk.Listbox(file_frame, selectmode=tk.MULTIPLE)
    file_listbox.pack(expand=True, fill="both", padx=5, pady=5)

    outdir_frame = tk.LabelFrame(root, text="Output Directory", bg=BG_COLOR)
    outdir_frame.place(x=10, y=290, width=320, height=80)

    outdir_var = tk.StringVar(value="./Output")
    outdir_entry = tk.Entry(outdir_frame, textvariable=outdir_var, width=25)
    outdir_entry.pack(side=tk.LEFT, padx=5, pady=5)

    choose_outdir_btn = tk.Button(outdir_frame, text="Browse...", command=choose_outdir, bg=BUTTON_COLOR, fg="white")
    choose_outdir_btn.pack(side=tk.LEFT, padx=5, pady=5)

    param_frame = tk.LabelFrame(root, text="Parameters", bg=BG_COLOR)
    param_frame.place(x=340, y=10, width=330, height=190)

    tk.Label(param_frame, text="Header Size (bytes):", bg=BG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    header_size_var = tk.StringVar(value="0")
    tk.Entry(param_frame, textvariable=header_size_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

    tk.Label(param_frame, text="Offset (bytes):", bg=BG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    data_sample_offset_var = tk.StringVar(value="0")
    tk.Entry(param_frame, textvariable=data_sample_offset_var, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    tk.Label(param_frame, text="Data Size (MB):", bg=BG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    data_sample_size_mb_var = tk.StringVar(value="10")
    tk.Entry(param_frame, textvariable=data_sample_size_mb_var, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

    action_frame = tk.LabelFrame(root, text="Actions", bg=BG_COLOR)
    action_frame.place(x=340, y=210, width=330, height=160)

    process_btn = tk.Button(action_frame, text="Process File(s)", command=process_files, width=15, bg="#4CAF50", fg="white")
    process_btn.pack(pady=10)

    progress_bar = ttk.Progressbar(action_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=5)

    try:
        img_pil = Image.open(LOGO_PATH)
        # Resize with a high-quality resampling filter
        resized_pil = img_pil.resize((150, 150), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(resized_pil)
    
        logo_label = tk.Label(root, image=logo_img, bg=BG_COLOR)
        logo_label.image = logo_img  # keep a reference
        logo_label.place(x=10, y=WINDOW_HEIGHT + 25, anchor="sw")

    except Exception as e:
        print("Failed to load/resize image:", e)
        

##    try:
#        logo_img = tk.PhotoImage(file=LOGO_PATH).subsample(3, 3)
#        logo_label = tk.Label(root, image=logo_img, bg=BG_COLOR)
#        logo_label.image = logo_img
#        # position bottom-left
#        logo_label.place(x=10, y=WINDOW_HEIGHT + 25, anchor="sw")
#    except Exception:
#        pass

    root.mainloop()


if __name__ == "__main__":
    run_gui()
