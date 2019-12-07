import flask
from flask import request, jsonify, url_for, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pygal                                                       # First import pygal


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/anthonychoi98/Documents/GitHub/TennisDB/Tennis/Tennis.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/test', methods=['POST', 'GET'])
def test():
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

    return render_template("test.html",fn=fn, ln=ln,bd=bd,country=country, gwon=gwon, mwon=mwon)

@app.route('/versus', methods=['GET'])
def versus():
    fn1 =''
    fn2 =''
    ln1=''
    ln2=''
    playerID=[]
    if request.method == 'GET':
        print("here")
        if (fn1 is not None and fn2 is not None):
            print(fn1)
            print("now here")

            fn1 = request.args.get('fn1')
            ln1 = request.args.get('ln1')
            fn2 = request.args.get('fn2')
            ln2 = request.args.get('ln2')
            print(fn1)
            query = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn1, ln1)

            conn =create_connection()
            crs = conn.cursor()

            playerID = crs.execute(query).fetchone()

            query2 = "select T.t_surface, COUNT(A.v_wID) from allTournaments A, tournaments T where A.v_wID = %d AND T.t_ID = A.v_ID group by T.t_surface;"%(int(playerID[0]))
            results2 = crs.execute(query2)
            surfacedata = [[str(item) for item in results] for results in crs.fetchall()]
            for sd in surfacedata:
                print(sd)


            #for player 2

            query = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn2, ln2)

            conn =create_connection()
            crs = conn.cursor()

            playerID = crs.execute(query).fetchone()

            query2 = "select T.t_surface, COUNT(A.v_wID) from allTournaments A, tournaments T where A.v_wID = %d AND T.t_ID = A.v_ID group by T.t_surface;"%(int(playerID[0]))
            results2 = crs.execute(query2)
            surfacedata = [[str(item) for item in results] for results in crs.fetchall()]
            for sd in surfacedata:
                print(sd[1])



    return render_template('versus.html', fn1=fn1, fn2=fn2)

@app.route('/players', methods=['GET'])
def players():

    if request.method == 'GET':
        fn=''
        ln=''
        data=''
        playerID=[]
        fn=''
        ln=''
        bd=''
        country=''
        mwon=''
        gwon=''
        query2 = ''
        surfacedata =[]
        d1=[]
        d2=[]
        d3=[]


        fn = request.args.get('fn')
        ln = request.args.get('ln')
        if(fn is not None):
            #get player info
            query = "select * from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn, ln)
            print(query)
            conn = create_connection()

            crs = conn.cursor()
            crs.execute(query)

            data = [[str(item) for item in results] for results in crs.fetchall()]

            #get player ID
            query2 = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn, ln)
            playerID = crs.execute(query).fetchone()
            te = []

            #get titles won
            query2 = "select COUNT(*) from allTournaments where v_wID = %d AND v_round = 'F';"%(int(playerID[0]))
            query3 = "select COUNT(*) from allTournaments A, tournaments T where v_wID = %d AND v_round = 'F' AND t_ID = A.v_ID AND t_level = 'M';"%(int(playerID[0]))
            query4 = "select COUNT(*) from allTournaments A, tournaments T where v_wID = %d AND v_round = 'F' AND t_ID = A.v_ID AND t_level = 'G';"%(int(playerID[0]))

            twon1 = crs.execute(query2).fetchone()
            mwon1 = crs.execute(query3).fetchone()
            gwon1 = crs.execute(query4).fetchone()
            twon = twon1[0]
            mwon = mwon1[0]
            gwon = gwon1[0]
            print("won: " + str(twon))
            print("mwon: " + str(mwon))
            print("gwon: " + str(gwon))

            #get grand slams won
            #get total titles
            #get surface statistics
            query2 = "select R.year, R.surface, COUNT(A.v_wiD) from allTournaments A,(SELECT strftime('%s', t_date) AS year, t_surface as surface, t_ID as id from tournaments)R where A.v_wID = %d AND R.id = A.v_ID group by R.year, R.surface;"%('%Y', int(playerID[0]))
            results2 = crs.execute(query2)

            surfacedata = [[str(item) for item in results] for results in crs.fetchall()]
            for sd in surfacedata:
                #sdata.append(sd[1])
                if sd[1] == 'Clay':
                    d1.append(int(sd[2]))
                elif sd[1] == 'Grass':
                    d2.append(int(sd[2]))
                elif sd[1] == 'Hard':
                    d3.append(int(sd[2]))


            print(d1)
            print(d2)
            print(d3)

            close_connection(conn)
            s = data[0]
            print(s)
            li = str(s).strip(']').split(", ")
            fn =li[1]
            ln = li[2]
            bd=li[3]
            country=li[5]

            #plotbar()


    	    graph_data = getbardata(d1, d2, d3)

        else:
            fn = 'hello'
            ln = 'there'
    return render_template('players.html', fn=fn, ln=ln, bd=bd,country=country, gwon=gwon, mwon=mwon, graph_data=graph_data)

def getbardata(d1, d2, d3):
    line_chart = pygal.Bar()
    line_chart.title = 'Wins based on surface'
    line_chart.x_labels = map(str, range(2010, 2020))
    line_chart.add('Clay', d1)
    line_chart.add('Grass', d2)
    line_chart.add('Hard', d3)
    line_chart.render()
    return line_chart.render_data_uri()



def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('/Users/anthonychoi98/Documents/GitHub/TennisDB/Tennis/Tennis.db')
    except Error as e:
        print(e)
    return conn


def execute_query(query):
    if query == '' : return

    conn = None
    try:
        conn = sqlite3.connect('/Users/anthonychoi98/Documents/GitHub/TennisDB/Tennis/Tennis.db')
    except Error as e:
        print(e)

    cursor = conn.cursor()

    results = cursor.execute(query).fetchall()
    conn.commit()

    return results

def close_connection(db):
    if db is not None:
        db.close()

def plot():
    bar_chart = pygal.Bar()                                            # Then create a bar graph object
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    bar_chart.render_to_file('bar_chart.svg')
    b_data = bar_chart.render_data_uri()
    return render_template("players.html", url = b_data)

def main():
    print("python main function")



if __name__ == '__main__':
    main()


app.run()
