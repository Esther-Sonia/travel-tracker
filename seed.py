from app.database import session, Base, engine
from app.models import User, Destination, Trip
from datetime import date

Base.metadata.create_all(engine)


def seed():
    #sample users
    user1 = User(name="Esther", email="esther@gmail.com")
    user2 = User(name="John", email="john@gmail.com")
    user3 = User(name="Clement", email="clement@gmail.com")
    user4 = User(name="Christine", email="Christine@gmail.com")
    user5 = User(name="Amanda", email="Amanda@gmail.com")

    #sample detination
    dest1 = Destination(name="Zanzibar", country="Tanzania",continent="Africa")
    dest2 = Destination(name="Bali", country="Indonesia", continent="Asia")
    dest3 = Destination(name="Santorini", country="Greece", continent="Europe")
    dest4 = Destination(name="Cape Town", country="South Africa", continent="Africa")
    dest5 = Destination(name="Kyoto", country="Japan", continent="Asia")

    session.add_all([user1, user2, user3, user4, user5, dest1, dest2, dest3, dest4, dest5])
    session.commit()

    trip1 = Trip(
        user_id=user1.id,destination_id=dest1.id,
        start_date=date(2025, 11, 8), end_date=date(2025, 11,15),
        notes="Relaxing beach vacation"
    )
    trip2 = Trip(
        user_id=user2.id, destination_id=dest2.id,
        start_date=date(2025, 12, 1), end_date=date(2025, 12, 10),
        notes="Cultural exploration and surfing"
    )
    trip3 = Trip(
        user_id=user3.id, destination_id=dest3.id,
        start_date=date(2026, 1, 5), end_date=date(2026, 1, 12),
        notes="Birthday celebration with friends"
    )
    trip4 = Trip(
        user_id=user4.id, destination_id=dest4.id,
        start_date=date(2025, 9, 20), end_date=date(2025, 9, 27),
        notes="Adventure and sightseeing"
    )
    trip5 = Trip(
        user_id=user5.id, destination_id=dest5.id,
        start_date=date(2025, 10, 15), end_date=date(2025, 10, 22),
        notes="Historical temples and nature walks"
    )
   
    session.add_all([trip1, trip2, trip3, trip4, trip5])
    session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()    