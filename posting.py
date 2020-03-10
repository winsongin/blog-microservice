import sqlite3, json, datetime
from flask import Flask, abort, jsonify, request, g
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

conn = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
cur = conn.cursor()

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('reddit.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Borrowed make_dicts(), get_db(), close_connection(), and query_db(), and @app.teardown_appcontext route from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Borrowed from https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to the Home Page of the Posting Microservice.</p>'''

# Create a new post
@app.route('/api/v1.0/resources/collections', methods=['POST'])
def create_post():
    parameters = request.get_json(force=True)

    title = parameters['title']
    text = parameters['text']
    community = parameters['community']
    username = parameters['username']
    date = datetime.date.today() # use of datetime module in order to prevent incorrect date from user input

    if len(parameters.keys()) == 4:

        query = "INSERT INTO posts (title, text, community, url, username, date) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, (title, text, community, None, username, date))
        conn.commit()

        query2 = "SELECT id FROM posts WHERE title=? AND text=? AND community=? AND username=? AND date=?"
        postID = query_db(query2, (title, text, community, username, date))
    
    elif len(parameters.keys()) == 5:
        url = parameters['url']

        query = "INSERT INTO posts (title, text, community, url, username, date) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, (title, text, community, url, username, date))
        conn.commit()

        query2 = "SELECT id FROM posts WHERE title=? AND text=? AND community=? AND url=? AND username=? AND date=?"
        postID = query_db(query2, (title, text, community, url, username, date))

    location = f"/api/v1.0/resources/collections/{postID[0]['id']}"
    result = {'msg': 'Created Successfully'}
    return jsonify(result), 201, {'Location': location}

@app.route('/api/v1.0/resources/collections', methods=['GET', 'DELETE'])
def retrieve_post():
    args = request.args.get('rowID')

    # Retrieve an existing post based on id (the primary key)
    if request.method == 'GET':
        query = "SELECT title, community, username, date FROM posts WHERE id=?"

        result = query_db(query, args)

        if len(result) == 0:
            result = abort(404, description="Resource not found") # return HTTP code 404 if the resource can't be found or the row has already been deleted

            return jsonify(result)

        return jsonify(result)

    # Delete an existing post based on id (the primary key)
    if request.method == 'DELETE':
        query = "SELECT title, community, username, date FROM posts WHERE id=?"

        result = query_db(query, args)

        if len(result) == 0:
            result = abort(404, description="Resource not found")

            return jsonify(result)

        else:
            query = "DELETE FROM posts WHERE id=?"
            cur.execute(query, args)
            conn.commit()

            msg = {'msg': 'The post has been deleted'}
            return jsonify(msg)

# Retrieve the n most recent posts from a particular community
@app.route('/api/v1.0/resources/collections/recent', methods=['GET'])
def retrieve_community_posts():
    args = request.args.get('community')
    amount = request.args.get('amount')

    query = "SELECT title, community, username, date FROM posts WHERE community=? ORDER BY id LIMIT ?"

    result = query_db(query, (args, amount))

    if len(result) == 0:
        result = abort(404, description="Resource not found")
        return jsonify(result)

    # There are not that many amount of posts
    if len(result) < int(amount): 
        result = abort(404, description="Resource not found")
        return jsonify(result)

    return jsonify(result)

# Retrieve the n most recent posts from any community
@app.route('/api/v1.0/resources/collections/all', methods=['GET'])
def retrieve_all_posts():
    amount = request.args.get('amount')

    query = "SELECT title, community, username, date FROM posts LIMIT ?"
    
    result = query_db(query, (amount,))

    if len(result) < int(amount):
        result = abort(404, description="Resource not found")
        return jsonify(result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

