PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user ( --imaginary user, used for merging clients
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nCon	INTEGER NOT NULL DEFAULT 0,
	totalTime	INTEGER NOT NULL DEFAULT 0,
	maxTime	INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS client ( --represents a TS3 client
	id	INTEGER NOT NULL PRIMARY KEY,
	mainNickname TEXT,
	nCon	INTEGER NOT NULL DEFAULT 0,
	totalTime	INTEGER NOT NULL DEFAULT 0,
	maxTime	INTEGER NOT NULL DEFAULT 0,
	user INTEGER,
	FOREIGN KEY(user) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS connection (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	client	INTEGER NOT NULL,
	connected	INTEGER NOT NULL,
	disconnected	INTEGER NOT NULL,
	reason	INTEGER NOT NULL,
	ip	TEXT NOT NULL,
	server	INTEGER NOT NULL DEFAULT 0,
	duration INTEGER NOT NULL DEFAULT 0,
	logfile INTEGER NOT NULL,
	FOREIGN KEY(client) REFERENCES client(id),
	FOREIGN KEY(logfile) REFERENCES logfile(id)
);

CREATE TABLE IF NOT EXISTS nickname (
	client	INTEGER NOT NULL,
	nickname	TEXT NOT NULL,
	used	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(client, nickname),
	FOREIGN KEY(client) REFERENCES client(id)
);

CREATE TABLE IF NOT EXISTS logfile (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	filename	TEXT NOT NULL UNIQUE,
	lines	INTEGER NOT NULL DEFAULT 0,
	size INTEGER NOT NULL DEFAULT 0
);

CREATE TRIGGER trigger_user_stats AFTER UPDATE ON client
	WHEN NEW.user <> NULL
BEGIN
  UPDATE user SET
    nCon = (SELECT SUM(nCon) FROM client WHERE user = NEW.user),
    totalTime = (SELECT SUM(totalTime) FROM client WHERE user = NEW.user),
    maxTime = (SELECT MAX(maxTime) FROM client WHERE user = NEW.user)
    WHERE id = NEW.user;
END;
