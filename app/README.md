# CloudBite Restaurant Ordering System

A cloud-based restaurant ordering platform built with Python, Flask, Google App Engine, Cloud Firestore, and Cloud SQL.

## Features

- 🍕 Menu browsing with real-time updates
- 🛒 Shopping cart functionality
- 👤 User authentication and authorization
- 📦 Order management system
- 🔥 Firestore (NoSQL) for menu items and user data
- 🗄️ Cloud SQL (PostgreSQL) for transactional order data
- 🔐 Secure authentication with password hashing
- 🚀 RESTful APIs for integration
- 📱 Responsive web interface

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Databases**: 
  - Google Cloud Firestore (NoSQL)
  - Google Cloud SQL PostgreSQL (Relational)
- **Authentication**: Firebase Admin SDK, bcrypt
- **Cloud Platform**: Google App Engine
- **Testing**: unittest
- **Version Control**: Git/GitHub

## Database Architecture

### Firestore (NoSQL)
- Menu items (flexible schema for easy updates)
- User profiles
- Order logs (for analytics)

### Cloud SQL (PostgreSQL)
- Orders table (transactional data)
- Order items table (relational integrity)

## Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd cloudbite-restaurant
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file with:
```
FLASK_SECRET_KEY=your-secret-key
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=firebase-credentials.json
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_NAME=cloudbite_orders
DB_HOST=your-sql-instance-ip
```

5. Initialize databases
```bash
python seed_database.py
python init_sql_db.py
```

6. Run the application
```bash
python main.py
```

## Running Tests

Run all unit tests:
```bash
python run_tests.py
```

Run specific test file:
```bash
python -m unittest tests.test_models
```

## API Endpoints

### Menu API
- `GET /menu/api/items` - Get all menu items

### Orders API
- `GET /orders/api/orders` - Get user's orders (requires authentication)
- `POST /orders/create` - Create new order (requires authentication)

See `/api-docs` for full documentation.

## Project Structure
```
cloudbite-restaurant/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── utils/
├── tests/
├── main.py
├── requirements.txt
├── app.yaml
└── README.md
```

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- SQL injection prevention with SQLAlchemy ORM
- CSRF protection
- Secure environment variable management

## Author

Your Name - Systems Development Coursework

## License

Educational Project