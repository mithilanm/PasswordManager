import sys
import getpass
import secrets
import mysql.connector
import bcrypt
from MasterPassword import *


def ask():
    again = ''
    while again not in ['Y', 'N']:
        again = input("Again? (Y or N) ")
        if(again not in ['Y', 'N']):
            print("Please enter either Y or N")
    if again == 'Y':
        main()
    else:
        sys.exit()


def check_password(txt):
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
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    if myresult == []:
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

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    for data in myresult:
        print("Username: {}".format(data[0]))
        print("Password: {}".format(data[1]))
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
        choice = ''
        length = ''
        while choice not in ['G', 'E']:
            choice = input(
                "Would you like to enter a password (E) or generate one for entry (G)? ")
            if choice not in ['G', 'E']:
                print("Please enter G or E")

        if choice == 'G':
            while not length.isnumeric():
                length = input(
                    "How long does the password have to be. Please enter a number: ")
                if not length.isnumeric():
                    print("Please enter a number!")
            your_password = gen_password(int(length))
            print("The generated password is: {}".format(your_password))

        elif choice == 'E':
            your_password = input("Enter the password: ")

        mycursor = mydb.cursor()

        sql = "INSERT INTO password (website,username,password) VALUES (%s, %s, %s)"
        values = (website.lower(), your_username, your_password)
        mycursor.execute(sql, values)

        mydb.commit()

        print(mycursor.rowcount, "record inserted")
        mydb.close()

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    ask()


def gen_password(length):
    password = secrets.token_urlsafe(length)
    return password


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
                "Would you like to update the username, password or both?")
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

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    ask()


def database_delete(website):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwordname,
            database=databasename
        )

        mycursor = mydb.cursor()

        sql = "DELETE FROM password WHERE (website = '{}' AND id <> 0)".format(
            website.lower())
        mycursor.execute(sql)

        mydb.commit()

        print(mycursor.rowcount, "record deleted")
        mydb.close()

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    ask()


def main():
    ans = False
    choice = ''
    ask1 = ''
    ask2 = ''
    while ans == False:
        # txt = input("Enter password: ")
        txt = getpass.getpass()
        ans = check_password(txt)

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
        if ask1 == 'Y':
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
        if ask2 == 'Y':
            database_insert(your_website)
        else:
            ask()

    elif(choice == 'D' and database_check(your_website)):
        database_delete(your_website)

    elif(choice == 'D' and not database_check(your_website)):
        print("No entry exists for this site to delete. Please try again!")
        ask()


main()
