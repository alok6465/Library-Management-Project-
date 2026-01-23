from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("Adding new book system columns to database...")
        
        # Add new columns to book table
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE book ADD COLUMN is_new_book BOOLEAN DEFAULT 1"))
            conn.execute(text("ALTER TABLE book ADD COLUMN new_book_expires DATETIME"))
            conn.execute(text("ALTER TABLE book ADD COLUMN is_prebooking BOOLEAN DEFAULT 0"))
            conn.execute(text("ALTER TABLE book ADD COLUMN prebooking_starts DATETIME"))
            conn.execute(text("ALTER TABLE book ADD COLUMN prebooking_slots INTEGER DEFAULT 0"))
            conn.execute(text("ALTER TABLE book ADD COLUMN prebooking_taken INTEGER DEFAULT 0"))
            conn.execute(text("ALTER TABLE book ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            conn.commit()
        
        print("New book system columns added successfully!")
        
        # Create PreBooking table
        with db.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pre_booking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    booked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) NOT NULL DEFAULT 'active',
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (book_id) REFERENCES book (id)
                )
            """))
            conn.commit()
        
        print("PreBooking table created successfully!")
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Migration error: {str(e)}")
        print("This might be normal if columns already exist.")