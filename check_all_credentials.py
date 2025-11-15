from app import create_app
from app.models import User

app = create_app()

with app.app_context():
    # Get all students
    students = User.query.filter_by(role='student').order_by(User.prn_number).all()
    admins = User.query.filter_by(role='admin').order_by(User.prn_number).all()
    
    print("=== ALL STUDENTS ===")
    for student in students:
        password = f"{student.mother_name}{student.dob}"
        print(f"PRN: {student.prn_number} | Password: {password} | Name: {student.name}")
    
    print("\n=== ALL ADMINS ===")
    for admin in admins:
        password = f"{admin.mother_name}{admin.dob}"
        print(f"PRN: {admin.prn_number} | Password: {password} | Name: {admin.name}")
    
    print(f"\nTotal Students: {len(students)}")
    print(f"Total Admins: {len(admins)}")