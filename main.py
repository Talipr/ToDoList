import sqlite3


def create_table(con):
    """
    creates tables in our db.
    """
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS AllTasks")
        cur.execute("CREATE TABLE IF NOT EXISTS AllTasks(Id INTEGER PRIMARY KEY, Name TEXT, Date DATE)")


def insert_row(con):
    """
    inserts new row to our tasks table.
    """
    task_name = raw_input("please enter the task name for your task list: ")
    task_date = raw_input("please enter date for your task, start with year, month, date, separated by - ")
    print task_name
    print task_date
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO AllTasks (Name, Date) VALUES (?, ?);", (task_name, task_date))
        con.commit()


def delete_task(con):
    """
    deletes some task from our tasks table.
    """
    task_to_be_deleted = raw_input("please enter task name to delete: ")
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM AllTasks WHERE Name = (?)", [task_to_be_deleted])
        con.commit()


def show_all_tasks(con):
    """
    prints all our tasks to do.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM AllTasks;")
        all_rows = cur.fetchall()
        for row in all_rows:
            print row[0]


def main():
    """
    our main project.
    """
    con = sqlite3.connect('tasks.db')
    create_table()
    ACTION_DICT = {1: insert_row, 2: delete_task, 3: show_all_tasks}
    action = 5
    while int(action) != 4:
        action = raw_input('please enter your number action. 1 for adding a new task. 2 for deleting some task.3 for'
                           'showing all tasks. 4 for exit the program. ')
        print ACTION_DICT.get(int(action))(con)


main()