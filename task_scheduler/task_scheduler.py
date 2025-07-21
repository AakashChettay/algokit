# algokit/task_scheduler/main.py
import os
import json
import logging
import argparse
import heapq # For priority queue (min-heap)
import uuid # For unique task IDs
import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.StreamHandler()
                    ])

# File to store tasks
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

def load_tasks() -> list:
    """
    Loads tasks from the JSON storage file.

    Returns:
        list: A list of task dictionaries. Returns an empty list if the file
              doesn't exist or is invalid.
    """
    if not os.path.exists(TASKS_FILE):
        logging.info("Tasks file not found. Starting with an empty task list.")
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
            if not isinstance(tasks, list):
                logging.warning("Tasks file content is not a list. Starting with empty list.")
                return []
            logging.info(f"Loaded {len(tasks)} tasks from {TASKS_FILE}.")
            return tasks
    except json.JSONDecodeError as e:
        logging.error(f"Error reading {TASKS_FILE}: {e}. File might be corrupted. Starting with empty list.")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading tasks: {e}. Starting with empty list.")
        return []

def save_tasks(tasks: list):
    """
    Saves the current list of tasks to the JSON storage file.

    Args:
        tasks (list): The list of task dictionaries to save.
    """
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
        logging.info(f"Saved {len(tasks)} tasks to {TASKS_FILE}.")
    except Exception as e:
        logging.error(f"Error saving tasks to {TASKS_FILE}: {e}")

def add_task(description: str, priority: int):
    """
    Adds a new task to the task list and saves it.
    Enforces unique priority numbers for pending tasks.

    Args:
        description (str): A brief description of the task.
        priority (int): The priority level (lower number = higher priority).
    """
    tasks = load_tasks()
    
    # Check for unique priority among pending tasks
    for task in tasks:
        if task.get('status') == 'pending' and task.get('priority') == priority:
            print(f"Error: A pending task with priority '{priority}' already exists ('{task['description']}').")
            print("Please choose a unique priority number for this task.")
            return

    task_id = str(uuid.uuid4()) # Generate a unique ID for the task
    added_time = datetime.datetime.now().isoformat() # ISO format for easy storage

    new_task = {
        'id': task_id,
        'description': description,
        'priority': priority,
        'added_time': added_time,
        'status': 'pending' # Tasks are pending when added
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' (Priority: {priority}) added with ID: {task_id} ✅")

def get_pending_tasks(all_tasks: list) -> list:
    """
    Filters and returns only the tasks that are in 'pending' status.

    Args:
        all_tasks (list): The full list of tasks.

    Returns:
        list: A list of pending task dictionaries.
    """
    return [task for task in all_tasks if task.get('status') == 'pending']

def execute_single_task(priority_to_execute: int):
    """
    Finds and executes a single pending task based on its unique priority number.

    Args:
        priority_to_execute (int): The unique priority number of the task to execute.
    """
    all_tasks = load_tasks()
    
    task_found = None
    task_index = -1
    for i, task in enumerate(all_tasks):
        if task.get('status') == 'pending' and task.get('priority') == priority_to_execute:
            task_found = task
            task_index = i
            break
    
    if not task_found:
        print(f"Error: No pending task found with priority '{priority_to_execute}'.")
        return

    print(f"\n--- Executing Task (Priority: {task_found['priority']}): {task_found['description']} ---")
    logging.info(f"Task ID: {task_found['id']}, Priority: {task_found['priority']}, Description: {task_found['description']}")
    
    # Simulate task execution
    simulated_work_time = max(0.5, len(task_found['description']) / 20.0) # Longer description = more work
    time.sleep(min(3, simulated_work_time)) # Cap at 3 seconds for demo

    # Update task status
    all_tasks[task_index]['status'] = 'completed'
    all_tasks[task_index]['completed_time'] = datetime.datetime.now().isoformat()
    
    save_tasks(all_tasks) # Save updated statuses
    print(f"Task '{task_found['description']}' completed. ✅")
    print(f"\n--- Task execution for priority {priority_to_execute} finished ---")


def run_scheduler():
    """
    Loads all pending tasks, processes them using a priority queue (min-heap),
    and marks them as completed.
    """
    all_tasks = load_tasks()
    pending_tasks = get_pending_tasks(all_tasks)

    if not pending_tasks:
        print("\nNo pending tasks to run. Add tasks using 'python main.py add ...' first.")
        return

    # Create a min-heap (priority queue) from pending tasks
    # Heap elements are tuples: (priority, task_id, task_dict)
    # Since priority is now unique, task_id is just for reference/tie-breaking (though not strictly needed for order)
    task_heap = []
    for task in pending_tasks:
        heapq.heappush(task_heap, (task['priority'], task['id'], task))

    print(f"\n--- Running Scheduler: Processing {len(task_heap)} pending tasks ---")

    processed_count = 0
    while task_heap:
        priority, task_id, task = heapq.heappop(task_heap) # Unpack the tuple
        
        print(f"\nExecuting Task (Priority: {priority}): {task['description']}")
        logging.info(f"Task ID: {task_id}, Priority: {priority}, Description: {task['description']}")
        
        # Simulate task execution
        simulated_work_time = max(0.5, len(task['description']) / 20.0)
        time.sleep(min(3, simulated_work_time))

        # Update task status in the original all_tasks list
        # Find the task by ID to update its status
        for i, t in enumerate(all_tasks):
            if t['id'] == task_id:
                all_tasks[i]['status'] = 'completed'
                all_tasks[i]['completed_time'] = datetime.datetime.now().isoformat()
                break
        
        processed_count += 1
        print(f"Task '{task['description']}' completed. ✅")
    
    save_tasks(all_tasks) # Save updated statuses
    print(f"\n--- Scheduler Finished: {processed_count} tasks processed ---")

def view_tasks():
    """
    Displays all tasks (pending and completed) from the tasks file.
    """
    all_tasks = load_tasks()
    if not all_tasks:
        print("\nNo tasks found. Add some first!")
        return

    print("\n--- All Tasks ---")
    # Sort tasks for consistent viewing, e.g., by priority then by added time
    all_tasks.sort(key=lambda x: (x.get('priority', float('inf')), x.get('added_time', '')))

    for i, task in enumerate(all_tasks):
        print(f"--- Task {i + 1} ---")
        print(f"ID: {task.get('id', 'N/A')}")
        print(f"Description: {task.get('description', 'N/A')}")
        print(f"Priority: {task.get('priority', 'N/A')}")
        print(f"Added: {task.get('added_time', 'N/A')}")
        print(f"Status: {task.get('status', 'N/A').upper()}")
        if task.get('status') == 'completed':
            print(f"Completed: {task.get('completed_time', 'N/A')}")
        print("-" * 20) # Separator

def clear_history():
    """
    Clears all tasks (both pending and completed) from the tasks.json file.
    Resets the task history.
    """
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f, indent=4) # Write an empty list
        print(f"\nTask history cleared. All tasks removed from {TASKS_FILE}. 🧹")
        logging.info("Task history cleared.")
    except Exception as e:
        logging.error(f"Error clearing task history: {e}")
        print(f"Failed to clear task history: {e}")


def main():
    """
    Main entry point for the Task Scheduler script.
    Handles command-line arguments for adding, running all, executing single, viewing, and clearing tasks.
    """
    parser = argparse.ArgumentParser(
        description="AlgoKit Task Scheduler: A command-line tool to manage and execute tasks based on unique priorities."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task to the scheduler with a unique priority.')
    add_parser.add_argument('description', type=str, help='A brief description of the task.')
    add_parser.add_argument('priority', type=int, help='The unique priority level (lower number = higher priority).')

    # Run all pending tasks command
    run_all_parser = subparsers.add_parser('run-all', help='Run all pending tasks based on their priority (highest priority first).')

    # Execute single task command
    execute_parser = subparsers.add_parser('execute', help='Execute a single pending task by its unique priority number.')
    execute_parser.add_argument('priority', type=int, help='The unique priority number of the task to execute.')

    # View tasks command
    view_parser = subparsers.add_parser('view', help='View all tasks (pending and completed), sorted by priority.')

    # Clear history command
    clear_history_parser = subparsers.add_parser('clear-history', help='Clear all tasks (pending and completed) from the history.')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description, args.priority)
    elif args.command == 'run-all':
        run_scheduler()
    elif args.command == 'execute':
        execute_single_task(args.priority)
    elif args.command == 'view':
        view_tasks()
    elif args.command == 'clear-history':
        clear_history()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()