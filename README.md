# LibraryPro - Professional Library Management System

A modern, responsive Flask-based library management system with role-based access control, featuring a professional UI/UX design.

## Features

- **User Authentication**: Secure login/logout with role-based access (Student/Admin)
- **Student Features**: Browse books, borrow/return books, track due dates
- **Admin Features**: Manage books, track all loans, handle overdue books
- **Modern UI**: Professional design with Bootstrap 5 and custom CSS
- **Responsive Design**: Mobile-first approach for all devices
- **Search Functionality**: Search books by title and author
- **Fine Calculation**: Automatic fine calculation for overdue books

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: Bootstrap 5, Custom CSS, Bootstrap Icons
- **Database**: SQLite (development), easily configurable for PostgreSQL/MySQL
- **Security**: CSRF protection, password hashing, session management

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pro-library-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
# Windows
set FLASK_APP=run.py
set FLASK_ENV=development

# macOS/Linux
export FLASK_APP=run.py
export FLASK_ENV=development
```

### 5. Initialize Database
```bash
# Initialize migration repository (run once)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration to database
flask db upgrade
```

### 6. Create Sample Users and Books
```bash
python create_sample_data.py
```

This will create:
- **120 Students** with PRN numbers (PRN2024001 to PRN2024120)
- **5 Administrators** with PRN numbers (ADM2024001 to ADM2024005)
- **20 Sample Books** for the library

The script will display sample login credentials after creation.



### 7. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Login System

### Authentication Method
- **PRN Number**: College PRN (e.g., PRN2024001 for students, ADM2024001 for admins)
- **Password**: Mother's Name + Date of Birth (e.g., Sunita15081995)

### Sample Login Credentials

**Students (120 total):**
- PRN: PRN2024001 | Password: [MotherName][DDMMYYYY]
- PRN: PRN2024002 | Password: [MotherName][DDMMYYYY]
- ... (Run create_sample_data.py to see all credentials)

**Administrators (5 total):**
- PRN: ADM2024001 | Password: [MotherName][DDMMYYYY]
- PRN: ADM2024002 | Password: [MotherName][DDMMYYYY]
- ... (Run create_sample_data.py to see all credentials)

### Password Format Examples
- Mother's Name: "Sunita", DOB: "15/08/1995" → Password: "Sunita15081995"
- Mother's Name: "Priya", DOB: "03/12/1998" → Password: "Priya03121998"

## Project Structure

```
pro-library-system/
├── app/
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── static/css/style.css     # Custom CSS
│   ├── templates/               # HTML templates
│   ├── auth/                    # Authentication blueprint
│   └── main/                    # Main application blueprint
├── migrations/                  # Database migrations
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Usage Guide

### For Students
1. Login with PRN number and password (MotherName+DOB)
2. View personal dashboard with borrowed books
3. Browse all available books in the library
4. Search books by title or author
5. Borrow available books (14-day loan period)
6. Extend loan period by 7 days
7. Return books before due date to avoid fines
8. Track due dates and overdue status

### For Administrators
1. Login with admin PRN and password
2. View comprehensive dashboard with statistics
3. **User Management:**
   - View all 120 students + 5 admins
   - Search users by name, PRN, or email
   - View detailed user information and loan history
4. **Book Management:**
   - Add new books to the library
   - Delete books (if no active loans)
   - Monitor book availability
5. **Loan Management:**
   - Track all active loans
   - Monitor overdue books and fines
   - Process book returns
   - Extend loan periods
6. **Data Tables:**
   - Responsive tables with all user and book data
   - Search functionality across all data
   - Export capabilities for reports

## Database Schema

### User Model
- `id`: Primary key
- `prn_number`: College PRN number (unique)
- `username`: System username
- `email`: User email
- `name`: Full name
- `mother_name`: Mother's name (for password)
- `dob`: Date of birth (DDMMYYYY format)
- `phone`: Contact number
- `address`: Home address
- `password_hash`: Hashed password
- `role`: 'student' or 'admin'

### Book Model
- `id`: Primary key
- `title`: Book title
- `author`: Book author
- `copies_total`: Total copies owned
- `copies_available`: Available copies

### Loan Model
- `id`: Primary key
- `user_id`: Foreign key to User
- `book_id`: Foreign key to Book
- `issue_date`: When book was borrowed
- `due_date`: When book is due (14 days from issue)
- `return_date`: When book was returned (nullable)

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)

### Database Configuration
The system uses SQLite by default. For production, update `config.py`:

```python
# For PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/library_db'

# For MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/library_db'
```

## Security Features

- CSRF protection on all forms
- Password hashing using Werkzeug
- Session management with Flask-Login
- Role-based access control
- Input validation and sanitization

## Customization

### Styling
- Modify `app/static/css/style.css` for custom styling
- Update color variables in CSS `:root` section
- Add custom Bootstrap themes

### Features
- Extend models in `app/models.py`
- Add new routes in blueprints
- Create additional templates

## Troubleshooting

### Common Issues

1. **Database not found**: Run `flask db upgrade`
2. **Import errors**: Ensure virtual environment is activated
3. **Permission denied**: Check file permissions
4. **Port already in use**: Change port in `run.py`

### Reset Database
```bash
# Remove existing database and migrations
rm -rf migrations/ app.db

# Reinitialize
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please create an issue in the repository or contact the development team.