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
    print(user_in)
    
    mydb = mysql.connector.connect(
    host='localhost',
    user='awandke2',
    database='awandke2_database',
    password='this_is_not_my_passoword')
    
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




if __name__ == '__main__':
   app.run()
