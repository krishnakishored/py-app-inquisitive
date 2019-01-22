#
# Connecting to Sqlite
#
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        # conn = sqlite3.connect(':memory:') # it will create a new database that resides in the memory (RAM) instead of a database file on disk.
        # print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
        # conn.close() # do not do it!!
    return None


def create_table(database='./data/sqlite3/inquisitive.db', sql_create_table=''):
    '''
    take db & create table sql as args
    '''
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid # To get back the generated id, we used the  lastrowid attribute of the Cursor object.



def main_insert_tables(database='./data/sqlite3/inquisitive.db',table_name='tbl_deutsch'):
    '''
    insert rows into a specific table(parts of speech) & duplicate them in table_deutsch 
    '''
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)
 
        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
 
        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)

def main_update_task():
    database = './data/sqlite3/demo_crud.db'
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-06',2))

def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))


def delete_all_rows(database,table_name):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_delete_all_rows =  'DELETE FROM ' + table_name
            cur.execute(sql_delete_all_rows)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

def main_delete_tasks():
    database = './data/sqlite3/demo_crud.db'
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        delete_task(conn, 2)
        # delete_all_tasks(conn)


def select_all_rows(database,table_name):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_select_all_rows =  'SELECT * FROM ' + table_name
            cur.execute(sql_select_all_rows)
            rows = cur.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 

def main_select_tasks():
    database = './data/sqlite3/inquisitive.db'
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn,1)
 
        print("2. Query all tasks")
        select_all_tasks(conn)



def insert_table_sub(database, table_name, values):
    """
    Insert a row into the partsofspeech tables (sub tables)
    :param conn:
    :param table_name
    :param values: tuple (german_word,english_word,partsofspeech)
    :return:
    """
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_insert_row =  'INSERT INTO ' + table_name+ '(german_word,english_word,partsofspeech) VALUES(?,?,?)'
            cur.execute(sql_insert_row, values)
            return cur.lastrowid
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")


def populate_db_from_file(filename='./data/german_english.txt',delimiter=':'):
    pass

if __name__ == '__main__':
    database = './data/sqlite3/inquisitive.db'
    table_name = 'tbl_conjunction'

    sql_create_tbl_deutsch = """ CREATE TABLE IF NOT EXISTS tbl_deutsch (
                                        id integer PRIMARY KEY,
                                        german_word text NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text,
                                        frequency integer,
                                        toughness integer
                                    ); """
    
    sql_create_tbl_conjunction = """ CREATE TABLE IF NOT EXISTS tbl_conjunction (
                                        id integer PRIMARY KEY,
                                        german_word text NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text
                                    ); """

    # create_table(database,sql_create_tbl_conjunction)
    # create_table(database,sql_create_tbl_deutsch)

    # value_tuple = ('und','and','conjunction')
    # value_tuple = ('denn','because','conjunction')
    # insert_table_sub(database,table_name, value_tuple)

    # select_all_rows(database,table_name)
    delete_all_rows(database,table_name)
    select_all_rows(database,table_name)
    # main_update_task()
    # main_delete_tasks()
    # main_select_tasks()