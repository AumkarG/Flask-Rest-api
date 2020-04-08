import flask
from flask import request, jsonify
from flask_restful import Resource, Api

import sqlite3

app = flask.Flask(__name__)
api=Api(app)

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
    print(id)
    query = "SELECT * FROM user WHERE id=" +id+";"
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    if(len(result)==0):
        return jsonify({"error":"ID NOT FOUND"})
    return jsonify(result)




@app.route("/create", methods=['POST'])
def create():
    if request.method == 'POST':
        fname = request.json['fname']
        lname = request.json['lname']
        email = request.json['email']
        
        try:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            sql='SELECT * FROM user WHERE email = "'+email+'";'
            print(sql)
            email_match= cur.execute(sql).fetchall()
            if(email_match):
                return jsonify({'error':'email exists'})
            num=cur.execute("select num from info").fetchall()
            new_id=num[0][0]+1      
            print(new_id)                                  #Generates new ID
            sql="update info set num = "+str(new_id)+";"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.execute( "INSERT INTO user(id,fname,lname,email) VALUES(? ,? ,? ,?);",(new_id,fname,lname,email))
            conn.commit()
            query = "SELECT * FROM user WHERE id=" +str(new_id)+";"
            result = cur.execute(query).fetchall()
            return jsonify(result)
        except Exception as e:
            print(e)
            return "Exception encountered"
        return page_not_found

api.add_resource(byid, '/userbyid/<id>')
api.add_resource(all, '/all')



if __name__ == '__main__':
    app.run(debug=True)
