from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE festival ADD COLUMN video_path VARCHAR(500)"))
            conn.commit()
        print("video_path column added successfully!")
    except Exception as e:
        print(f"Column might already exist or error: {e}")
