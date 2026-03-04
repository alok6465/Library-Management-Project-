# Code Snippets for Blackbook

## 1. APPLICATION ENTRY POINT (run.py)

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 2. CONFIGURATION (config.py)

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'library-secret-key-2024'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'library.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
```

---

## 3. DATABASE MODELS (models.py)

### User Model
```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prn_number = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    
    loans = db.relationship('Loan', backref='borrower', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### Book Model
```python
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    thumbnail = db.Column(db.String(500), nullable=True)
    copies_total = db.Column(db.Integer, nullable=False, default=1)
    copies_available = db.Column(db.Integer, nullable=False, default=1)
    is_virtual = db.Column(db.Boolean, nullable=False, default=False)
    pdf_file_path = db.Column(db.String(500), nullable=True)
    
    loans = db.relationship('Loan', backref='book', lazy='dynamic')
```

### Loan Model
```python
from datetime import datetime, timedelta

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    
    @property
    def is_overdue(self):
        return self.return_date is None and datetime.utcnow() > self.due_date
    
    @property
    def fine_amount(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * 5.0
        elif self.is_overdue:
            days_late = (datetime.utcnow() - self.due_date).days
            return days_late * 5.0
        return 0.0
```

### Festival Model
```python
class Festival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    video_path = db.Column(db.String(500), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    creator = db.relationship('User', foreign_keys=[created_by], backref='festivals')
```

---

## 4. KEY ROUTES (routes.py)

### Student Dashboard
```python
@bp.route('/student-dashboard')
@login_required
def student_dashboard():
    books = Book.query.all()
    my_loans = Loan.query.filter_by(user_id=current_user.id, return_date=None).all()
    
    # Get upcoming festival
    upcoming_festival = Festival.query.filter(
        Festival.is_active == True,
        Festival.date >= datetime.utcnow().date()
    ).order_by(Festival.date.asc()).first()
    
    return render_template('main/dashboard_student_modern.html',
                         books=books, 
                         my_loans=my_loans,
                         upcoming_festival=upcoming_festival)
```

### Borrow Book
```python
@bp.route('/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if book.copies_available <= 0:
        flash('Sorry, this book is currently not available.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Check 2-book limit
    current_loans = Loan.query.filter_by(user_id=current_user.id, return_date=None).count()
    if current_loans >= 2:
        flash('You can only borrow maximum 2 books at a time.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Create new loan
    loan = Loan(user_id=current_user.id, book_id=book_id)
    book.copies_available -= 1
    
    db.session.add(loan)
    db.session.commit()
    
    flash(f'Successfully borrowed "{book.title}"', 'success')
    return redirect(url_for('main.dashboard'))
```

### Search Algorithm
```python
@bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    if query:
        # Strategy 1: Category matching
        category_books = Book.query.filter(Book.category.ilike(f'%{query}%')).all()
        
        # Strategy 2: Exact matches in title/author
        exact_books = Book.query.filter(
            or_(
                Book.title.ilike(f'%{query}%'),
                Book.author.ilike(f'%{query}%')
            )
        ).all()
        
        # Combine results
        books = category_books + exact_books
        
        # Remove duplicates
        seen = set()
        unique_books = []
        for book in books:
            if book.id not in seen:
                seen.add(book.id)
                unique_books.append(book)
        
        books = unique_books
    else:
        books = []
    
    return render_template('main/search_results.html', books=books, query=query)
```

### Add Festival
```python
@bp.route('/add-festival', methods=['GET', 'POST'])
@login_required
def add_festival():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        date_str = request.form.get('date')
        
        # Handle image upload
        image_path = None
        image_file = request.files.get('image')
        if image_file and image_file.filename:
            from werkzeug.utils import secure_filename
            upload_dir = os.path.join(os.getcwd(), 'app', 'static', 'festivals')
            os.makedirs(upload_dir, exist_ok=True)
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(upload_dir, filename)
            image_file.save(file_path)
            image_path = f'/static/festivals/{filename}'
        
        festival = Festival(
            title=title,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            image_path=image_path,
            created_by=current_user.id
        )
        
        db.session.add(festival)
        db.session.commit()
        
        flash(f'Festival "{title}" added successfully!', 'success')
        return redirect(url_for('main.manage_festivals'))
    
    return render_template('main/add_festival.html')
```

---

## 5. TEMPLATES

### Base Template (base.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}LibraryPro{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">📚 LibraryPro</a>
            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="{{ url_for('main.dashboard') }}">Dashboard</a>
                    <a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{{ url_for('auth.student_login') }}">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Book Card Component (book_card_modern.html)
```html
<div class="book-card">
    {% if book.thumbnail %}
        <img src="{{ book.thumbnail }}" class="book-thumbnail" alt="{{ book.title }}">
    {% else %}
        <div class="book-thumbnail-placeholder">📖</div>
    {% endif %}
    
    <div class="book-info">
        <h5 class="book-title">{{ book.title }}</h5>
        <p class="book-author">{{ book.author }}</p>
        
        {% if book.is_virtual %}
            <span class="badge bg-info">Virtual</span>
        {% elif book.copies_available > 0 %}
            <span class="badge bg-success">Available</span>
        {% else %}
            <span class="badge bg-danger">Unavailable</span>
        {% endif %}
        
        <div class="book-actions mt-2">
            {% if book.is_virtual %}
                <button onclick="openPDFReader({{ book.id }}, '{{ book.title }}')" 
                        class="btn btn-sm btn-primary">
                    <i class="bi bi-book"></i> Read
                </button>
            {% elif book.copies_available > 0 %}
                <a href="{{ url_for('main.borrow_book', book_id=book.id) }}" 
                   class="btn btn-sm btn-success">
                    <i class="bi bi-bookmark-plus"></i> Borrow
                </a>
            {% endif %}
        </div>
    </div>
</div>
```

---

## 6. CSS STYLING (modern.css)

```css
/* Hero Section */
.hero-modern {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 3rem;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

/* Stat Cards */
.stat-card-modern {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.stat-card-modern:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

/* Book Cards */
.book-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.book-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.book-thumbnail {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

/* Animations */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.book-card {
    animation: slideInUp 0.6s ease-out;
}
```

---

## 7. DEPLOYMENT (build.sh)

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized')"
```

---

## 8. DEPLOYMENT (Procfile)

```
web: gunicorn run:app
```

---

## 9. EXCEL EXPORT (excel_export.py)

```python
import openpyxl
from datetime import datetime
import os

def create_excel_exports():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_dir = 'excel_exports'
    os.makedirs(export_dir, exist_ok=True)
    
    # Create workbook
    wb = openpyxl.Workbook()
    
    # Users sheet
    ws_users = wb.active
    ws_users.title = 'Users'
    ws_users.append(['ID', 'PRN', 'Name', 'Email', 'Role'])
    
    users = User.query.all()
    for user in users:
        ws_users.append([user.id, user.prn_number, user.name, user.email, user.role])
    
    # Save file
    filename = f'Library_Export_{timestamp}.xlsx'
    filepath = os.path.join(export_dir, filename)
    wb.save(filepath)
    
    return {'success': True, 'filename': filename}
```

---

## 10. AUTHENTICATION (auth/routes.py)

```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.auth import bp
from app.models import User

@bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        prn = request.form.get('prn_number')
        password = request.form.get('password')
        
        user = User.query.filter_by(prn_number=prn, role='student').first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.student_dashboard'))
        else:
            flash('Invalid PRN or password', 'danger')
    
    return render_template('auth/student_login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.index'))
```

---

**END OF CODE SNIPPETS**

Total Pages: ~15-20 pages when formatted for blackbook
