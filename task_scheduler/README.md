# Task Scheduler (Priority-Based CLI)

A robust command-line interface (CLI) tool for the AlgoKit suite that allows you to manage and execute tasks based on a unique priority system. This module demonstrates the use of a min-heap (priority queue) for efficient task scheduling, ensuring that higher-priority tasks are processed first. All tasks are persistently stored in a local JSON file.

-----

## 🚀 Features

The `task_scheduler` offers the following functionalities:

  * **Add Tasks with Unique Priorities**: Define new tasks with a description and an integer priority level. The system enforces that each *pending* task must have a unique priority number (lower number indicates higher priority).
  * **Persistent Task Storage**: All tasks (pending and completed) are automatically saved to and loaded from a local `tasks.json` file, ensuring your task list is preserved across sessions.
  * **Run All Pending Tasks**: Execute all tasks currently in a 'pending' state. Tasks are processed strictly according to their priority, with the highest priority (lowest number) tasks running first.
  * **Execute Specific Task by Priority**: Directly execute a single pending task by providing its unique priority number, allowing for immediate processing of critical items out of sequence if needed.
  * **View All Tasks**: Display a comprehensive list of all tasks, including their ID, description, priority, added timestamp, and current status (pending or completed). Tasks are displayed sorted by priority.
  * **Clear Task History**: A utility command to completely reset the task list, removing all pending and completed tasks from the `tasks.json` file.
  * **Simulated Task Execution**: Tasks are "executed" by printing messages and simulating work with a brief delay, making it easy to observe the scheduler's behavior.

-----

## ⚙️ Key Concepts

This project demonstrates several important Python programming concepts and system design principles:

  * **Priority Queue (Min-Heap)**: Utilizes Python's built-in `heapq` module to implement a min-heap, which is a fundamental data structure for efficiently managing items based on their priority.
  * **Command-Line Interface (CLI)**: Employs `argparse` to create a flexible and user-friendly CLI with subcommands (`add`, `run-all`, `execute`, `view`, `clear-history`).
  * **File Handling (JSON)**: Uses the `json` module for persistent storage of task data, allowing for easy serialization and deserialization of Python dictionaries and lists.
  * **Unique ID Generation**: Leverages the `uuid` module to assign unique identifiers to each task, aiding in tracking and management.
  * **Timestamping**: Uses the `datetime` module to record when tasks are added and completed.
  * **Modular Design**: Code is organized into distinct functions for clear separation of concerns (e.g., loading/saving, adding, executing, viewing tasks).
  * **Logging**: Provides informative console output using the `logging` module for better user feedback and debugging.

-----

## 📦 How to Run

Follow these steps to get the `task_scheduler` running on your local machine:

1.  **Navigate to the Module Directory**:
    Open your terminal or command prompt and change your current directory to `algokit/task_scheduler/`.

    ```bash
    cd algokit/task_scheduler/
    ```

2.  **Ensure `tasks.json` Exists**:
    Make sure an empty `tasks.json` file exists in the same directory as `main.py`. If it doesn't, you can create it manually:

    ```bash
    # On Windows PowerShell:
    New-Item -Path tasks.json -ItemType File -Value "[]"

    # On Linux/macOS:
    touch tasks.json
    echo "[]" > tasks.json
    ```

    The script will manage this file for storing your task data.

3.  **Use the Commands**:
    The `task_scheduler` uses subcommands for different operations.

      * **Add a New Task**:
        To add a task, specify a `description` (in quotes if it contains spaces) and a unique `priority` number. Remember, **lower numbers mean higher priority**.

        ```bash
        python main.py add "Perform critical database backup" 1
        python main.py add "Generate daily sales report" 5
        python main.py add "Send marketing emails" 10
        python main.py add "Clean up temporary files" 8
        python main.py add "Urgent bug fix deployment" 0
        ```

        *If you try to add a task with a priority that is already assigned to a *pending* task, the script will display an error and prevent the addition.*

      * **View All Tasks**:
        To see all tasks (pending and completed), sorted by priority:

        ```bash
        python main.py view
        ```

      * **Execute a Single Task by Priority**:
        To run a specific pending task immediately, provide its unique priority number:

        ```bash
        python main.py execute 3
        ```

        (This will execute the task that has been assigned priority `3`).

      * **Run All Pending Tasks**:
        To process all tasks currently in 'pending' status, in order of their priority:

        ```bash
        python main.py run-all
        ```

        You will see messages as each task is "executed." After the scheduler finishes, you can use `python main.py view` again to see their updated statuses.

      * **Clear Task History**:
        To remove all tasks (pending and completed) from `tasks.json` and reset the history:

        ```bash
        python main.py clear-history
        ```

-----

## ✅ Checkpoints & Evaluation

The `task_scheduler` module has been developed to meet specific requirements and demonstrate key features:

### **1. Command-line tool to add tasks with priorities**

  * **Status:** **PASS**
  * **Evaluation:** The `add` subcommand allows users to specify a task description and an integer priority.
  * **Implementation Detail:** `argparse` is used to define the `add` subcommand with `description` and `priority` arguments.

### **2. Uses custom queue or heap logic for scheduling**

  * **Status:** **PASS**ng tasks and uses Python's `heapq` module to maintain them in a min-heap (priority queue). Tasks are extracted and executed based on their priority (lowest number first).
  * **Implementation Detail:** `heapq.heappush` and `heapq.heappop` are used within `run_scheduler`.

### **3. Priority number should always be unique (for pending tasks)**

  * **Status:** **PASS**
  * **Evaluation:** The `add_task` function now includes a check to ensure that no two *pending* tasks share the same priority number. If a duplicate is attempted, an error message is displayed, and the task is not added.
  * **Implementation Detail:** A loop iterates through existing pending tasks to validate uniqueness before adding a new one.

### **4. Run tasks individually based on their Priority number**

  * **Status:** **PASS**
  * **Evaluation:** The new `execute` subcommand allows users to specify a priority number, and the scheduler will find and execute only that specific pending task.
  * **Implementation Detail:** The `execute_single_task` function searches for the exact task by priority and processes it.

### **5. Clear history command (`json` will be `[]`)**

  * **Status:** **PASS**
  * **Evaluation:** The `clear-history` subcommand successfully empties the `tasks.json` file, effectively resetting the entire task history.
  * **Implementation Detail:** The `clear_history` function overwrites `tasks.json` with an empty JSON array `[]`.

### **6. Persistent Storage**

  * **Status:** **PASS**
  * **Evaluation:** All tasks, including their descriptions, priorities, unique IDs, added times, and statuses, are loaded from and saved to `tasks.json`, ensuring data is preserved between program runs.
  * **Implementation Detail:** `load_tasks` and `save_tasks` functions handle JSON file I/O.

### **7. Logging & User Feedback**

  * **Status:** **PASS**
  * **Evaluation:** The script provides clear and informative messages to the console about task additions, executions, completions, and errors.
  * **Implementation Detail:** Uses the `logging` module for various levels of output.

### **8. Cross-Platform Compatibility**

  * **Status:** **PASS**
  * **Evaluation:** The module relies solely on Python's standard library (`os`, `json`, `heapq`, `uuid`, `datetime`, `time`, `argparse`), which ensures it runs consistently across Windows, macOS, and Linux.
  * **Implementation Detail:** Uses OS-agnostic functions for file paths and operations.
  * **Evaluation:** The `run-all` command loads pendi