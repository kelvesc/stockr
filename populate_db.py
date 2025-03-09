from app.app import app, db
from app.models import Team, Subteam, User, Type, Asset, Transaction
from datetime import datetime, timezone
import random

def populate_db():
    with app.app_context():
        db.session.query(Transaction).delete()
        db.session.query(Asset).delete()
        db.session.query(User).delete()
        db.session.query(Subteam).delete()
        db.session.query(Team).delete()
        db.session.query(Type).delete()
        db.session.commit()


        # Create Teams
        teams = [Team(name=f"Team {i}", location=f"Location {i}") for i in range(1, 6)]
        db.session.add_all(teams)
        db.session.commit()

        # Create Subteams

        # Create Subteams
        subteams = [Subteam(name=f"Subteam {i}", team_id=random.choice(teams).id) for i in range(1, 11)]
        db.session.add_all(subteams)
        db.session.commit()

        # Create Users
        users = [
            User(
                name=f"User{i}",
                last_name=f"Last{i}",
                coreid=f"UserL{i}",
                email=f"user{i}@example.com",
                psw="password",
                team_id=random.choice(teams).id,
                subteam_id=random.choice(subteams).id,
            )
            for i in range(1, 11)
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create Types
        types = [Type(name=f"Type {i}") for i in range(1, 5)]
        db.session.add_all(types)
        db.session.commit()

        # Create Assets
        assets = [
            Asset(
                tag=i,
                name=f"Asset {i}",
                serial_number=f"SN{i:05d}",
                status="Available",
                comments="Test asset",
                type_id=random.choice(types).id,
                owner_id=random.choice(users).id,
                team_id=random.choice(teams).id,
            )
            for i in range(1, 41)
        ]
        db.session.add_all(assets)
        db.session.commit()

        # Create Transactions
        transactions = [
            Transaction(
                responsible_id=random.choice(users).id,
                asset_tag=random.choice(assets).tag,
                date_transaction=datetime.now(timezone.utc),
            )
            for _ in range(40)
        ]
        db.session.add_all(transactions)
        db.session.commit()

        print("Database populated with test data!")

if __name__ == "__main__":
    populate_db()
