import flask
from flask import request, jsonify, url_for, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/anthonychoi98/Documents/GitHub/TennisDB/Tennis/Tennis.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/players', methods=['POST', 'GET'])
def players():
    fn=''
    ln=''
    data=''
    playerID=''
    fn=''
    ln=''
    bd=''
    country=''
    mwon=''
    gwon=''

    if request.method == 'POST':
        fn =  request.form.getlist('fn')
        ln =  request.form.getlist('ln')
        #get player info
        query = "select * from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn[0], ln[0])
        print(query)
        conn = create_connection()

        crs = conn.cursor()
        crs.execute(query)

        data = [[str(item) for item in results] for results in crs.fetchall()]

        #get player ID
        query2 = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn[0], ln[0])
        playerID = crs.execute(query).fetchone()[0]

        print(playerID)

        #get titles won
        query2 = "select COUNT(*) from allTournaments where v_wID = %d AND v_round = 'F';"%(int(playerID))
        query3 = "select COUNT(*) from allTournaments A, tournaments T where v_wID = %d AND v_round = 'F' AND t_ID = A.v_ID AND t_level = 'M';"%(int(playerID))
        query4 = "select COUNT(*) from allTournaments A, tournaments T where v_wID = %d AND v_round = 'F' AND t_ID = A.v_ID AND t_level = 'G';"%(int(playerID))

        twon = crs.execute(query2).fetchone()[0]
        mwon = crs.execute(query3).fetchone()[0]
        gwon = crs.execute(query4).fetchone()[0]
        print("won: " + str(twon))
        print("mwon: " + str(mwon))
        print("gwon: " + str(gwon))

        #get grand slams won
        #get total titles
        close_connection(conn)
        s = data[0]
        print(s)
        li = str(s).strip(']').split(", ")
        fn =li[1]
        ln = li[2]
        bd=li[3]
        country=li[5]



    return render_template("players.html",fn=fn, ln=ln,bd=bd,country=country, gwon=gwon, mwon=mwon)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('/Users/anthonychoi98/Documents/GitHub/TennisDB/Tennis/Tennis.db')
    except Error as e:
        print(e)
    return conn


def execute_query(conn, query):
    if query == '' : return

    #print (query)

    cursor = conn.cursor()

    results = cursor.execute(query).fetchall()
    for result in results:
        print(result)

    return results

def close_connection(db):
    if db is not None:
        db.close()




app.run()
