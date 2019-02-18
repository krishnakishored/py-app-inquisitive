from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Spieler'}
    words = [
            {'german': 'denken', 'english' : 'to think'}, 
            {'german': 'nehmen', 'english' : 'to take'} 
    ]
    return render_template('index.html', title='Home', user=user, words=words)
    # return render_template('index.html', title='Home', words=words)