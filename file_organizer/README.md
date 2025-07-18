# File Organizer

A powerful and modular Python utility designed to automatically sort and organize files within a specified directory. It categorizes files based on their type (extension) and moves them into designated subfolders, helping to declutter and maintain an organized file system.

-----

## 🚀 Features

The `file_organizer` offers the following capabilities:

  * **Intelligent File Categorization**: Automatically identifies file types (e.g., documents, images, videos, code) based on their extensions and moves them into predefined category subfolders.
  * **Recursive Organization**: Ability to process files not just in the specified root directory, but also within all its nested subfolders.
  * **Duplicate File Handling**: Automatically renames files if a file with the same name already exists in the destination folder, preventing accidental overwrites.
  * **Hidden/System File Exclusion**: Skips hidden files (e.g., `.DS_Store`, files starting with `.`) and system-specific files, ensuring they are not moved or altered.
  * **Configurable Categories**: File type to folder mappings are defined in an external `config.json` file, allowing for easy customization without modifying the core code.
  * **Dry Run Mode**: Provides a simulation mode to preview exactly what changes (file moves, folder creations) would occur without actually performing them.
  * **Clear Logging**: Outputs detailed information to the console about every action taken (or proposed in dry run), including file moves, directory creations, and skipped files.
  * **Cross-Platform Compatibility**: Built using Python's standard `os` and `shutil` modules, ensuring seamless operation across Windows, macOS, and Linux.

-----

## ⚙️ Key Concepts

This project demonstrates several core programming concepts and best practices:

  * **File System Interaction**: Utilizes Python's `os` and `shutil` modules for navigating directories, creating folders, and moving files.
  * **Command-Line Interface (CLI)**: Implements `argparse` for robust command-line argument parsing, allowing users to control the script's behavior (source directory, recursive mode, dry run).
  * **Configuration Management**: Employs `json` to load external configuration, making the file categorization highly customizable.
  * **Error Handling**: Incorporates `try-except` blocks to gracefully manage potential issues like permission errors or invalid paths during file operations.
  * **Modular Design**: Code is structured into functions with clear responsibilities, enhancing readability and maintainability.
  * **Logging**: Uses Python's `logging` module for informative output, aiding in debugging and user feedback.

-----

## 📦 How to Run

Follow these steps to get the `file_organizer` up and running:

1.  **Navigate to the Module Directory**:
    Open your terminal or command prompt and change your current directory to `algokit/file_organizer/`.

    ```bash
    cd algokit/file_organizer/
    ```

2.  **Ensure `config.json` Exists**:
    Make sure the `config.json` file is present in the same directory as `main.py`. This file defines your file categories. An example `config.json` might look like this:

    ```json
    {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".ods", ".odp"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".mpeg", ".mpg"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executables": [".exe", ".dmg", ".app", ".msi", ".bat", ".sh"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".php", ".json", ".xml", ".ipynb"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
        "Others": []
    }
    ```

3.  **Prepare a Test Directory (Optional but Recommended)**:
    For safe testing, create a dedicated folder outside your project (e.g., on your Desktop or in your User directory) and populate it with various file types, including some in subfolders and some hidden files.

    **Example `file_organizer_test` directory structure:**

    ```
    C:\Users\YourUser\file_organizer_test\
    ├── document.pdf
    ├── report.docx
    ├── photo.jpg
    ├── song.mp3
    ├── script.py
    ├── presentation.pptx
    ├── archive.zip
    ├── unknown.xyz
    ├── .hidden_config.txt          # Hidden file (Unix-style)
    ├── SubFolder1/
    │   ├── nested_doc.txt
    │   └── nested_image.png
    ├── SubFolder2/
    │   ├── another_video.mp4
    │   ├── important_code.js
    │   └── .dot_file_in_sub.log    # Hidden file in subfolder
    │   └── .hidden_subfolder/      # Hidden subfolder
    ```

    *(To create these on Windows PowerShell, you can use `New-Item -Path <filename> -ItemType File` for files and `mkdir <foldername>` for folders. For `.hidden_files`, just include the dot in the name).*

4.  **Run the Script**:
    Use the `python` command followed by `main.py` and the path to the directory you wish to organize.

      * **Basic Usage (Flat Directory):**
        To organize files only in the top-level of a folder:

        ```bash
        python main.py <PATH_TO_YOUR_DIRECTORY>
        ```

        Example:

        ```bash
        python main.py C:\Users\YourUser\Downloads
        ```

        or (for Linux/macOS)

        ```bash
        python main.py ~/Downloads
        ```

      * **Recursive Usage (Including Subfolders):**
        To organize files found within subfolders as well (recommended for the `file_organizer_test` example):

        ```bash
        python main.py <PATH_TO_YOUR_DIRECTORY> --recursive
        ```

        Example:

        ```bash
        python main.py "C:\Users\YourUser\file_organizer_test" --recursive
        ```

      * **Dry Run Mode (Preview Changes):**
        To see what actions the script *would* take without actually moving any files:

        ```bash
        python main.py <PATH_TO_YOUR_DIRECTORY> --dry-run
        ```

        Or with recursion for a full preview (recommended for the `file_organizer_test` example first):

        ```bash
        python main.py "C:\Users\YourUser\file_organizer_test" --dry-run --recursive
        ```

    **Important:** Replace `<PATH_TO_YOUR_DIRECTORY>` with the actual absolute or relative path to the folder you want to organize. The script will create subfolders like `Documents`, `Images`, etc., within the specified directory and move files accordingly. Files not matching defined categories will go into an `Others` folder.

-----

## ✅ Checkpoints & Evaluation

The `file_organizer` module has been developed with several key capabilities in mind. Here's a detailed evaluation of each checkpoint:

### **1. Handles Duplicate Filenames? (e.g., `file.txt` & `file.txt` → no overwrite)**

  * **Status:** **PASS**
  * **Evaluation:** The script incorporates logic (`get_unique_filename` function) to prevent accidental overwrites. If a file with the same name already exists in the destination category folder, the new file will be automatically renamed by appending a timestamp (e.g., `report_20250718_123456.pdf`) or a counter to ensure uniqueness.
  * **Implementation Detail:** `shutil.move` is performed only after ensuring the target filename is unique.

### **2. Ignores System/Hidden Files?**

  * **Status:** **PASS**
  * **Evaluation:** The `is_hidden_or_system_file` function effectively identifies and skips files that are hidden (e.g., files starting with `.` on Unix-like systems) and attempts to detect hidden attributes on Windows. Hidden directories are also excluded during recursive scans. These files/folders will remain in their original locations.
  * **Implementation Detail:** Files are filtered using `os.path.basename().startswith('.')` and `os.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN` on Windows.

### **3. Works on Nested Folders? Or only flat files?**

  * **Status:** **PASS**
  * **Evaluation:** By utilizing the `--recursive` command-line argument, the script can traverse into all subdirectories within the specified source path (`os.walk` is used for this). Files found in these nested folders are moved to the appropriate category subfolders created directly in the *root* of the specified source directory. Original subfolders are left empty (if all their contents are moved).
  * **Implementation Detail:** The `organize_files` function uses `os.walk` when `recursive` is `True`.

### **4. Logs Actions to Console or File?**

  * **Status:** **PASS**
  * **Evaluation:** The script uses Python's standard `logging` module to provide clear, real-time feedback to the console. It logs successful moves, directory creations, warnings (e.g., file renames), and errors.
  * **Implementation Detail:** `logging.basicConfig` is set up for `INFO` level messages, which are printed to `stdout`.

### **5. Has a Config for Which Extensions Map to Which Folders?**

  * **Status:** **PASS**
  * **Evaluation:** The mapping of file extensions to their respective category folders (e.g., `.jpg` to `Images`, `.pdf` to `Documents`) is stored in an external `config.json` file. This allows users to easily customize or expand categories without altering the Python code itself.
  * **Implementation Detail:** The `load_categories_from_config` function reads this `config.json` at the start of execution.

### **6. Dry Run Mode? (Preview changes before moving)**

  * **Status:** **PASS**
  * **Evaluation:** The `--dry-run` argument enables a simulation mode. When active, the script performs all the logic (identifying files, determining destinations, checking for duplicates) but replaces actual `shutil.move` operations with informative log messages prefixed with `[DRY RUN]`. No files are moved, and no directories are created.
  * **Implementation Detail:** A `dry_run` boolean flag controls whether actual file system operations are performed.

### **7. Safe Rollback if Interrupted? (optional, advanced)**

  * **Status:** **FAIL**
  * **Evaluation:** This feature is **not** implemented. If the script is interrupted during an active run (e.g., by force-quitting the terminal), some files may have been moved while others haven't, leading to an inconsistent state. Implementing a robust rollback mechanism would require a more complex transaction logging system.
  * **Implementation Detail:** No specific code has been added for rollback functionality.

### **8. Works Cross-Platform? (Windows/Mac/Linux paths)**

  * **Status:** **PASS**
  * **Evaluation:** The script exclusively uses modules from Python's standard library (`os`, `shutil`, `json`, `argparse`, `logging`, `datetime`, `stat`) that are designed to be cross-platform compatible. Path handling (e.g., `os.path.join`) automatically adjusts to the conventions of the underlying operating system.
  * **Implementation Detail:** Relies on Python's built-in OS abstraction.