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
	closed boolean
);
insert into config values (0, 'Free Contest ??', '(Contest details)', 'http://(Link to CWS)', 'http://(Link to RWS)', 0);

