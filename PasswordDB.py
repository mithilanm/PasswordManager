import mysql.connector
import bcrypt
import sys
import getpass
from MasterPassword import *


def ask():
    again = ''
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
        # print("It matches")
        return True
    else:
        print("It does not match!")
        return False


def database_check(website):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )
        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM password WHERE website='{}'".format(website.lower()))
        myresult = mycursor.fetchall()
        mydb.close()
    except:
        print("Something went wrong: {}".format(err))

    if(myresult == []):
        return False
    else:
        return True


def database_access(website):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )
        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT username, password FROM password WHERE website='{}'".format(website.lower()))
        myresult = mycursor.fetchall()
        mydb.close()

    except:
        print("Something went wrong: {}".format(err))

    for x in myresult:
        print("Username: {}".format(x[0]))
        print("Password: {}".format(x[1]))
    ask()


def database_insert(website):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )

        your_username = input("Enter the username: ")
        your_password = input("Enter the password: ")
        mycursor = mydb.cursor()

        sql = "INSERT INTO password (website,username,password) VALUES (%s, %s, %s)"
        values = (website.lower(), your_username, your_password)
        mycursor.execute(sql, values)

        mydb.commit()

        print(mycursor.rowcount, "record inserted")
        mydb.close()

    except:
        print("Something went wrong: {}".format(err))

    ask()


def database_update(website):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )
        choice = ""
        while choice not in ['username', 'password', 'both']:
            choice = input(
                "Would you like to update the username, password or both? (Enter username, password or both) ")
            if choice not in ['username', 'password', 'both']:
                print("Please enter username, password or both!")
        if choice == 'username':
            your_username = input("Enter the new username: ")
            sql = "UPDATE password SET username = (%s) WHERE website = (%s)"
            values = (your_username, website.lower())
        elif choice == 'password':
            your_password = input("Enter the new password: ")
            sql = "UPDATE password SET password = (%s) WHERE website = (%s)"
            values = (your_password, website.lower())
        else:
            your_username = input("Enter the new username: ")
            your_password = input("Enter the new password: ")
            sql = "UPDATE password SET username = (%s), password = (%s) WHERE website = (%s)"
            values = (your_username, your_password, website.lower())

        mycursor = mydb.cursor()

        mycursor.execute(sql, values)

        mydb.commit()

        print(mycursor.rowcount, "record updated")
        mydb.close()

    except:
        print("Something went wrong: {}".format(err))

    ask()


def database_delete(website):
    pass


def main():
    ans = False
    choice = ''
    ask1 = ''
    ask2 = ''
    while ans == False:
        # txt = input("Enter password: ")
        txt = getpass.getpass()
        ans = password(txt)

    while(choice not in ['E', 'I', 'U', 'D']):
        choice = input(
            "Would you like to access an entry (E), insert an entry (I), update an entry (U) or delete an entry(D)? ")
        if(choice not in ['E', 'I', 'U', 'D']):
            print("Please enter either E, I, U or D!")

    your_website = input("Enter the site: ")

    if(choice == 'E' and database_check(your_website)):
        database_access(your_website)

    elif(choice == 'E' and not database_check(your_website)):
        print("No entry exists for this site! Please try again!")
        ask()

    elif(choice == 'I' and not database_check(your_website)):
        database_insert(your_website)

    elif(choice == 'I' and database_check(your_website)):
        while(ask1 not in ['Y', 'N']):
            ask1 = input(
                "This entry already exists. Would you like to update it instead? (Y or N) ")
            if(ask1 not in ['Y', 'N']):
                print("Please enter either Y or N")
        if(ask1 == 'Y'):
            database_update(your_website)
        else:
            ask()

    elif(choice == 'U' and database_check(your_website)):
        database_update(your_website)

    elif(choice == 'U' and not database_check(your_website)):
        while(ask2 not in ['Y', 'N']):
            ask2 = input(
                "This entry does not exist. Would you like to insert it instead? (Y or N) ")
            if(ask2 not in ['Y', 'N']):
                print("Please enter either Y or N")
        if(ask2 == 'Y'):
            database_insert(your_website)
        else:
            ask()

    elif(choice == 'D'):
        database_delete(your_website)


main()
