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


def update_trip(user_id):
    trip_id = input("Enter the Trip ID you want to update: ").strip()
    trip = session.query(Trip).filter_by(id=trip_id, user_id=user_id).first()  #here fetch the trip you want to update
    if not trip:
        print("Trip not found.")
        return

    print(f"\nEditing Trip to {trip.destination.name}, {trip.destination.country}")
    
    # Prompt for new details
    new_name = input(f"New destination name (or press Enter to keep '{trip.destination.name}'): ").strip()
    new_country = input(f"New country (or press Enter to keep '{trip.destination.country}'): ").strip()
    new_continent = input(f"New continent (or press Enter to keep '{trip.destination.continent}'): ").strip()
     
     #update start and end dates if provided
    start_date_input = input(f"New start date (DD-MM-YYYY) or press Enter to keep '{trip.start_date.strftime('%d-%m-%Y')}': ").strip()
    if start_date_input:
        try:
            trip.start_date = datetime.strptime(start_date_input, "%d-%m-%Y").date()
        except ValueError:
            print("Invalid date format. Keeping original start date.")

    end_date_input = input(f"New end date (DD-MM-YYYY) or press Enter to keep '{trip.end_date.strftime('%d-%m-%Y')}': ").strip()
    if end_date_input:
        try:
            new_end_date = datetime.strptime(end_date_input, "%d-%m-%Y").date()
            if new_end_date < trip.start_date:
                print("End date cannot be before start date. Keeping original end date.")
            else:
                trip.end_date = new_end_date
        except ValueError:
            print("Invalid date format. Keeping original end date.")

    # Update notes if new ones are provided
    new_notes = input("New notes (or press Enter to keep current notes): ").strip()
    if new_notes:
        trip.notes = new_notes


    new_destination_name = new_name or trip.destination.name
    new_country = new_country or trip.destination.country
    new_continent = new_continent or trip.destination.continent

    # Check if the destination exists already
    destination = session.query(Destination).filter_by(
        name=new_destination_name,
        country=new_country,
        continent=new_continent
    ).first()

    if not destination:
        destination = Destination(name=new_destination_name, country=new_country, continent=new_continent)
        session.add(destination)
        session.commit()

    trip.destination_id = destination.id

    try:
        session.commit()
        print("Trip updated successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error updating trip: {e}")



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

def update_user_email(user_id):
    print("\n--- Update User Email ---")
    user = session.query(User).filter_by(id=user_id).first()

    if user:
        print(f"Current Email: {user.email}")
        new_email = input("Enter the new email address: ").strip()

        if new_email == "":
            print("Email cannot be empty.")
            return

        user.email = new_email
        session.commit()
        print("Email updated successfully.")
    else:
        print("User not found.")

def delete_user_account(user_id):
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        print("User not found.")
        return

    confirm = input("Are you sure you want to delete your account? This will remove all your trips too. (yes/no): ").strip().lower()
    if confirm == "yes":
        
        session.query(Trip).filter_by(user_id=user_id).delete()
        session.delete(user)
        try:
            session.commit()
            print("Your account and all trips have been deleted. Goodbye!")
            exit()  
        except Exception as e:
            session.rollback()
            print(f"Error deleting account: {e}")
    else:
        print("Account deletion cancelled.")



def menu(user_id):
    while True:
        print("""
--- 🌍 My Travel Dashboard ---
1. Add a new trip
2. View upcoming trips
3. View completed trips
4. Update a trip
5. Delete a trip
6. Show travel stats
7. View profile info
8. Update profile inf0
9. Delete account
10. Exit                         
            

""")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            new_trip(user_id)
        elif choice == '2':
            view_upcoming_trips(user_id)
        elif choice == '3':
            view_completed_trips(user_id)
        elif choice == '4':
            update_trip(user_id)    
        elif choice == '5':
            delete_trip(user_id)
        elif choice == '6':
            show_travel_stats(user_id)
        elif choice == '7':
            view_profile_info(user_id)
        elif choice == '8':
            update_user_email(user_id)
        elif choice == '9':
            delete_user_account(user_id)
        elif choice == '10':
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
  


            

        



     


