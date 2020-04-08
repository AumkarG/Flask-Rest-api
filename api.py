import flask
from flask import request, jsonify
from flask_restful import Resource, Api

import sqlite3

app = flask.Flask(__name__)
api=Api(app)
app.config["DEBUG"] = True

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The User for the given id does not exist </p>", 404

class all(Resource):
    def get(self,id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        all_users= cur.execute('SELECT * FROM user;').fetchall()
        return jsonify(all_users)


class byid(Resource):
    def get(self,id):
        query = "SELECT * FROM user WHERE"
        to_filter = []
        if id:
            query += ' id=? AND'
            to_filter.append(id)
        if not (id):
            return page_not_found(404)

        query = query[:-4] + ';'
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        results = cur.execute(query, to_filter).fetchall()

        return jsonify(results)

@app.route('/userbyid', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    query = "SELECT * FROM user WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)

    query = query[:-4] + ';'
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    result = cur.execute(query, to_filter).fetchall()
    return jsonify(result)

def pap():
    print('yolo')



@app.route("/create", methods=['POST'])
def create():
    if request.method == 'POST':
        fname = request.json['fname']
        lname = request.json['lname']
        email = request.json['email']
        id=3
        try:
        #    sql = ''' INSERT INTO user(id,fname,lname,email)
        #        VALUES(?,?,?,?); '''
        #    conn = sqlite3.connect('users.db')
        #    data_tuple = (id, fname,lname, email)
        #    cur = conn.cursor()
        #    cur.execute(sql, data_tuple)
        #    pap()
        #    return jsonify(request.json)
            print(email)
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute( "INSERT INTO user(id,fname,lname,email) VALUES(8,'RF','24F','EF2F');")
            print("Heylo")
            conn.commit()
            return jsonify(request.json)
        except Exception as e:
            return e

        return page_not_found

api.add_resource(byid, '/userbyid/<id>')
api.add_resource(all, '/all')



if __name__ == '__main__':
    app.run(debug=True)
