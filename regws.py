#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sqlite3, click, subprocess
from flask import Flask, g, render_template, request, flash,\
	send_file, abort, redirect

app = Flask(__name__)
#app.config.from_object(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'regws.db'),
	SECRET_KEY = 'SECRET_KEY',
	USERNAME = 'admin',
	PASSWORD = 'admin'
))

def get_db():
	"""Open a connection if not existed for the current application context"""
	if not hasattr(g, 'db'):
		g.db = sqlite3.connect(app.config['DATABASE'])
		g.db.row_factory = sqlite3.Row
	return g.db

@app.teardown_appcontext
def teardown_db(error):
	"""Teardown the connection if existed for the current application context"""
	if hasattr(g, 'db'):
		g.db.close()

@app.cli.command('init_db')
def init_db():
	"""Initialize the database"""
	print("Initializes the database")
	db = get_db()
	with app.open_resource('schema.sql') as f:
		db.cursor().executescript(f.read())
	db.commit()

def add_user(contest_id, username, password, teamname, hidden):
	subprocess.call(['cmsAddUser', '-p', password, username, teamname, username])
	subprocess.call(['cmsAddParticipation', '-c', str(contest_id), username] + (['--hidden'] if hidden else []))
	return True

@app.cli.command('add_users')
@click.argument('contest_id', type=int)
def add_users(contest_id):
	"""Add users to a contest"""
	db = get_db()
	for row in db.execute('select username, password, teamname, hidden from users'):
		add_user(contest_id, row[username], row[password], row[teamname], row[hidden])

import home_page
import edit_page

@app.route('/change_logo', methods=['GET', 'POST'])
def change_logo_page():
	filename = '/var/local/lib/cms/ranking/logo.png'
	if request.method == 'POST':
		if 'file' not in request.files:
			flash("No file part")
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			if os.path.isfile(filename):
				os.remove(filename)
			flash("Logo removed")
			return redirect(request.url)
		flash(file.filename)
		file.save('/var/local/lib/cms/ranking/logo.png')
		return redirect(request.url)
	last_modified=os.path.getmtime(filename)
	return render_template('change_logo_page.html',
		mtime=str(last_modified))

@app.route('/logo')
def logo_page():
	filename = '/var/local/lib/cms/ranking/logo.png'
	if not os.path.isfile(filename):
		abort(404)
	last_modified=os.path.getmtime(filename)
	return send_file(filename, last_modified=last_modified)
		
