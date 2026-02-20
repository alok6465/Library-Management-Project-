from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
        with db.engine.connect() as conn:
            # Create new table with correct schema
            conn.execute(text("""
                CREATE TABLE festival_new (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    image_path VARCHAR(500),
                    video_url VARCHAR(500),
                    video_path VARCHAR(500),
                    created_by INTEGER NOT NULL,
                    created_at DATETIME NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    FOREIGN KEY(created_by) REFERENCES user(id)
                )
            """))
            
            # Copy data from old table
            conn.execute(text("""
                INSERT INTO festival_new 
                SELECT id, title, description, date, image_path, video_url, video_path, 
                       user_id, created_at, is_active 
                FROM festival
            """))
            
            # Drop old table
            conn.execute(text("DROP TABLE festival"))
            
            # Rename new table
            conn.execute(text("ALTER TABLE festival_new RENAME TO festival"))
            
            conn.commit()
        print("Festival table fixed successfully!")
    except Exception as e:
        print(f"Error: {e}")
