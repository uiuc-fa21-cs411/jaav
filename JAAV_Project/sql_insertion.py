import mysql.connector
import csv 
mydb = mysql.connector.connect(
    host='localhost',
    user='awandke2',
    database='awandke2_database',
    password='this_is_my_password:)'
)

# Numbers to use to get the correct data into the tables
#Parks: row[1], row[4], row[5], row[3], row[2]
#Trails: row[1], row[2], row[9], row[8], row[7]
#Species: row[0], row[1], row[2]
#ParkBiodiveristy: row[0], row[1], row[2]
#Campsites: row[1], row[0], row[3], row[2]

#max_len = 255
with open('../data/parks.csv') as csv_file:
    csv_file = csv.reader(csv_file, delimiter= ',')
    all_value = []
    for row in csv_file:
        # this is a fix for the Species table problem, truncates Common names to 255 characters 
        #if (len(row[1]) > max_len):
        #  row[1] = (row[1])[0:max_len:1]
        value = (row[1], row[4], row[5], row[3], row[2])
        all_value.append(value)
    
    all_value.pop(0)

query = "insert into `Parks` values(%s, %s, %s, %s, %s)"


mycursor = mydb.cursor()
mycursor.executemany(query, all_value)
mydb.commit()