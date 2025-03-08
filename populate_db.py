import sqlite3
import random
import string
from hashlib import sha256
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect('stockr.db')
cursor = conn.cursor()

# Data for teams
teams_data = [
    ('Engineering', 'Building A'),
    ('Marketing', 'Building B'),
    ('HR', 'Building C'),
    ('Finance', 'Building D'),
    ('IT Support', 'Building E')
]

# Insert teams
cursor.executemany('''
    INSERT INTO teams (team_name, team_location) 
    VALUES (?, ?)
''', teams_data)

# Commit changes to DB
conn.commit()


# Getting data from teams
cursor.execute("SELECT id FROM teams")
team_ids = [row[0] for row in cursor.fetchall()]

# Ensure we have enough teams before proceeding
if len(team_ids) < 5:
    raise ValueError("Not enough teams found. Ensure teams are populated first.")

# Data for subteams (assigned to random teams)
subteams_data = [
    ('Backend Dev', team_ids[0], 'Building A'),
    ('Frontend Dev', team_ids[0], 'Building A'),
    ('Cloud Infra', team_ids[0], 'Building A'),
    ('Social Media', team_ids[1], 'Building B'),
    ('Brand Management', team_ids[1], 'Building B'),
    ('Recruitment', team_ids[2], 'Building C'),
    ('Employee Relations', team_ids[2], 'Building C'),
    ('Payroll', team_ids[3], 'Building D'),
    ('Budget Planning', team_ids[3], 'Building D'),
    ('IT Helpdesk', team_ids[4], 'Building E'),
    ('Security Ops', team_ids[4], 'Building E'),
    ('DevOps', team_ids[0], 'Building A'),
    ('SEO', team_ids[1], 'Building B'),
    ('Training', team_ids[2], 'Building C'),
    ('Audit', team_ids[3], 'Building D')
]

# Insert subteams
cursor.executemany('''
    INSERT INTO subteams (subteam_name, origin_team, subteam_location) 
    VALUES (?, ?, ?)
''', subteams_data)

# Commit changes to DB
conn.commit()


# Fetch valid team IDs
cursor.execute("SELECT id FROM teams")
team_ids = [row[0] for row in cursor.fetchall()]

# Fetch valid subteam IDs and their corresponding team IDs
cursor.execute("SELECT id, origin_team FROM subteams")
subteams = cursor.fetchall()
subteam_ids = [row[0] for row in subteams]

# Helper function to hash passwords
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Sample user data
users_data = [
    ("Alice", "Johnson", "alice.johnson@example.com", team_ids[0], subteam_ids[0]),
    ("Bob", "Smith", "bob.smith@example.com", team_ids[1], subteam_ids[1]),
    ("Charlie", "Brown", "charlie.brown@example.com", team_ids[2], subteam_ids[2]),
    ("David", "Miller", "david.miller@example.com", team_ids[3], subteam_ids[3]),
    ("Emma", "Davis", "emma.davis@example.com", team_ids[4], subteam_ids[4]),
    ("Frank", "Wilson", "frank.wilson@example.com", team_ids[0], subteam_ids[5]),
    ("Grace", "Moore", "grace.moore@example.com", team_ids[1], subteam_ids[6]),
    ("Henry", "Taylor", "henry.taylor@example.com", team_ids[2], subteam_ids[7]),
    ("Isabella", "Anderson", "isabella.anderson@example.com", team_ids[3], subteam_ids[8]),
    ("Jack", "Thomas", "jack.thomas@example.com", team_ids[4], subteam_ids[9])
]

# Generate coreid and hash passwords
users_data = [
    (f"{first.lower()}{last.lower()[0:2]}", first, last, hash_password("default123"), email, team, subteam)
    for first, last, email, team, subteam in users_data
]

# Insert users
cursor.executemany('''
    INSERT INTO users (coreid, name, last_name, password, email, team, subteam) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', users_data)

# Commit changes to DB
conn.commit()

# Insert sample assets type
assets_types_data = [
    ('Accessories',),
    ('Phones',),
    ('Computers',),
    ('Equipments',)
]

cursor.executemany('''
    INSERT INTO assets_type (asset_type) 
    VALUES (?)
''', assets_types_data)

# Commit changes to DB
conn.commit()

# Fetch valid asset type IDs
cursor.execute("SELECT id FROM assets_type")
assets_type_ids = [row[0] for row in cursor.fetchall()]

# Fetch valid user IDs
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

# Fetch valid team IDs
cursor.execute("SELECT id FROM teams")
team_ids = [row[0] for row in cursor.fetchall()]

# Function to generate a unique tag
def generate_unique_tag(existing_tags):
    while True:
        tag = random.randint(1000, 99999)
        if tag not in existing_tags:
            existing_tags.add(tag)
            return tag

# Function to generate a random serial number
def generate_serial_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

# Set of existing tags to avoid duplicates
existing_tags = set()

# Sample asset names categorized by type
asset_names = {
    "Computers": ["Laptop Dell XPS", "MacBook Pro", "HP EliteBook", "Lenovo ThinkPad", "Asus ROG Strix"],
    "Phones": ["iPhone 13", "Samsung Galaxy S22", "Google Pixel 7", "OnePlus 9", "Xiaomi Mi 11"],
    "Accessories": ["Logitech Mouse", "Mechanical Keyboard", "USB-C Hub", "Wireless Headset", "Portable SSD"],
    "Equipments": ["3D Printer", "Projector", "Server Rack", "CCTV Camera", "VR Headset"]
}

# Asset distribution across types
assets_data = []
for asset_type_id in assets_type_ids:
    category = list(asset_names.keys())[assets_type_ids.index(asset_type_id)]
    for _ in range(10):  # Create 10 assets per type
        tag = generate_unique_tag(existing_tags)
        name = random.choice(asset_names[category])
        owner_id = random.choice(user_ids)
        origin_team = random.choice(team_ids)
        status = random.choices(["ok", "not ok"], weights=[10, 1], k=1)[0]
        serial_number = generate_serial_number()
        assets_data.append((asset_type_id, tag, name, owner_id, origin_team, status, serial_number))

# Insert assets
cursor.executemany('''
    INSERT INTO assets (type, tag, name, owner, origin_team, status, serial_number) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', assets_data)

# Commit changes to DB
conn.commit()


# Fetch valid asset IDs
cursor.execute("SELECT tag FROM assets")
asset_tags = [row[0] for row in cursor.fetchall()]

# Fetch valid user IDs
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

# Generate random transactions
transactions_data = []
for asset_tag in asset_tags:
    responsible_id = random.choice(user_ids)
    date_transaction = datetime.now() - timedelta(days=random.randint(1, 365))  # Random date within the last year
    transactions_data.append((asset_tag, responsible_id, date_transaction))

# Insert transactions
cursor.executemany('''
    INSERT INTO transactions (asset_tag, responsible_id, date_transaction, comments) 
    VALUES (?, ?, ?, NULL)
''', transactions_data)


# Commit and close
conn.commit()
conn.close()

print("Database populated successfully!")
