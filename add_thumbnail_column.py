"""Add thumbnail column to books

Run this script to add thumbnail column to existing database
"""

from app import create_app, db
from app.models import Book

app = create_app()

with app.app_context():
    # Check if column exists
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('book')]
    
    if 'thumbnail' not in columns:
        # Add thumbnail column
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE book ADD COLUMN thumbnail VARCHAR(500)'))
            conn.commit()
        print("Thumbnail column added successfully!")
    else:
        print("Thumbnail column already exists!")
