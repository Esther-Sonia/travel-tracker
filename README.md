# 🌍 Travel Tracker CLI App

Welcome to the Travel Tracker – your personal travel journal in the command line! This CLI application helps globetrotters log, organize, and analyze their travel experiences with ease.

---

## ✨ Key Features

✈️ Add a new trip with destination, country, continent, and travel dates

🗓️ View upcoming and completed trips

🧾 Add optional notes to your trips

📊 View travel statistics (countries and continents visited)

👤 Create and log in as a user with name and email

🗑️ Delete trips

📋 View your profile info (name, email, account creation date)

---


## 🛠️ Tech Stack

- **Python**
- **SQLAlchemy** (ORM)
- **SQLite** (default local database)
- **Alembic** (for database migrations)

## 📦 Project Structure

````
travel-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   ├── migration/
│   │   ├── env.py
│   │   ├── versions
├── main.py
├── seed.py
├── alembic.ini
├── README.md
├── .gitignore
````

## 🧪 How to Run

1. **Clone the Repository:**

```bash
git clone https://github.com/yourusername/travel-tracker-cli.git
cd travel-tracker-cli


Set Up Environment:

Ensure you have Python installed. Then install dependencies:

pip install -r requirements.txt

Run the app


🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request
