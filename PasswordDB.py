import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="firstdash"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM login")

myresult=mycursor.fetchall()

for x in myresult:
    print(x)
