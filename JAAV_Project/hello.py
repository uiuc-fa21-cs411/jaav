import pandas
from flask import Flask, render_template, request
app = Flask(__name__)
import mysql.connector

@app.route('/')
def home():
   return render_template('index.html', title = "JAAV Final Project")

@app.route('/query', methods=['POST'])
def process_query():
    user_in = (request.form['query_string'])
    select_q1 = (request.form['select_query_1'])
    select_q2 = (request.form['select_query_2'])

    print(select_q1)
    print(select_q2)
    print(user_in)
    
    mydb = mysql.connector.connect(
    host='localhost',
    user='awandke2',
    database='awandke2_database',
    password='')
    
    mycursor = mydb.cursor()

    if select_q1 == 1:
        query = "SELECT *, count(ParkBiodiversity.Biodiversity) AS NativeCount FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park WHERE Parks.ParkName like concat('%%', '%s', '%%') and ParkBiodiversity.Nativeness = 'Native' GROUP BY ParkName ORDER BY NativeCount desc;"%user_in.strip()
    elif select_q2 == 1:
        query = "select * from Parks where Parks.ParkName like concat('%%', '%s', '%%')"%user_in.strip()
    else:
        query = "select * from Parks where Parks.ParkName like concat('%%', '%s', '%%')"%user_in.strip()

    print(query)
    mycursor.execute(query)

    for (ParkName, Latitude, Longitude, Size, State) in mycursor:
        print("{}, {}, {}, {}, {}".format(ParkName, Latitude, Longitude, Size, State))

    df = pandas.read_sql_query(query, mydb)
    print(df)
    mycursor.close()
    mydb.close()

    def make_valid(v):
        if v != v:
            return None
        else:
            return v

    column_labels = [col for col in df.columns]
    per_col_values = [
        [make_valid(value) for value in df[col]]
        for col in df.columns
    ]

    response = {
        "query_string": query,
        "data": {
            "labels": [[col] for col in column_labels],
            "values": per_col_values
        }
    }

    print(response)
    return response




if __name__ == '__main__':
   app.run()