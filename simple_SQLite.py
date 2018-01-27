import sqlite3

import traceback

db_name = 'chainsaw.db'

def main():

    while True:
        choice = get_choice()
        if choice == 'q':
            break
        if choice == '1':
            add_new()
        if choice == '2':
            show_all()
        if choice == '3':
            delete_record()
        if choice == '4':
            update_record()
        if choice == '5':
            search_record_by_name()

def add_new():

    # get new data, call method to add to DB

    name = input('Enter name: ')
    '''check if user enters the correct datatype'''
    while True:
        try:
            catches = int(input('Enter catches: '))
            break
        except ValueError:
            print('Catches must be an Integer.')

    country = input('Enter country: ')
    #add user entries to database
    add_to_db(name, country, catches)
def add_to_db(name, country, catches):

    """ todo connect to db, insert data, handle errors """
    try:
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            create_table()
            cur.execute('insert into chainsaw values (?,?,?)', (name, country, catches))
    except sqlite3.Error as er:
        print('Changes being rolled back because of error:', er)
        traceback.print_exc()
        db.rollback()

def create_table():
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute('create table if not exists chainsaw ("Chainsaw Juggling Record Holder" text, Country text, "Number of catches" int)')
def show_all():

    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        for r in cur.execute('select * from chainsaw'):
            print('Juggler\'s name:\t\t\t' + r[0]) # todo nice formatting
            print('Country:\t\t\t' + r[1])
            print('Number of catches:\t\t'+str(r[2]))
            print()


def delete_record():
    try:
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            print('Enter the options to delete: 1 = By name, 2 = By Country, 3 = catches.')
            while True:
                try:
                    user_option = int(input('Enter your choice: '))
                    if(user_option == 1):
                        delete_choice = input('Enter the name: ')
                        sql = 'Delete from chainsaw where "Chainsaw Juggling Record Holder" = ?'
                        cur.execute(sql, (delete_choice,))
                        print('Data successfully deleted.')
                        break
                    elif(user_option == 2):
                        delete_choice = input('Enter the country: ')
                        sql = 'Delete from chainsaw where Country = ?'
                        cur.execute(sql,(delete_choice,))
                        print('Data successfully deleted.')
                        break
                    elif(user_option == 3):
                        delete_choice = input('Enter the catches: ')
                        sql = 'Delete from chainsaw where "Number of catches" = ?'
                        cur.execute(sql, (delete_choice,))
                        print('Data successfully deleted.')
                        break
                    else:
                        print('Please enter the correct choice.')
                except ValueError:
                    print('user_option must be an integer.')
    except sqlite3.Error as er:
        print('Rolling back changes due to error', er)
        traceback.print_exc()
        db.rollback()


def search_record_by_name():
    db = sqlite3.connect(db_name)
    cur = db.cursor()
    search_name = input('Enter name: ')
    sql = 'SELECT * FROM chainsaw WHERE "Chainsaw Juggling Record Holder" = ?'
    cur.execute(sql, (search_name,))
    for row in cur:
        print(row)

def update_record():
    try:
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            update_name = input('Enter the name: ')
            update_catches_record = int(input('Enter the new number of catches: '))
            sql = 'UPDATE chainsaw SET "Number of catches" = ? WHERE "Chainsaw Juggling Record Holder" = ?'
            cur.execute(sql,(update_catches_record,update_name))
    except sqlite3.Error as error:
        print('Rolling back changes due to error', error)
        traceback.print_exc()
        db.rollback()

def get_choice():

    print('''

    Press 1 to add new record

    Press 2 to show all records

    Press 3 to delete record

    Press 4 to edit record

    press 5 to search (by name)

    Press q to quit program

    ''')

    return input('Enter choice: ')  # validation useful here.

if __name__ == '__main__':

    main()
