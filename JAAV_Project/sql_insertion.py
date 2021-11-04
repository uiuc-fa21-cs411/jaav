import mysql.connector
import csv 
mydb = mysql.connector.connect(
    host='localhost',
    user='vineetc2',
    database='vineetc2_database',
    password=''
)

with open('/home/vineetc2/data/parks.csv') as csv_file:
    csv_file = csv.reader(csv_file, delimiter= ',')
    all_value = []
    for row in csv_file:
        value = (row[1], row[4], row[5], row[3], row[2])
        all_value.append(value)
    
    all_value.pop(0)

query = "insert into `Parks` values(%s, %s,%s,%s, %s)"


mycursor = mydb.cursor()
mycursor.executemany(query, all_value)
mydb.commit()