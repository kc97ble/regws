#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from regws import app, get_db, add_user
from flask import render_template, request, flash

@app.route('/', methods=['GET', 'POST'])
def home_page():
	db = get_db()
	cr = db.execute('select * from config')
	config = cr.fetchone()

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		teamname = request.form['teamname']
		hidden = request.form['hidden']

		if username=='' or password=='' or teamname=='':
			flash(u"Lỗi: Bạn phải điền tất cả các mục")
		elif db.execute('select count(*) from users where username=?', [username]).fetchone()[0] != 0:
			flash(u"Lỗi: Tên đăng nhập này đã được sử dụng");
		else:
			if config['contest_id'] != 0:
				hidden = 1
				add_user(config['contest_id'], username, password, teamname, hidden)
			db.execute('insert into users (username, password, teamname, hidden) values (?, ?, ?, ?)', [username, password, teamname, hidden])
			db.commit()
				
			flash(u"Đăng kí thành công")

	return render_template('home_page.html', config=config)
