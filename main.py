import sqlite3
import Settings


def create_table(con):
    """
    creates tables in our db.
    """
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS all_tasks(Id INTEGER PRIMARY KEY, Name TEXT, Priority INTEGER, "
                    "Done INTEGER, Date DATE)")
        cur.execute("CREATE TABLE IF NOT EXISTS categories(Id INTEGER PRIMARY KEY, Name TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS tasks_to_categories(Task_id INTEGER , Category_id INTEGER)")


def insert_row(con):
    """
    inserts new row to our tasks table.
    """
    task_name = raw_input("please enter the task name for your task list: ")
    task_date = raw_input("please enter date for your task, start with year, month, date, separated by - ")
    task_priority = int(raw_input("please enter the priority of your task, number between 1 to 10 "))
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO all_tasks (Name, Priority, Done, Date) VALUES (?, ?, 0, ?);", (task_name, task_priority
                                                                                                , task_date))
        con.commit()
        category_name = raw_input("please enter the category of your task. if you have more than one, enter one by one."
                                  " to end, enter the word \"done\": ")
        while category_name != "done":
            insert_task_to_category(task_name, category_name, con)
            category_name = raw_input("enter next category or \"done\" to finish: ")


def get_id(db_name, item_name, con):
    """
    gets item for finding it id.
    :param db_name
    :param item_name
    :param con: connection to the db.
    :return: id of the item.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM {db} WHERE Name = \"{value}\";".format(db=db_name, value=item_name))
        results = cur.fetchall()
        return results


def insert_task_to_category(task_name, category_name, con):
    """
    gets task and category, and insert it to tasks_to_categories table.
    :param task_name
    :param category_name
    :param con: connection to the db.
    """
    task_id = get_id("all_tasks", task_name, con)
    category_id = get_id("categories", category_name, con)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO tasks_to_categories (Task_id, Category_id) VALUES (?, ?);", (int(task_id[0][0]),
                                                                                              int(category_id[0][0])))
        con.commit()


def delete_task(con):
    """
    deletes some task from our tasks table.
    """
    task_to_be_deleted = raw_input("please enter task name to delete: ")
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM all_tasks WHERE Name = (?)", [task_to_be_deleted])
        con.commit()
        print "The task {name} has been deleted".format(name=task_to_be_deleted)


def show_all_tasks(con):
    """
    prints all our tasks to do.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM all_tasks;")
        all_rows = cur.fetchall()
        task_id = 1
        for row in all_rows:
            print "task number {id}: {name}".format(id=task_id, name=row[0])
            task_id += 1


def update_status(con):
    """
    updates task to be done.
    """
    task_name_to_be_updates = raw_input("please enter the task name to update: ")
    with con:
        cur = con.cursor()
        cur.execute("UPDATE all_tasks SET Done=? WHERE Name=?", (1, task_name_to_be_updates))
        con.commit()


def insert_categories(con):
    """
    insert all categories from setting file.
    """
    for category in Settings.Categories:
        cur = con.cursor()
        cur.execute("INSERT INTO categories (Name) VALUES (?)", (category,))
    con.commit()


def main():
    """
    our main project.
    """
    con = sqlite3.connect(r"D:\Main Documents\PycharmProjects\ToDoList\tasks.db")
    create_table(con)
    insert_categories(con)
    ACTION_DICT = {1: insert_row, 2: delete_task, 3: show_all_tasks, 4: update_status}
    action = -1
    while int(action) != 5:
        action = int(raw_input('please enter your number action. 1 for adding a new task. 2 for deleting some task.3 '
                               ' for showing all tasks. 4 for updating task\'s status. 5 for exiting the program. '))
        if action in ACTION_DICT:
            ACTION_DICT.get(action)(con)


main()