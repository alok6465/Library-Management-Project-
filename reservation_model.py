# Add this to models.py after the existing models

class BookReservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, expired, fulfilled
    
    user = db.relationship('User', backref='reservations')
    book = db.relationship('Book', backref='reservations')
    
    def __init__(self, **kwargs):
        super(BookReservation, self).__init__(**kwargs)
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)
    
    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at and self.status == 'active'
    
    @property
    def hours_remaining(self):
        if self.status == 'active':
            remaining = self.expires_at - datetime.utcnow()
            return max(0, remaining.total_seconds() / 3600)
        return 0
    
    def __repr__(self):
        return f'<BookReservation {self.id}: {self.user.name} - {self.book.title}>'