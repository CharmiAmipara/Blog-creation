from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from blog import db
from blog.posts.forms import newPost
from blog.models import Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
	form = newPost()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Blog has been posted!', category='success')
		return redirect(url_for('main.home'))
	return render_template('newpost.html', title='New Post', form = form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def updatepost(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = newPost()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Blog has been updated!!', category='success')
		return redirect(url_for('posts.post', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('newpost.html', title='Update Post', form = form, legend ='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletepost(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Blog has been deleted!', category='success')
	return redirect(url_for('main.home'))