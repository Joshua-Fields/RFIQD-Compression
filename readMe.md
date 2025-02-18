# RFIQD Flattening & Mock-File Reducer

This repository provides tools to **reduce the size** of `.rfiqd` files by creating “mock” copies with limited data. It includes:

- **Python script** (`Reduce_RFIQD_size.py`): Command-line usage  
- **Shell script** (`Reduce_RFIQD_size.sh`): For Git Bash / Linux / macOS  
- **Batch script** (`Reduce_RFIQD_size.bat`): For Windows Command Prompt  
- **Optional GUI** (`rfiqd_gui.py`): Requires additional libraries (PySimpleGUI)
- **Standalone Executable** (`rfiqd_gui.exe`): No additional requirements


---

## Requirements

- **Python 3.6+** (verified on Python 3.13)  
- If you plan to use the **GUI** (`rfiqd_gui.py`), install dependencies from `requirements.txt`:
  
  ```bash
  pip install -r requirements.txt
  ```

  This will install **PySimpleGUI** and any other necessary packages.

---

## 1. Python Script Usage

1. **Open** a terminal (Command Prompt, PowerShell, or Git Bash).  
2. **Navigate** (`cd`) to the `rfiqd_flattening_python_script` folder (the one containing `Reduce_RFIQD_size.py`).  
3. **Run** the Python script with your `.rfiqd` file(s) as parameters:
   
   ```bash
   python Reduce_RFIQD_size.py "D:\Path\To\Your\...\2023-10-17_13-18-50.741.rfiqd"
   ```

### Multiple Files

You can specify multiple `.rfiqd` files in one command:

```bash
python Reduce_RFIQD_size.py ^
  "D:\path\to\file1.rfiqd" ^
  "D:\path\to\file2.rfiqd" ^
  --outdir "D:\output\directory"
```

- **Default Output**: If you do **not** specify `--outdir`, the reduced files are placed in the **Output** folder within this repo.  
- **Custom Output**: Use `--outdir "D:/output/directory"` to store them elsewhere.

---

## 2. Shell Script Usage (Git Bash / Linux / macOS)

1. **Open** Git Bash (or another Unix-like shell).  
2. **Navigate** (`cd`) to the `rfiqd_flattening_python_script` folder.  
3. **Run** the shell script, passing your original `.rfiqd` file(s) as parameters:
   
   ```bash
   ./Reduce_RFIQD_size.sh "D:/path/to/file.rfiqd"
   ```

### Multiple Files

Add as many `.rfiqd` files as you like, plus optional `--outdir`:

```bash
./Reduce_RFIQD_size.sh \
  "D:/path/file1.rfiqd" \
  "D:/path/file2.rfiqd" \
  --outdir "D:/output/directory"
```

- If you omit `--outdir`, the reduced files go into the **Output** folder by default.

---

## 3. Batch Script Usage (Windows CMD)

1. **Open** Command Prompt (cmd.exe).  
2. **Navigate** (`cd`) to the `rfiqd_flattening_python_script` folder.  
3. **Run**:
   
   ```bat
   Reduce_RFIQD_size.bat "D:\path\to\file.rfiqd"
   ```

### Multiple Files

You can list multiple `.rfiqd` files:

```bat
Reduce_RFIQD_size.bat ^
  "D:\path\to\file1.rfiqd" ^
  "D:\path\to\file2.rfiqd" ^
  --outdir "D:\some\other\directory"
```

- Omit `--outdir` to place reduced files in the **Output** folder.

---

## Notes

- **Paths with spaces** must be quoted, e.g. `"D:\DV2 Pilot Original\..."`.  
- You can supply as many `.rfiqd` files as desired; each will produce a `_mock.rfiqd` version.  
- Defaults: Copies **4 KB** of the file header and a **1 MB** data sample starting at an offset of **64 KB**. Adjust parameters via the command line (e.g., `--header-size`, `--data-sample-offset`, `--data-sample-size`).

---

_Enjoy reducing your RFIQD files!_