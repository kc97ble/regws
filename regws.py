#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sqlite3, click, subprocess
from flask import Flask, g, render_template, request, flash

app = Flask(__name__)
#app.config.from_object(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'regws.db'),
	SECRET_KEY = 'SECRET_KEY',
	USERNAME = 'admin',
	PASSWORD = 'admin'
))

def get_db():
	"""Open a connection if not existed
	for the current application context"""
	if not hasattr(g, 'db'):
		g.db = sqlite3.connect(app.config['DATABASE'])
		g.db.row_factory = sqlite3.Row
	return g.db

@app.teardown_appcontext
def teardown_db(error):
	"""Teardown the connection if existed
	for the current application context"""
	if hasattr(g, 'db'):
		g.db.close()

@app.cli.command('initdb')
def init_db():
	"""Initialize the database"""
	print("Initializes the database")
	db = get_db()
	with app.open_resource('schema.sql') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('addusers')
@click.argument('contest-id', type=int)
def add_users(contest_id):
	"""Add users to CMS"""
	db = get_db()
	count_ok = 0
	count_failed = 0
	for row in db.execute('select username, password, teamname,'
	' hidden from users'):
		exit_status_1 = subprocess.call([
			'echo', 'cmsAddUser', 
			'-p', row['password'], 
			row['username'], 
			row['teamname'], 
			row['username'],
		])
		exit_status_2 = subprocess.call([
			'echo', 'cmsAddParticipation',
			'-c', str(contest_id),
			row['username'],
			'--hidden' if row['hidden'] != 0 else '',
		])
		if exit_status_1==0 and exit_status_2==0:
			count_ok += 1
		else:
			count_failed += 1
	print("OK %d/%d" % (count_ok, count_ok+count_failed))

import home_page
import edit_page
