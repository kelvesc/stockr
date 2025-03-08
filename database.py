import sqlite3

conn = sqlite3.connect("stockr.db")
cursor = conn.cursor()

# Teams Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    team_location TEXT NOT NULL
);
''')

# Subteams Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subteams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subteam_name TEXT NOT NULL,
    origin_team INTEGER NOT NULL,
    subteam_location TEXT NOT NULL,
    FOREIGN KEY (origin_team) REFERENCES teams(id)
);
''')

# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coreid TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    team INTEGER NOT NULL,
    subteam INTEGER NOT NULL,
    FOREIGN KEY (team) REFERENCES teams(id),
    FOREIGN KEY (subteam) REFERENCES subteams(id)
);
''')

# Asset type Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS assets_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type TEXT NOT NULL
);
''')

# Assets Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    tag INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    owner INTEGER NOT NULL,
    origin_team INTEGER NOT NULL,
    status TEXT NOT NULL,
    serial_number TEXT UNIQUE NOT NULL,
    comments TEXT,
    FOREIGN KEY (type) REFERENCES assets_type(id),
    FOREIGN KEY (owner) REFERENCES users(id),
    FOREIGN KEY (origin_team) REFERENCES teams(id)
);
''')

# Transactions Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS assets_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    responsible_id INTEGER NOT NULL,
    date_transaction DATETIME NOT NULL,
    comments TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    FOREIGN KEY (responsible_id) REFERENCES users(id)
);
''')

# Transactions Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsible_id INTERGET NOT NULL,
    asset_tag INTEGER NOT NULL,
    date_transaction DATETIME NOT NULL,
    comments TEXT,
    FOREIGN KEY (asset_tag) REFERENCES assets(tag),
    FOREIGN KEY (responsible_id) REFERENCES users(id)
);
''')


conn.commit()
conn.close()

print("Database created successfully!")