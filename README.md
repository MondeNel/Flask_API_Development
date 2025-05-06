# Flask_API_Development

A simple RESTful API built with Flask, SQLAlchemy, and Flask-RESTful to manage user data. It supports creating, reading, updating, and deleting users, and logs all changes to a CSV file (`users.csv`) for real-time tracking and transparency.

---

## 📦 Features

- Add new users
- Get all users or individual user details
- Update user information via PATCH
- Delete users and see updated user list
- Log all user data in a live-updated `users.csv` file

---

## 🔧 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/MondeNel/Flask_API_Development.git
cd Flask_API_Development

``` 

2. Create and activate a virtual environment (optional but recommended):

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

3. Install dependencies:

```bash
# Create
pip install -r requirements.txt
```

4. 🚀 Running the Application
```bash
python app.py
```

The server will start on: http://localhost:5000

| Method | Endpoint          | Description               |
| ------ | ----------------- | ------------------------- |
| GET    | `/api/users`      | Get all users             |
| POST   | `/api/users`      | Create a new user         |
| GET    | `/api/users/<id>` | Get a specific user       |
| PATCH  | `/api/users/<id>` | Update specific user data |
| DELETE | `/api/users/<id>` | Delete a user             |

### 🧪 Use Postman, Insomnia, Thunder Client (VS Code extension), or any HTTP client to test these endpoints.



#### 🧾 Why CSV Logging?
We added a users.csv file that updates automatically every time the user database changes. This file serves multiple purposes:

✅ Real-time backup of the current state of users

🔍 Easy inspection of data changes during development

📈 External sync possibility with tools like Excel or Google Sheets

📂 Keeps track of id, name, email in plain-text format


