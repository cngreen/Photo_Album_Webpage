CREATE DATABASE IF NOT EXISTS group29_pa2;
USE group29_pa2;
DROP TABLE IF EXISTS AlbumAccess;
DROP TABLE IF EXISTS Contain;
DROP TABLE IF EXISTS Photo;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS User;


CREATE TABLE User
(
	username VARCHAR(20),
	password VARCHAR(256),
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	email VARCHAR(40),
	PRIMARY KEY (username)
);

CREATE TABLE Album
(
	albumid int AUTO_INCREMENT,
	title VARCHAR(50),
	created TIMESTAMP default CURRENT_TIMESTAMP,
	lastupdated TIMESTAMP default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	username VARCHAR(20),
	access ENUM('public','private'),
	PRIMARY KEY (albumid),
	FOREIGN KEY (username) REFERENCES User(username)
	ON UPDATE CASCADE
	ON DELETE RESTRICT
);

CREATE TABLE Photo
(
	picid VARCHAR(40),
	format VARCHAR(3),
	date TIMESTAMP default CURRENT_TIMESTAMP,
	PRIMARY KEY (picid)
);

CREATE TABLE Contain
(
	sequencenum int,
	albumid int,
	picid VARCHAR(40),
	caption VARCHAR(255) NOT NULL,
	PRIMARY KEY (sequencenum),
	FOREIGN KEY (albumid) REFERENCES Album(albumid)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (picid)   REFERENCES Photo(picid)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE AlbumAccess
(
	albumid int,
	username VARCHAR(20),
	FOREIGN KEY (albumid) REFERENCES Album(albumid)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (username) REFERENCES User(username)
	ON UPDATE CASCADE
	ON DELETE RESTRICT
);
