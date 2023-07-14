# Using the task_manager.py file, modify the programme by refactoring the code to ensure readability for devs.

import os   # OS module imported to use alongside the display_statistics function. Source: https://www.tutorialsteacher.com/python/os-module#?utm_content=cmp-true 

# Function to create the 'user.txt' file if it doesn't exist:
def create_user_file():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w"):
            pass

# Function which allows users to login: distinguishing between user admin and regular user:
def login():
    users = {'admin': 'password'}

    username = input("Enter your username: ")
    if username == 'admin':
        password = input("Password: ")
        if username in users and users[username] == password:
            print("Login successful!")
            print("Welcome, admin!")
            menu()
        else:
            print("Invalid username or password. Please try again! ")
            login()
    else:
        print("Welcome, " + username)
        menu()

# Function which determines if user is 'admin', allowing access to 'gr' and 'ds' functions:
def is_admin():
    admin_username = "admin"
    username = input("Enter your username: ")
    return username == admin_username

# Function which registers new users; if the username already exists within the file, an error message prints:
def reg_user():
    username = input("Register your username: ")
    with open("user.txt", "r+") as file:
        if username in file.read():
            print("Username already exists. Please try again.")
            return menu
    with open("user.txt", "a") as file:
        file.write(username + "\n")
    print("User registered successfully.")
    menu()

# Function which allows a user to add new tasks to the .txt file, asking for specific inputs:
def add_task():
    task_user = input("Enter your username: ")
    task_name = input("Enter the task name: ")
    task_description = input("Enter the task description: ")
    task_date = input("Enter the task date: ")
    with open("tasks.txt", "a") as file:
        file.write(f"{task_user}: {task_name} - {task_description} - {task_date}\n")
    print("Task added successfully.")
    menu()

# Function which allows a user to view all the tasks currently in the .txt file:
def view_all():
    with open("tasks.txt", "r+") as file:
        tasks = file.readlines()
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task.strip()}")
        menu()

# Function which allows a user to view assigned tasks in the .txt file, using their provided username.
# Otherwise, an error message appears if the user has not inputted any new tasks:
def view_mine():
    username = input("Enter your username: ")
    with open("user.txt", "r+") as user_file, open("tasks.txt", "r") as tasks_file:
        users = user_file.readlines()
        tasks = tasks_file.readlines()
    assigned_tasks = [task.strip() for user, task in zip(users, tasks) if user.strip() == username]
    if assigned_tasks:
        for i, task in enumerate(assigned_tasks):
            print(f"{i + 1}. {task}")
    else:
        print("No tasks assigned to you.")
        menu()

# Function which allows the user to edit the date of a task if user input == 'no'
def edit_task():
    task_number = int(input("Enter the task number to edit: "))
    with open("tasks.txt", "r+") as file:
        tasks = file.readlines()
    if task_number < 1 or task_number > len(tasks):
        print("Invalid task number.")
        return

    task = tasks[task_number - 1].strip()
    print(f"Selected task: {task}")

    if "[Complete]" in task:
        print("This task is already marked as complete and cannot be edited.")
        edit_task()

    choice = input("Do you want to mark it as complete? (Yes/No) ")
    if choice.lower() == "yes":
        tasks[task_number - 1] = task + " [Complete]\n"
    else:
        new_date = input("Enter the new date (or leave blank to keep the current date): ")
        if new_date.strip():
            tasks[task_number - 1] = new_date + "\n"

        new_username = input("Enter the new user (or leave blank to keep the current user): ")
        if new_username.strip():
            tasks[task_number - 1] = new_username + "\n"

    with open("tasks.txt", "w") as file:
        file.writelines(tasks)
    print("Task edited successfully.")
    menu()

# Function which allows the user to view the stats regarding user and task informations:
def generate_reports():
    with open("tasks.txt", "r+") as tasks_file:
        tasks = tasks_file.readlines()

    total_tasks = len(tasks)
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    for task in tasks:
        if "[Complete]" in task:
            completed_tasks += 1
        else:
            incomplete_tasks += 1
            task_info = task.strip().split(",")
    with open("task_overview.txt", "w") as task_file:
        task_file.write(f"Total tasks: {total_tasks}\n")
        task_file.write(f"Completed tasks: {completed_tasks}\n")
        task_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        task_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_file.write(f"Percentage of incomplete tasks: {incomplete_tasks / total_tasks * 100}%\n")
        task_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100}%\n")
    with open("user.txt", "r+") as user_file:
        users = user_file.readlines()

    user_count = len(users)
    with open("user_overview.txt", "w") as user_file:
        user_file.write(f"Total users registered: {user_count}\n")
        for user in users:
            assigned_tasks = 0
            completed_assigned_tasks = 0
            for task in tasks:
                task_info = task.strip().split(",")
                if user.strip() == task_info[0]:
                    assigned_tasks += 1
                    if "[Complete]" in task:
                        completed_assigned_tasks += 1
            percentage_completed = completed_assigned_tasks / assigned_tasks * 100 if assigned_tasks > 0 else 0
            user_file.write(f"\nUser: {user.strip()}\n")
            user_file.write(f"Assigned tasks: {assigned_tasks}\n")
            user_file.write(f"Percentage of completed tasks: {percentage_completed}%\n")
    print("Reports generated successfully.")
    menu()

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

# Function which displays a message when user chooses to quit the task manager:
def quit_programme():
    print("You have chosen to quit the application. Thank you for using 'Task Manager'!")

def menu():
    print("\n---- Task Manager ----")
    print('''1. Register User ('r')
2. Add Task ('a')
3. View All Tasks ('va')
4. View My Tasks ('vm')
5. Edit Task ('et')
6. Generate Reports ('gr')
7. Display Statistics ('ds')
8. Quit ('q')''')

    user_choice = input("\nPlease enter your choice: ")
    if user_choice == 'r':
        reg_user()
    elif user_choice == 'a':
        add_task()
    elif user_choice == 'va':
        view_all()
    elif user_choice == 'vm':
        view_mine()
    elif user_choice == 'et':
        edit_task()
    elif user_choice == 'gr':
        if is_admin():
            generate_reports()
        else:
            print("Access denied. Only the admin can generate reports.")
            menu()
    elif user_choice == 'ds':
        if is_admin():
            display_stats()
        else:
            print("Access denied. Only the admin can display statistics.")
            menu()
    elif user_choice == 'q':
        quit_programme()
    else:
        print("Invalid user choice! Please try another option...")

create_user_file()
login()