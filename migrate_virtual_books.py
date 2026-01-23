from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("Adding virtual book columns to database...")
        
        # Add new columns to book table
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE book ADD COLUMN is_virtual BOOLEAN DEFAULT 0"))
            conn.execute(text("ALTER TABLE book ADD COLUMN pdf_file_path VARCHAR(500)"))
            conn.execute(text("ALTER TABLE book ADD COLUMN virtual_price FLOAT DEFAULT 0.0"))
            conn.execute(text("ALTER TABLE book ADD COLUMN download_price FLOAT DEFAULT 11.0"))
            conn.commit()
        
        print("Virtual book columns added successfully!")
        
        # Create VirtualBookPurchase table
        with db.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS virtual_book_purchase (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    purchase_type VARCHAR(20) NOT NULL,
                    amount_paid FLOAT NOT NULL DEFAULT 0.0,
                    purchase_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    payment_status VARCHAR(20) NOT NULL DEFAULT 'completed',
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (book_id) REFERENCES book (id)
                )
            """))
            conn.commit()
        
        print("VirtualBookPurchase table created successfully!")
        
        # Add some sample virtual books
        with db.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO book (title, author, category, is_virtual, virtual_price, download_price, copies_total, copies_available)
                VALUES 
                ('Python Programming Guide', 'John Doe', 'Programming', 1, 0.0, 11.0, 1, 1),
                ('Web Development Basics', 'Jane Smith', 'Web Development', 1, 0.0, 15.0, 1, 1),
                ('Data Science Handbook', 'Mike Johnson', 'Data Science', 1, 0.0, 20.0, 1, 1)
            """))
            conn.commit()
        
        print("Sample virtual books added!")
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Migration error: {str(e)}")
        print("This might be normal if columns already exist.")