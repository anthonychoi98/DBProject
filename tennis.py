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
    player1ID=[]
    player2ID=[]
    graph_data =[]

    if request.method == 'GET':

        print("here")
        fn1 = request.args.get('fn1')
        ln1 = request.args.get('ln1')
        fn2 = request.args.get('fn2')
        ln2 = request.args.get('ln2')

        if (fn1 is not None and fn2 is not None):
            print(fn1)
            print(fn2)

            getp1 = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn1, ln1)

            conn =create_connection()
            crs = conn.cursor()

            player1ID = crs.execute(getp1).fetchone()

            #if(playerID is not None):
            #query2 = "select T.t_surface, COUNT(A.v_wID) from allTournaments A, tournaments T where A.v_wID = %d AND T.t_ID = A.v_ID group by T.t_surface;"%(int(playerID[0]))
            #results2 = crs.execute(query2)
            #surfacedata = [[str(item) for item in results] for results in crs.fetchall()]
            #for sd in surfacedata:
            #    print(sd)


            getp2 = "select MIN(p_playerID) from players where p_firstName = '%s' AND p_lastName = '%s';"%(fn2, ln2)

            conn =create_connection()
            crs = conn.cursor()
            player2ID = crs.execute(getp2).fetchone()


            versusquery = "select R.playerID as p1, R.wins as p1won, T.p2, T.p2wins from (select A.v_wID as playerID, COUNT(A.v_wID) as wins from allTournaments A where A.v_wID = %d AND A.v_lID = %d) R,(select A.v_wID as p2, COUNT(A.v_wID) as p2wins from allTournaments A where A.v_wID = %d AND A.v_lID = %d)T;"%(int(player1ID[0]), int(player2ID[0]), int(player2ID[0]), int(player1ID[0]))
            res = crs.execute(versusquery).fetchone()

            print("results" )
            print(res)
            pie_chart = pygal.Pie()
            if (res[1] == 0 and res[3] == 0):
                print("TNEVNW;AEONEV;OIAWNO;EVIAN")
                pie_chart.title = 'never played in the last 10 years'
            else:
                pie_chart.title = 'player 1 vs player 2'
            p1 = fn1 + ' ' + ln1
            p2 = fn2 + ' ' + ln2
            pie_chart.add(p1, int(res[1]))
            pie_chart.add(p2, int(res[3]))

            pie_chart.render()

            graph_data = pie_chart.render_data_uri()

        else:
            graph_data = 'https://i.pinimg.com/564x/30/62/75/3062756a297f1e3c22e35f3fe89b3ecc.jpg'


    return render_template('versus.html', fn1=fn1, fn2=fn2, graph_data=graph_data)

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
        graph_data=[]
        tarr=[]
        minyear = 0
        maxyear = 0

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
                tarr.append(sd[0])
                if sd[1] == 'Clay':
                    d1.append(int(sd[2]))
                elif sd[1] == 'Grass':
                    d2.append(int(sd[2]))
                elif sd[1] == 'Hard':
                    d3.append(int(sd[2]))

            #for range of years in graph data
            minyear = min(tarr)
            maxyear = str(int(max(tarr)) + 1)

            #retrieve strings to display
            s = data[0]
            li = str(s).strip(']').split(", ")
            fn =li[1]
            ln = li[2]
            bd=li[3]
            country=li[5]

            #graph to display
    	    graph_data = getbardata(d1, d2, d3, minyear, maxyear)

            close_connection(conn)

        else:
            fn = 'hello'
            ln = 'there'
            graph_data = 'https://i.pinimg.com/564x/30/62/75/3062756a297f1e3c22e35f3fe89b3ecc.jpg'
    return render_template('players.html', fn=fn, ln=ln, bd=bd,country=country, gwon=gwon, mwon=mwon, graph_data=graph_data)

@app.route('/insert', methods=['GET','POST'])
def insert():
    print("here")
    name = []
    year =[]
    surface =[]
    bestof=[]
    level=[]
    insertc=''
    if request.method == 'POST':

        name = request.form.getlist('name')
        year = request.form.getlist('year')
        surface = request.form.getlist('surface')
        bestof = request.form.getlist('bestof')
        level = request.form.getlist('level')

        if (name is not None and year is not None):

            id = str(name[0]) + str(year[0])
            insert = "insert into tournaments values('%s', '%s', '%s', '%s', %d, '%s');"%(str(id), str(name[0]), str(year[0]), str(surface[0]), int(bestof[0]), str(level[0]))
            conn =create_connection()
            crs = conn.cursor()
            print(insert)
            crs.execute(insert)
            conn.commit()
            print("inserted!")

            insertc = 'INSERTED ' + str(name[0]) + '!'
    return render_template('insert.html', inserted=insertc)

def getbardata(d1, d2, d3, minyear, maxyear):
    years =[]
    print("minyear and max")
    print(minyear)
    print(maxyear)
    for i in range(int(minyear), int(maxyear)):
        print("year:")
        print(i)
        years.append(i)
    line_chart = pygal.Bar()
    line_chart.title = 'Wins based on surface'
    #line_chart.x_labels = map(str, range(int(minyear), int(maxyear)))
    line_chart.x_labels = map(str, years)

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

def main():
    print("python main function")



if __name__ == '__main__':
    main()


app.run()
