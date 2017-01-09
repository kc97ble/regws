#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from regws import app, get_db
from flask import render_template, request, flash

@app.route('/edit', methods=['GET', 'POST'])
def edit_page():
	db = get_db()
	if request.method=='POST':
		fields = ['title', 'detail', 'cwsurl', 'rwsurl', 'closed', 'contest_id']
		db.execute('update config set {}=?, {}=?, {}=?, {}=?, {}=?, {}=?'.format(*fields), [request.form[x] for x in fields])
		db.commit()
		flash(u"Đã lưu")
	cr = db.execute('select * from config')
	config = cr.fetchone()
	print(config)
	return render_template('edit_page.html', config=config)
