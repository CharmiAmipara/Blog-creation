from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from blog import db, bcrypt
from blog.users.forms import Reg, Login, Update
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from blog.users.utils import save_pic

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = Reg()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data , email=form.email.data, password=hash_password)
		db.session.add(user)
		db.session.commit()
		flash('Account has been created! Log in to access your account!', category='success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Log in unsuccessful! Please check Email and Password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home')) 

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = Update()
	if form.validate_on_submit():
		if form.picture.data:
			pic_file = save_pic(form.picture.data)
			current_user.img = pic_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Account has been updated!', category='success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	img = url_for('static', filename='IMG/' + current_user.img)
	return render_template('account.html', title='Account', img=img, form =form)

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
	return render_template('user_posts.html' , posts=posts, user=user  )

