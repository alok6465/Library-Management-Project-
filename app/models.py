from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prn_number = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)  # Format: DDMMYYYY
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    
    # Academic Details
    year = db.Column(db.String(10), nullable=True)  # 1st, 2nd, 3rd, 4th, 5th
    course = db.Column(db.String(50), nullable=True)  # BSC IT, BSC CS, etc.
    
    # Activity Tracking
    total_books_borrowed = db.Column(db.Integer, default=0)
    total_extension_requests = db.Column(db.Integer, default=0)
    library_hours_this_month = db.Column(db.Float, default=0.0)
    library_hours_this_year = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    loans = db.relationship('Loan', backref='borrower', lazy='dynamic')
    library_sessions = db.relationship('LibrarySession', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    copies_total = db.Column(db.Integer, nullable=False, default=1)
    copies_available = db.Column(db.Integer, nullable=False, default=1)
    loans = db.relationship('Loan', backref='book', lazy='dynamic')
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, **kwargs):
        super(Loan, self).__init__(**kwargs)
        if not self.due_date:
            self.due_date = datetime.utcnow() + timedelta(days=14)
    
    @property
    def is_overdue(self):
        return self.return_date is None and datetime.utcnow() > self.due_date
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (datetime.utcnow() - self.due_date).days
        return 0
    
    @property
    def fine_amount(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * 1.0  # $1 per day fine
        elif self.is_overdue:
            days_late = (datetime.utcnow() - self.due_date).days
            return days_late * 1.0
        return 0.0
    
    def __repr__(self):
        return f'<Loan {self.id}: {self.borrower.username} - {self.book.title}>'

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_type = db.Column(db.String(20), nullable=False, default='all')  # 'all', 'student', 'specific'
    recipient_ids = db.Column(db.Text, nullable=True)  # Comma-separated IDs for multiple recipients
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_notices')
    
    @property
    def recipients(self):
        if self.recipient_ids:
            ids = [int(id.strip()) for id in self.recipient_ids.split(',') if id.strip()]
            return User.query.filter(User.id.in_(ids)).all()
        return []
    
    @property
    def is_new(self):
        from datetime import datetime, timedelta
        # Notice is "new" for 1.4 weeks (10 days)
        return datetime.utcnow() - self.created_date <= timedelta(days=10)
    
    @property
    def days_old(self):
        from datetime import datetime
        return (datetime.utcnow() - self.created_date).days
    
    def __repr__(self):
        return f'<Notice {self.id}: {self.title}>'

class ExtensionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    requested_days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    admin_response = db.Column(db.Text, nullable=True)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    response_date = db.Column(db.DateTime, nullable=True)
    responded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status_expires_at = db.Column(db.DateTime, nullable=True)
    
    loan = db.relationship('Loan', backref='extension_requests')
    admin = db.relationship('User', foreign_keys=[responded_by])
    
    def set_status_expiry(self):
        if self.status == 'approved':
            self.status_expires_at = datetime.utcnow() + timedelta(hours=24)
        elif self.status == 'rejected':
            self.status_expires_at = datetime.utcnow() + timedelta(days=2)
    
    def is_status_expired(self):
        return self.status_expires_at and datetime.utcnow() > self.status_expires_at
    
    def __repr__(self):
        return f'<ExtensionRequest {self.id}: {self.status}>'

class LibrarySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out = db.Column(db.DateTime, nullable=True)
    duration_hours = db.Column(db.Float, nullable=True)
    
    def calculate_duration(self):
        if self.check_out:
            delta = self.check_out - self.check_in
            self.duration_hours = delta.total_seconds() / 3600
    
    def __repr__(self):
        return f'<LibrarySession {self.id}: {self.user.name}>'