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
    fn = ''
    ln = ''
    data = ''

    if request.method == 'POST':
        fn =  request.form.getlist('fn')
        ln =  request.form.getlist('ln')

        query = "select * from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn[0], ln[0])
        print(query)
        conn = create_connection()
        data = execute_query(conn, query)
        close_connection(conn)

    return render_template("players.html", data=data)

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
