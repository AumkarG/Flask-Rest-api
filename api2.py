import flask
from flask import request, jsonify
from flask_restful import Resource, Api

import sqlite3

app = flask.Flask(__name__)
api=Api(app)
app.config["DEBUG"] = True

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class all(Resource):
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

api.add_resource(HelloWorld, '/')
api.add_resource(byid, '/userbyid/<id>')


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=['GET'])
def home():
   return '''<h1>User System Prototype</h1>
<p>A prototype API for creating and fetching user.</p>'''


@app.route('/api/users/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM user;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The User for the given id does not exist </p>", 404


@app.route('/api/users/byid', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
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


@app.route('/api/users/create', methods=['POST'])
def create():
    if(request.method=='POST'):
        try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        all_books = cur.execute('SELECT * FROM user;').fetchall()
        return jsonify(all_books)
    else:
        return page_not_found(404)





app.run()
