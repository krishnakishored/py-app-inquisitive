from app import app
from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm

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



@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# return render_template('login.html', title='Sign In', form=form)
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		# return redirect('/index')
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)


@app.route('/words',methods=['GET','POST'])    
def random_words():
    words = [
            {'german': 'erzählen', 'english' : 'to narrate'}, 
            {'german': 'entsprechen', 'english' : 'to correspond'} 
    ]
    return render_template('words.html', title='Words', words=words)