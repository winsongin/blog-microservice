# import flask_api
# from flask_api import status, exceptions
# import pugsql

import sqlite3, json
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = sqlite3.connect("reddit.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS posts(
    id INT PRIMARY KEY,
    title STRING,
    text STRING,
    community STRING,
    url STRING DEFAULT NULL,
    username STRING,
    date STRING
)""")

conn.commit()

# Borrowed make_dicts(), get_db(), close_connection(), and query_db() from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("reddit.db")
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/v1.0/resources/collections', methods=['POST'])
def create_post():
    parameters = request.get_json()

    title = parameters['title']
    text = parameters['text']
    community = parameters['community']
    username = parameters['username']
    date = parameters['date']

    if len(parameters.keys()) == 5:

        query = "INSERT INTO posts (title, text, community, url, username, date) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, (title, text, community, None, username, date))
        conn.commit()
    
    elif len(parameters.keys()) == 6:
        url = parameters['url']

        query = "INSERT INTO posts (title, text, community, url, username, date) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, (title, text, community, url, username, date))
        conn.commit()

    result = "Created Successfully"
    return jsonify(result), 201



@app.route('/api/v1.0/resources/collections', methods=['DELETE'])
def delete_post():


# Retrieve n posts from any community
# @app.route('/api/v1.0/resources/collections/all', methods=['GET'])
# def allRecentPosts():
#     n = request.args.get('n', type = int)
    
#     query = "SELECT title, community, username FROM posts"

#     cur.execute(query)
#     results = cur.fetchall()

#     return jsonify(results)

# # Retrieve n posts from a specific community
# @app.route('/api/v1.0/resources/collections', methods=['GET'])
# def communityRecentPosts():
#     n = request.args.get('n', type = int)
#     community  = request.args.get('community', type = int)
    
#     query = "SELECT title, community, username FROM posts WHERE community = {}"
#     cur.execute(query.format(community))
#     results = cur.fetchall()
    
#     return jsonify(results)


# Retrieve an existing post
@app.route('/api/v1.0/resources/collections', methods=['GET'])
def retrieve_post():
    title = request.args.get('title')
    community = request.args.get('community')
    username = request.args.get('username')

    print(community)
    print(title)
    print(username)

    query = ("SELECT * FROM posts WHERE title=? AND community=? AND username=?")
    args = [title, community, username]

    result = query_db(query, args, one=False)

    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True)

