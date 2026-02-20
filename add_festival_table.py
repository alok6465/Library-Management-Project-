"""Add Festival model

Run this to add festival table to database
"""

from app import create_app, db

app = create_app()

with app.app_context():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'festival' not in tables:
        with db.engine.connect() as conn:
            conn.execute(db.text('''
                CREATE TABLE festival (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    image_path VARCHAR(500),
                    video_url VARCHAR(500),
                    created_by INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (created_by) REFERENCES user(id)
                )
            '''))
            conn.commit()
        print("Festival table created successfully!")
    else:
        print("Festival table already exists!")
