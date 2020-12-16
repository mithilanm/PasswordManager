import mysql.connector
import bcrypt
from MasterPassword import *


def password(txt):
    password = txt.encode()

    if bcrypt.checkpw(password, hashed):
        #print("It matches")
        website = input("Enter the name of the site: ")
        database_access(website)
    else:
        print("It does not match!")
        main()


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
            "SELECT username, password FROM password WHERE website='{}'".format(website))

    except:
        print("Something went wrong: {}".format(err))

    myresult = mycursor.fetchall()

    if(myresult == []):
        print("No entry exists for this site! Please try again!")
        main()
    else:
        for x in myresult:
            print("Username: {}".format(x[0]))
            print("Password: {}".format(x[1]))


def main():
    txt = input("Enter password: ")
    password(txt)


main()
