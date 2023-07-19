# Using the task_manager.py file, modify the programme by refactoring the code to ensure readability for devs.

# OS module imported to use alongside the display_statistics function.
# Source: https://www.tutorialsteacher.com/python/os-module#?utm_content=cmp-true
import os

# datetime module imported to ensure accurate user input of dates. 
# Source: https://www.programiz.com/python-programming/datetime 
import datetime

# Function to create the 'user.txt' file if it doesn't exist:
def create_user_file():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as file:
            file.write("admin;password\n")  # Writes admin user and password to the file.

def is_admin(curr_user):
    ''' Takes in the input of the curr_user,
    if "admin" is entered, programme detects as is_admin
    allowing access to 'gr' and 'ds' functions.
    Source: https://www.programiz.com/python-programming/docstrings '''
    return curr_user == "admin"

# Function which allows users to login: distinguishing between user admin and regular user:
def login():
    create_user_file()
    # Reads usernames from user.txt file.
    with open("user.txt", "r") as file:
        users = {line.strip().split(";")[0]: line.strip().split(";")[1] for line in file}

    username = input("Enter your username: ")
    if username in users:
        password = input("Password: ")
        if users[username] == password:
            print("\nLogin successful!")
            if is_admin(username):
                print("\nWelcome, admin!")
                menu("admin")
            else:
                print("\nWelcome, " + username)
                menu(username)
        else:
            print("Invalid username or password. Please try again!")
            login()
    else:
        print("You are not registered. Please register first.")
        reg_user()

# Function which registers new users and asks for a password; 
# if the username already exists within the file, an error message prints:
def reg_user():
    username = input("Register your username: ")
    password = input("Enter your password: ")

    with open("user.txt", "r") as file:
        if username in file.read():
            print("Username already exists. Please try again.")
            return reg_user()
        
    with open("user.txt", "a") as file:
        file.write(f"{username}; {password}\n")

    print("User registered successfully.")
    menu(username)

# Function which allows a user to add new tasks to the .txt file, asking for specific inputs:
def add_task():
    task_user = input("Enter your username: ")
    task_name = input("Enter the task name: ")
    task_description = input("Enter the task description: ")
    assigned_date = input("Enter the assigned date (DD-MM-YYYY): ")
    due_date = input("Enter the due date (DD-MM-YYYY): ")

    try:
        datetime.datetime.strptime(assigned_date, "%d-%m-%Y")
        datetime.datetime.strptime(due_date, "%d-%m-%Y")   # Utilises the datetime module to ensure correct formatting of date input
    except ValueError:  # Raises error if invalid date input
        print("Invalid date format. Please enter the date in the format DD-MM-YYYY.")
        add_task()
        return
    
    with open("tasks.txt", "a") as file:
        file.write(f"{task_user}: {task_name} - {task_description} - {assigned_date} - {due_date}\n")

    print("Task added successfully.")
    menu(task_user)

# Function which allows a user to view all the tasks currently in the .txt file:
def view_all():
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    if tasks:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.strip()}")
    else:
        print("No tasks available.")

# Function which allows a user to view and edit their assigned tasks:
def view_mine():
    username = input("Enter your username: ")
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    assigned_tasks = [task.strip() for task in tasks if task.startswith(username)]
    if assigned_tasks:
        for i, task in enumerate(assigned_tasks, start=1):
            print(f"{i}. {task}")
        
        task_number = int(input("Enter the task number to edit: "))
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return
        
        task = tasks[task_number - 1].strip()
        print(f"Selected task: {task}")

        if "[Complete]" in task:
            print("This task is already marked as complete and cannot be edited.")
            view_mine()
            return

        choice = input("Do you want to mark it as complete? (Yes/No) ")
        if choice.lower() == "yes":
            tasks[task_number - 1] = task + " [Complete]\n"
        else:
            new_date = input("Enter the new date (or leave blank to keep the current date): ")
            if new_date.strip():
                try:
                    datetime.datetime.strptime(new_date, "%d-%m-%Y")
                    tasks[task_number - 1] = f"{task.split(':')[0]}: {task.split(':')[1]}: {new_date}\n"
                except ValueError:
                    print("Invalid date format. Task not updated.")
                    view_mine()
                    return

            new_username = input("Enter the new user (or leave blank to keep the current user): ")
            if new_username.strip():
                tasks[task_number - 1] = task.replace(task.split(':')[0], new_username)

        with open("tasks.txt", "w") as file:
            file.writelines(tasks)

        print("Task edited successfully.")
        menu(task.split(':')[0])
    else:
        print("No tasks assigned to you.")
    menu(username)

# Function which allows the user to view the stats regarding user and task informations:
def generate_reports():
    # Reads tasks data from tasks.txt.
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()

    total_tasks = len(tasks)
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    current_date = datetime.date.today()

    for task in tasks:
        if "[Complete]" in task:
            completed_tasks += 1
        else:
            incomplete_tasks += 1
            task_info = task.strip().split(" - ")
            if len(task_info) < 4:
                print("Error: Task information is incomplete.")
                return

            task_due_date = datetime.datetime.strptime(task_info[3], "%d-%m-%Y").date()
            if task_due_date < current_date:
                overdue_tasks += 1

    # Generate task_overview.txt report
    with open("task_overview.txt", "w") as task_file:
        task_file.write(f"Total tasks: {total_tasks}\n")
        task_file.write(f"Completed tasks: {completed_tasks}\n")
        task_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        task_file.write(f"Incomplete + Overdue tasks: {incomplete_tasks + overdue_tasks}\n")
        task_file.write(f"Percentage of incomplete tasks: {incomplete_tasks / total_tasks * 100:.2f}%\n")
        task_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

    # Read users data from user.txt
    with open("user.txt", "r") as user_file:
        users = user_file.readlines()

    user_count = len(users)
    with open("user_overview.txt", "w") as user_file:
        user_file.write(f"Total users registered: {user_count}\n")
        for user in users:
            username = user.strip().split(':')[0]
            assigned_tasks = sum(1 for task in tasks if task.startswith(username))
            completed_assigned_tasks = sum(1 for task in tasks if task.startswith(username) and "[Complete]" in task)
            incomplete_assigned_tasks = assigned_tasks - completed_assigned_tasks

            # Calculates the percentages of assigned and completed tasks
            percentage_assigned = assigned_tasks / total_tasks * 100
            percentage_completed = completed_assigned_tasks / assigned_tasks * 100 if assigned_tasks > 0 else 0
            percentage_incomplete = 100 - percentage_completed

            # Find overdue tasks for the user
            overdue_assigned_tasks = sum(1 for task in tasks if task.startswith(username)
                                         and "[Complete]" not in task
                                         and datetime.datetime.strptime(task.strip().split(" - ")[3], "%d-%m-%Y").date() < current_date)

            user_file.write(f"\nUser: {username}\n")
            user_file.write(f"Assigned tasks: {assigned_tasks}\n")
            user_file.write(f"Percentage of total assigned tasks: {percentage_assigned:.2f}%\n")
            user_file.write(f"Percentage of completed tasks: {percentage_completed:.2f}%\n")
            user_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
            user_file.write(f"Overdue tasks: {overdue_assigned_tasks}\n")

    print("Reports generated successfully.")
    menu("admin")

# Function which displays the generated reports to the user/admin:
def display_stats():
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Reports have not been generated yet. Please generate the reports first.")
        return
    
    with open("task_overview.txt", "r") as task_file:
        task_stats = task_file.read()

    with open("user_overview.txt", "r") as user_file:
        user_stats = user_file.read()

    print("---- Task Statistics ----")
    print(task_stats)
    print("---- User Statistics ----")
    print(user_stats)
    menu("admin")

# Function which displays a message when user chooses to quit the task manager:
def quit_programme():
    print("You have chosen to quit the application. Thank you for using 'Task Manager!'")

def menu(curr_user):
    print("\n---- Task Manager ----")
    print('''Register User ('r')
Add Task ('a')
View All Tasks ('va')
View My Tasks ('vm')
Generate Reports ('gr')
Display Statistics ('ds')
Quit ('q')''')

    user_choice = input("\nPlease enter your choice: ")

    if user_choice == 'r':
        reg_user()
    elif user_choice == 'a':
        add_task()
    elif user_choice == 'va':
        view_all()
        menu(curr_user)
    elif user_choice == 'vm':
        view_mine()
        menu(curr_user)
    elif user_choice == 'gr':
        if is_admin(curr_user):
            generate_reports()
        else:
            print("Access denied. Only the admin can generate reports.")
            menu(curr_user)
    elif user_choice == 'ds':
        if is_admin(curr_user):
            display_stats()
        else:
            print("Access denied. Only the admin can display statistics.")
            menu(curr_user)
    elif user_choice == 'q':
        quit_programme()
    else:
        print("Invalid user choice! Please try another option...")
        menu(curr_user)

create_user_file()
login()