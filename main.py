import sqlite3 as lite

con = lite.connect('tasks.db')

"""
creates tables in our db.
"""
def create_table():
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE AllTasks(Id INTEGER PRIMARY KEY, Name TEXT)")

"""
inserts new row to our tasks table.
"""
def insert_row():
    task_name = raw_input("please enter the task name for your task list: ")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO AllTasks (Name) VALUES (?);", [task_name])

"""
deletes some task from our tasks table.
"""
def delete_task():
    task_to_be_deleted = raw_input("please enter task name to delete: ")
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM AllTasks WHERE Name = (?)", [task_to_be_deleted])

"""
prints all our tasks to do.
"""
def show_all_tasks():
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM AllTasks;")
        all_rows = cur.fetchall()
        for row in all_rows:
            print row[0]

"""
our main project.
"""
def main():
    create_table()
    action_dic = {1: "insert_row", 2: "delete_task", 3: "show_all_tasks"}
    action = raw_input("""please enter your number action. 1 for adding a new task. 2 for deleting some task.
                       3 for showing all tasks. 4 for exit the program.""")
    while action != 4:
        globals()[action_dic[int(action)]]()
        action = raw_input("enter your next step: ")


main()


