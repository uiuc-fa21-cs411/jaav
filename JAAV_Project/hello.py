import pandas
from flask import Flask, render_template, request
app = Flask(__name__)
import mysql.connector

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/def')
def signin1():
    return render_template('signin.html')

@app.route('/info')
def home():
   return render_template('home.html', title = "JAAV Final Project")

@app.route('/ftrails')
def favtr():
    return render_template('favtrails.html', title = "Favorite Trails")

@app.route('/info/query', methods=['POST'])
def process_query():
    user_in = (request.form['query_string']).strip()
    select_q1 = (request.form['select_query_1']).strip()
    select_q2 = (request.form['select_query_2']).strip()
    #print(request.form)
    username_in = (request.form['update_fav_trail_usrnm']).strip()
    trailname_in = (request.form['update_fav_trail_trlnm']).strip()
    custom_query = (request.form['custom_query']).strip()
    del_user = (request.form["del_user"]).strip()
    del_trail = (request.form["del_trail"]).strip()
    create_user = request.form["create_user"].strip()
    create_pass = request.form["create_pass"].strip()
    add_trail_user = request.form["add_trail_user"].strip()
    add_trail_name = request.form["add_trail_name"].strip()
    # print(type(select_q1))
    # print(select_q2)
  

    mydb = mysql.connector.connect(
    host='localhost',
    user='awangoo2',
    database='awangoo2_database',
    password='Abhsav2020!')
    
    mycursor = mydb.cursor()

    query = ''
    # runs general parks query modified by q1 and/or q2
    if user_in != '':
        query = "select * from Parks where Parks.ParkName like concat('%%', '%s', '%%')"%user_in
        if select_q1 == "1" and select_q2 != "1":
          query = "SELECT Parks.ParkName, Parks.Latitude, Parks.Longitude, Parks.Size, Parks.State, count(ParkBiodiversity.Biodiversity) AS NativeCount FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park WHERE ParkBiodiversity.Nativeness = 'Native' and Parks.ParkName like concat('%%', '%s', '%%') GROUP BY ParkName ORDER BY NativeCount desc"%user_in
        elif select_q2 == "1" and select_q1 != "1":
          query = "SELECT * FROM(SELECT AVG(Trails.Popularity) as longTrailPopularity, Trails.ParkName FROM Trails inner join Parks on Trails.ParkName = Parks.ParkName WHERE Parks.ParkName like concat('%%', '%s', '%%') and Trails.Length >= (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q1 NATURAL JOIN (SELECT AVG(Trails.Popularity) as ShortTrailPopularity, Trails.ParkName FROM Trails WHERE  Trails.Length < (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q2 NATURAL JOIN Parks;"%user_in
        elif select_q1 == "1" and select_q2 == "1":
          query = "SELECT * FROM(SELECT AVG(Trails.Popularity) as longTrailPopularity, Trails.ParkName FROM Trails inner join Parks on Trails.ParkName = Parks.ParkName WHERE Parks.ParkName like concat('%%', '%s', '%%') and Trails.Length >= (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q1 NATURAL JOIN (SELECT AVG(Trails.Popularity) as ShortTrailPopularity, Trails.ParkName FROM Trails WHERE  Trails.Length < (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q2 NATURAL JOIN (SELECT Parks.ParkName, count(ParkBiodiversity.Biodiversity) AS NativeCount FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park WHERE ParkBiodiversity.Nativeness = 'Native' GROUP BY ParkName) as q3 NATURAL JOIN Parks;"%user_in
        
    # runs just native count query
    elif select_q1 == "1":
        query = "SELECT Parks.ParkName, count(ParkBiodiversity.Biodiversity) AS NativeCount FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park WHERE ParkBiodiversity.Nativeness = 'Native' GROUP BY ParkName ORDER BY NativeCount desc;"    
    # runs just trail popularity query
    elif select_q2 == "1":
        query = "SELECT * FROM(SELECT AVG(Trails.Popularity) as longTrailPopularity, Trails.ParkName FROM Trails WHERE Trails.Length >= (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q1 NATURAL JOIN (SELECT AVG(Trails.Popularity) as ShortTrailPopularity, Trails.ParkName FROM Trails WHERE Trails.Length < (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q2;"
    # Add or delete a user
    elif create_user != '' and create_pass != '':
      if del_user == "1":
        delete_query = "delete from FavoriteTrails where Username = '%s'"%create_user
        print(delete_query)
        mycursor.execute(delete_query)
        mydb.commit()
        delete_query = "delete from Users where Username = '%s'"%create_user
        print(delete_query)
        mycursor.execute(delete_query)
        mydb.commit()
      else :
        insert_query = "insert into Users values('%s', '%s')"%(create_user, create_pass)
        print(insert_query)
        mycursor.execute(insert_query)
      mydb.commit()
      query =  "select * from Users"
    # Add or delete a favorite trail
    elif add_trail_user != '' and add_trail_name != '':
      if del_trail == "1":
        delete_query = "delete from FavoriteTrails where Username = '%s' and TrailName = '%s'"%(add_trail_user, add_trail_name)
        mycursor.execute(delete_query)
      else :
        insert_query = "insert into FavoriteTrails values('%s', '%s', 0)"%(add_trail_user, add_trail_name)
        mycursor.execute(insert_query)
      mydb.commit()  
      query = "select * from FavoriteTrails where Username like concat('%%', '%s', '%%')"%add_trail_user
    # this will execute any sql query, useful for debugging
    elif custom_query != '':
        if ("select" in custom_query.lower()):
          query = custom_query
        else:
          mycursor.execute(custom_query)
          mydb.commit()
          query = ''    
    # Update FavoriteTrails table's Visited field to 1 instead of 0 to mark as visited for specified user
    else:
        update_query = "update FavoriteTrails set Visited = 1 where TrailName = '" + trailname_in + "' and Username = '" + username_in + "'"
        print (update_query)
        mycursor.execute(update_query)
        mydb.commit()
        # Display Favorite Trails after the update
        query = "select * from FavoriteTrails"

    print(query)
    
    df = pandas.read_sql_query(query, mydb)
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

    # print(response)
    return response



if __name__ == '__main__':
   app.run()

