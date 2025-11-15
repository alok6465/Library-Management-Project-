from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    # Check if user already exists
    existing_user = User.query.filter_by(prn_number='PRN2024001').first()
    
    if existing_user:
        # Update existing user
        existing_user.mother_name = 'Seema'
        existing_user.dob = '03121995'
        existing_user.set_password('Seema03121995')
        print("Updated existing user PRN2024001")
    else:
        # Create new user
        user = User(
            prn_number='PRN2024001',
            username='student1',
            name='Test Student',
            email='student1@college.edu',
            mother_name='Seema',
            dob='03121995',
            phone='9876543210',
            address='Test Address',
            role='student',
            year='2nd',
            course='BSC IT'
        )
        user.set_password('Seema03121995')
        db.session.add(user)
        print("Created new user PRN2024001")
    
    db.session.commit()
    print("User PRN2024001 with password Seema03121995 is ready!")
    print("You can now login with these credentials")