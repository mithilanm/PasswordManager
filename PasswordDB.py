import mysql.connector
import bcrypt
import sys
import getpass
from MasterPassword import *


def ask():
    again = 'default'
    while again not in ['Y', 'N']:
        again = input("Again? (Y or N) ")
        if(again not in ['Y', 'N']):
            print("Please enter either Y or N")
    if(again == 'Y'):
        main()
    else:
        sys.exit()


def password(txt):
    password = txt.encode()

    if bcrypt.checkpw(password, hashed):
        #print("It matches")
        return True
    else:
        print("It does not match!")
        return False


def database_access():
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )
        website = input("Enter the name of the site: ")
        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT username, password FROM password WHERE website='{}'".format(website.lower()))
        myresult = mycursor.fetchall()
        mydb.close()
    except:
        print("Something went wrong: {}".format(err))

    if(myresult == []):
        print("No entry exists for this site! Please try again!")
        ask()
    else:
        for x in myresult:
            print("Username: {}".format(x[0]))
            print("Password: {}".format(x[1]))
        ask()


def database_insert():
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )

        your_wesbite = input("Enter the site: ")
        your_username = input("Enter the username: ")
        your_password = input("Enter the password: ")
        mycursor = mydb.cursor()

        sql = "INSERT INTO password (website,username,password) VALUES (%s, %s, %s)"
        values = (your_wesbite.lower(), your_username, your_password)
        mycursor.execute(sql, values)

        mydb.commit()

        print(mycursor.rowcount, "record inserted")
        ask()
    except:
        print("Something went wrong: {}".format(err))


def database_update():
    pass


def datbase_delete():
    pass


def main():
    ans = False
    choice = 'wrong'
    while ans == False:
        #txt = input("Enter password: ")
        txt = getpass.getpass()
        ans = password(txt)

    while(choice not in ['E', 'I']):
        choice = input(
            "Would you like to access an entry (E) or insert an entry (I)? ")
        if(choice not in ['E', 'I']):
            print("Please enter either E or I!")

    if(choice == 'E'):
        database_access()

    elif(choice == 'I'):
        database_insert()


main()
