-- $ sqlite3 reddit.db < reddit.sql

PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    text VARCHAR NOT NULL,
    community VARCHAR NOT NULL,
    url VARCHAR DEFAULT NULL,
    username VARCHAR NOT NULL,
    date DATE NOT NULL
);
