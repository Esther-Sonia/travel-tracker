from datetime import datetime
from app.models import User, Destination, Trip
from app.database import session, Base, engine

Base.metadata.create_all(engine)

def new_trip(user_id):
    destination_name = input("Enter destination name (e.g. Diani Beach): ").strip()
    country = input("Enter destination country (e.g. Kenya): ").strip()
    continent = input("Enter continent (e.g. Africa): ").strip()

    while True:
        start_date_str = input("Enter start date (DD-MM-YYYY): ").strip()
        try:
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
            break
        except ValueError:
            print("Invalid start date format. Please use DD-MM-YYYY.")

    while True:
        end_date_str = input("Enter end date (DD-MM-YYYY): ").strip()
        try:
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
            if end_date < start_date:
                print("End date cannot be before start date. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid end date format. Please use DD-MM-YYYY.")

    notes = input("Enter any notes for the trip (optional): ").strip()

    destination = session.query(Destination).filter_by(
        name=destination_name,
        country=country,
        continent=continent
    ).first()

    if not destination:
        destination = Destination(name=destination_name, country=country, continent=continent)
        session.add(destination)
        session.commit()

    trip = Trip(
        user_id=user_id,
        destination_id=destination.id,
        start_date=start_date,
        end_date=end_date,
        notes=notes if notes else None
    )

    session.add(trip)
    session.commit()

    print(f"Trip to {destination_name} from {start_date} to {end_date} added successfully!")

def view_upcoming_trips(user_id):
    today = datetime.now().date()
    trips = session.query(Trip).filter(
        Trip.user_id == user_id,
        Trip.start_date >= today
    ).all()

    print("Upcoming Trips:")
    if trips:
        for trip in trips:
            formatted_date = trip.start_date.strftime("%d-%m-%Y")
            print(f"- ID: {trip.id} | {trip.destination.name}, {trip.destination.country} on {formatted_date}")
            if trip.notes:
                print(f"  📝 Notes: {trip.notes}")
    else:
        print("No upcoming trips found.")


def view_completed_trips(user_id):
    today = datetime.now().date()
    trips = session.query(Trip).filter(Trip.user_id == user_id, Trip.start_date <= today).all()

    print("\n🏁 Completed Trips:")
    if trips:
        for trip in trips:
            formatted_date = trip.start_date.strftime('%d-%m-%Y')
            print(f"- ID: {trip.id} | {trip.destination.name}, {trip.destination.country} on {formatted_date}")
            if trip.notes:
                print(f"  📝 Notes: {trip.notes}")
    else:
        print("No completed trips found.")


def delete_trip(user_id):
    trip_id = input("Enter the Trip ID you want to delete (e.g. 11): ").strip()
    trip = session.query(Trip).filter_by(id=trip_id, user_id=user_id).first()

    if trip:
        session.delete(trip)
        try:
            session.commit()
            print("🗑️ Trip deleted successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error deleting trip: {e}")
    else:
        print(" Trip not found.")  


def show_travel_stats(user_id):
    trips = session.query(Trip).filter_by(user_id=user_id).all()
    countries = set(trip.destination.country for trip in trips)
    continents = set(trip.destination.continent for trip in trips)

    print(f"\nCountries visited: {len(countries)}")
    print(f"Continents visited: {len(continents)}")



def view_profile_info(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        print("User not found.")
        return

    print("\n Your Travel Profile:")
    print(f"- Name: {user.name}")
    print(f"- Email: {user.email}")
    print(f"- Account Created At: {user.created_at.strftime('%d-%m-%Y %H:%M:%S')}")

def menu(user_id):
    while True:
        print("""
--- 🌍 My Travel Dashboard ---
1. Add a new trip
2. View upcoming trips
3. View completed trips
4. Delete a trip
5. Show travel stats
6. View profile info
7. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            new_trip(user_id)
        elif choice == '2':
            view_upcoming_trips(user_id)
        elif choice == '3':
            view_completed_trips(user_id)
        elif choice == '4':
            delete_trip(user_id)
        elif choice == '5':
            show_travel_stats(user_id)
        elif choice == '6':
            view_profile_info(user_id)
        elif choice == '7':
         break  
        else:
         print("Invalid choice. Try again.")

def login():
    while True:
        name = input("Enter your name to log in: ").strip()
        if name:
            break
        print("Name cannot be empty. Please try again.")

    user = session.query(User).filter_by(name=name).first()

    if not user:
        print("User not found. Creating new user...")
        while True:
            email = input("Enter your email: ").strip()
            if email:
                break
            print("Email cannot be empty. Please try again.")

        user = User(name=name, email=email)
        session.add(user)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {e}")
            return
        print(f"Welcome, {name}!Your account has been created.")

    else:
        print(f"Welcome back, {user.name}!")

    menu(user.id)


if __name__ == "__main__":
    login()
  


            

        



     


