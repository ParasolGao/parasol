from flask import Flask, session, redirect, url_for, escape, request
from flask import request
from flask import render_template
from user import User
from flask_table import Table, Col

app = Flask(__name__)
app.secret_key = 'C2\xe3\xb8\x1c@\x94K\x82+\xa3\x0c\xee\x8fl"\x8bPu\x9c\xe0'


class ItemTable(Table):
    name = Col('Book')


@app.route('/login', methods=['POST', 'GET'])
def login():
#   username = request.form['username']
    
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        username = session['username']
        password = session['password']
        print(username)
        if username is None:
            return render_template('404.html')
        user_temp = User(username,password)
        result = user_temp.login()
        if result == True:
            return redirect(url_for('index'))
        else:
            return render_template('404.html')

    return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login')) 
    
@app.route('/recommend')
def recommend():
    username = session['username']
    password = session['password']
    user_temp = User(username, password)
    items = user_temp.recommend_based_on_score()
    books = items
    print("books:")
    print(books)
    return render_template('rec_table.html', books=books)
    
@app.route('/recommend_based_on_simularity')
def recommend_based_on_simularity():
    username = session['username']
    password = session['password']
    user_temp = User(username,password)
    items = user_temp.recommend_based_on_simularity()
    books = items
    print("books:")
    print(books)
    return render_template('rec_table.html', books=books)

if __name__ == "__main__":
    app.run()