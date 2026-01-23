#!/usr/bin/env bash
# build.sh - Render deployment script

set -o errexit

pip install -r requirements.txt

# Initialize database and create users
python -c "
from app import create_app
from app.extensions import db
from app.models import User, Book
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if users exist
    if User.query.count() == 0:
        print('Creating demo users...')
        
        # Create admin
        admin = User(
            prn_number='ADM2024001',
            username='admin2024',
            name='Admin User',
            email='admin@library.com',
            mother_name='Admin',
            dob='01012000',
            phone='1234567890',
            address='Library Office',
            role='admin'
        )
        admin.set_password('Admin01012000')
        db.session.add(admin)
        
        # Create students
        students_data = [
            ('PRN2024001', 'Rahul Sharma', 'Sunita', '15081995'),
            ('PRN2024002', 'Priya Patel', 'Meera', '22031998'),
            ('PRN2024003', 'Amit Kumar', 'Geeta', '10121997'),
        ]
        
        for prn, name, mother_name, dob in students_data:
            student = User(
                prn_number=prn,
                username=prn.lower(),
                name=name,
                email=f'{prn.lower()}@college.edu',
                mother_name=mother_name,
                dob=dob,
                phone='9876543210',
                address='Demo Address',
                role='student',
                year='2nd',
                course='BSC IT'
            )
            password = mother_name + dob
            student.set_password(password)
            db.session.add(student)
        
        # Create sample books
        books_data = [
            ('Python Programming', 'John Smith', 3),
            ('Data Structures', 'Robert Johnson', 2),
            ('Web Development', 'Sarah Wilson', 4),
        ]
        
        for title, author, copies in books_data:
            book = Book(
                title=title,
                author=author,
                copies_total=copies,
                copies_available=copies,
                is_new_book=True,
                new_book_expires=datetime.utcnow() + timedelta(days=60)
            )
            db.session.add(book)
        
        db.session.commit()
        print('Demo data created successfully!')
        print('Admin Login: ADM2024001 / Admin01012000')
        print('Student Login: PRN2024001 / Sunita15081995')
    else:
        print(f'Database already has {User.query.count()} users')
"