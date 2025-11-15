from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("=== ALL STUDENT CREDENTIALS ===")
    students = User.query.filter_by(role='student').all()
    for student in students:
        password = f"{student.mother_name}{student.dob}"
        print(f"PRN: {student.prn_number} | Password: {password} | Name: {student.name}")
    
    print("\n=== ALL ADMIN CREDENTIALS ===")
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        password = f"{admin.mother_name}{admin.dob}"
        print(f"PRN: {admin.prn_number} | Password: {password} | Name: {admin.name}")