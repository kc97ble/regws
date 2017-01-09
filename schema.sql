-- USERS --
drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username text not null,
	password text,
	teamname text,
	hidden boolean
);

-- CONFIG --
drop table if exists config;
create table config (
	id integer primary key check(id=0),
	title text,
	detail text,
	cwsurl text,
	rwsurl text,
	closed boolean,
	contest_id integer
);

insert into config values (
	0,
	'Free Contest',
	'(Contest details)',
	'http://52.39.24.177/',
	'http://52.39.24.177:8890',
	0,
	0
);

