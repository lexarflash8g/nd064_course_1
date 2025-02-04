import sqlite3
import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

db_connection_count = 0  # Add this line to declare the variable

def get_db_connection():
    global db_connection_count  # Declare the variable as global to modify it
    db_connection_count += 1  # Increment the count each time a connection is made
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    if post is not None:
        logging.info('Article "%s" retrieved!', post['title'])
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logging.info('Article with id "%s" does not exist!', post_id)
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)

@app.route('/about')
def about():
    logging.info('About us page was retrieved!')
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                            (title, content))
            connection.commit()
            connection.close()
            logging.info('Article "%s" created!', title)
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    return jsonify(db_connection_count=db_connection_count, post_count=posts[0])

if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
