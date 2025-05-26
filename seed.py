from app.database import session, Base, engine
from app.models import User, Destination, Trip
from datetime import date

Base.metadata.create_all(engine)


def seed():
    #sample users
    user1 = User(
        name="Esther",
        email="esther@gmail.com"
    )
    user2 = User(
        name="John",
        email="john@gmail.com"
    )
    #sample detination
    dest1 = Destination(name="Zanzibar", country="Tanzania",continent="Africa")
    dest2 = Destination(name="Bali", country="Indonesia", continent="Asia")

    session.add_all([user1, user2, dest1, dest2])
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
   
    session.add_all([trip1, trip2])
    session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()    