import mysql.connector
import csv 
mydb = mysql.connector.connect(
    host='localhost',
    user='jananir2',
    database='jananir2_database',
    password='Mseq131640!'
)

with open('../data/species.csv') as csv_file:
    csv_file = csv.reader(csv_file, delimiter= ',')
    all_value = []
    for row in csv_file:
        value = (row[0], row[1], row[2])
        all_value.append(value)
    
    all_value.pop(0)

query = "insert into `Species` values(%s, %s,%s)"


mycursor = mydb.cursor()
mycursor.executemany(query, all_value)
mydb.commit()