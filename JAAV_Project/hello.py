import pandas
from flask import Flask, render_template, request
app = Flask(__name__)
import mysql.connector

#until a better solution, update these variables before running and before committing
my_user = "awandke2"
my_database = "awandke2_database"
my_password = "Mayaisveryfluffy1!"

@app.route('/')
def home():
   return render_template('index.html', title = "JAAV Final Project")

@app.route('/query', methods=['POST'])
def process_query():
    user_in = (request.form['query_string'])
    test_val = (request.form['test_val'])
    print(test_val)
    
    mydb = mysql.connector.connect(
    host='localhost',
    user=my_user,
    database=my_database,
    password=my_password)
    
    mycursor = mydb.cursor()

    query = "select * from Parks where Parks.ParkName like concat('%%', '%s', '%%')"%user_in.strip()
    print(query)
    mycursor.execute(query)

    for (ParkName, Latitude, Longitude, Size, State) in mycursor:
        print("{}, {}, {}, {}, {}".format(ParkName, Latitude, Longitude, Size, State))

    #df = pandas.read_sql_query(sql)
    mycursor.close()
    mydb.close()

    def make_valid(v):
        if v != v:
            return None
        else:
            return v

    # column_labels = [col for col in df.columns]
    # per_col_values = [
    #     [make_valid(value) for value in df[col]]
    #     for col in df.columns
    # ]

    # response = {
    #     "query_string": sql,
    #     "data": {
    #         "labels": [[col] for col in column_labels],
    #         "values": per_col_values
    #     }
    # }

    # print(response)
    return {}


@app.route('/insert', methods=['POST'])
def process_insert():
    user_in = (request.form['insert_string']).strip()
    print(user_in)

    mydb = mysql.connector.connect(
    host='localhost',
    user=my_user,
    database=my_database,
    password=my_password)
    
    mycursor = mydb.cursor()

    statement = "insert into FavoriteTrails values (fake_username,'%s',1) "%user_in
    print(statement)
    mycursor.execute(statement)

    for (Username, TrailName, Visited) in mycursor:
        print("{}, {}, {}".format(Username, TrailName, Visited))

    #df = pandas.read_sql_query(sql)
    mycursor.close()
    mydb.close()

    def make_valid(v):
        if v != v:
            return None
        else:
            return v
        
    return {}


if __name__ == '__main__':
   app.run()
