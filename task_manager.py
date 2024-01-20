# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def update_tasks():
    '''Updates the 'tasks.txt' file when tasks are added/edited.'''
    with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))


def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        with open("user.txt", "w") as out_file:
            # - Request input of a new username
            new_username = input("New Username: ")

            # - Check if the username already exists and restart loop if it does.
            if new_username in username_password.keys():
                print("User already exists. Please use a different username.")
                break

            # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")
            
            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password
            # - Otherwise restart the loop to try again.
            else:
                print("Passwords do no match. Please try again.")
                break

            # If checks passed, add new user to user list.
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
            exit()


def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    else:    
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    update_tasks()
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    task_num = 1
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"\t --- Task {task_num}: ---\n"
            disp_str += f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            t_status = "Yes" if t['completed'] == True else "No"
            disp_str += f"Task Completed: \t {t_status}\n"
            print(disp_str)
            task_num += 1

    # Loop through choices for user to edit the task.
    editing = True        
    while editing:
        task_choice = int(input("To select a task please enter the task's number, or enter '-1' to return to the main menu: "))
        if task_choice == -1:
            break
        else:
            # For each task loop through to check if assigned to curr_user.
            counter = 0
            for t in task_list:
                if t['username'] == curr_user:
                    counter += 1
                    if counter == task_choice:
                        task_option = input("To edit the task please enter 'e'.\nTo mark the task as complete please enter 'c'.\n: ").lower()
                        if task_option == 'c':
                            t['completed'] = True
                            print("Task has been updated.")
                        # If user selects 'e' and the task is not completed then ask if they want to assign a new user or change the due date.
                        elif task_option == 'e' and t['completed'] is False:
                            new_user = input("Do you want to change the user assigned to the task? Enter the new user, otherwise enter 'n': ")
                            if new_user == 'n':
                                pass
                            elif new_user not in username_password.keys():
                                print("User does not exist. Please enter a valid username")
                                break
                            elif new_user == curr_user:
                                print("You are already assigned to the task.")
                                break
                            elif new_user in username_password.keys() and new_user != curr_user:
                                t['username'] = new_user
                                print("Task has been updated.")
                            while True:
                                new_date = input("Do you want to change the due date of the task? Enter the new date (YYYY-MM-DD), otherwise enter 'n': ")
                                if new_date == 'n':
                                    break
                                # Check to ensure date is input in correct format, loops until correct.
                                else:
                                    try:
                                        t['due_date'] = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                                        print("Task has been updated.")
                                        break
                                    except ValueError:
                                        print("Invalid datetime format. Please use the format specified")

                        elif task_option == 'e':
                            print("Task has already been completed.")
                            editing = False
                            break
                        else:
                            print("Incorrect selection, please try again.")
                            break
                        # Tasks are updated by calling function.
                        update_tasks()
                        return
                        
def generate_report():
    '''Calculating data for overview reports and creating the 'task_overview.txt' and 'user_overview.txt' files.'''
    curr_date = date.today()
    task_data = {'total_tasks': 0, 'completed': 0, 'overdue': 0}
    # Defining disp_str to store the User overview report.
    disp_str = "\t --- User Overview Report ---\n"
    disp_str += f"Generated on: {curr_date}\n"
    disp_str += f"Total number of users registered: {len(username_password)}\n"
    disp_str += f"Total number of tasks in task manager: {len(task_list)}\n\n"
    # Loop through each user to gather the data required for each to add to report.
    for user in username_password.keys():
        user_task_data = {'total_tasks': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0, 'percent_incomplete': 0, 'percent_overdue': 0}
        for t in task_list:
            if t['username'] == user:
                user_task_data['total_tasks'] += 1
                if t['completed'] == True:
                    user_task_data['completed'] += 1
                elif t['due_date'].strftime(DATETIME_STRING_FORMAT) > curr_date.strftime(DATETIME_STRING_FORMAT):
                    user_task_data["overdue"] += 1

        user_task_data['incomplete'] = user_task_data['total_tasks'] - user_task_data['completed']
        user_task_data['percent_incomplete'] = round(user_task_data['incomplete'] / user_task_data['total_tasks'] * 100) if user_task_data['total_tasks'] > 0 else 0
        user_task_data['percent_overdue'] = round(user_task_data['overdue'] / user_task_data['total_tasks'] * 100) if user_task_data['total_tasks'] > 0 else 0

        disp_str += f"\t --- Report for {user}: ---\n"
        disp_str += f"Total number of tasks for this user: {user_task_data['total_tasks']}\n"
        disp_str += f"Total number of completed tasks: {user_task_data['completed']}\n"
        disp_str += f"Total number of incomplete tasks: {user_task_data['incomplete']}\n"
        disp_str += f"Total number of overdue tasks: {user_task_data['overdue']}\n"
        disp_str += f"Percentage of tasks that are incomplete: {user_task_data['percent_incomplete']}%\n"
        disp_str += f"Percentage of tasks that are overdue: {user_task_data['percent_overdue']}%\n\n"

        # Adds user data into 'task_data' dictionary to sum up data for task overview report.
        task_data['total_tasks'] += user_task_data['total_tasks']
        task_data['completed'] += user_task_data['completed']
        task_data['overdue'] += user_task_data['overdue']

    # Adds/overwrites user overview report text file with the disp_str string.
    with open("user_overview.txt", "w") as u_rep:
        u_rep.write(disp_str)
    
    # Calculates data on tasks using the task_data dictionary.
    t_incomplete = task_data['total_tasks'] - task_data['completed']
    percent_incomplete = round(t_incomplete / task_data['total_tasks'] * 100)
    percent_overdue = round(task_data['overdue'] / task_data['total_tasks'] * 100)
    
    # Defines new disp_str for task overview report.
    disp_str = "\t --- Task Overview Report ---\n"
    disp_str += f"Generated on: {curr_date}\n"
    disp_str += f"Total number of tasks in task manager: {task_data['total_tasks']}\n"
    disp_str += f"Total number of completed tasks: {task_data['completed']}\n"
    disp_str += f"Total number of incomplete tasks: {t_incomplete}\n"
    disp_str += f"Total number of overdue tasks: {task_data['overdue']}\n"
    disp_str += f"Percentage of tasks that are incomplete: {percent_incomplete}%\n"
    disp_str += f"Percentage of tasks that are overdue: {percent_overdue}%\n"
    
    # Adds/overwrites task overview report text file
    with open("task_overview.txt", "w") as t_rep:
        t_rep.write(disp_str)

def display_stats():
    '''Read data from task and user overview reports and displays the data in the console for user.'''
    with open("task_overview.txt", 'r') as task_file:
        print(task_file.read())

    with open("user_overview.txt", 'r') as user_file:
        print(user_file.read())
    
# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()   
    
    elif menu == 'gr':
        generate_report()
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        # Checking if user and task overview reports exists, if not then the reports are produced.
        if not os.path.exists("user_overview.txt" and "task_overview.txt"):
            generate_report()
        
        display_stats()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please try again")