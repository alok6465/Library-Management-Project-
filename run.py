import os
from app import create_app
from app.extensions import db
from app.models import User, Book, Loan

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'Loan': Loan}

# Initialize database tables and create demo data
with app.app_context():
    try:
        db.create_all()
        print(f"Database initialized. Current user count: {User.query.count()}")
        
        # Create demo data if database is empty
        if User.query.count() == 0:
            print("No users found. Creating demo data...")
        import random
        
        # Sample data for realistic names
        first_names = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
                      'Ananya', 'Fatima', 'Ira', 'Prisha', 'Anvi', 'Riya', 'Navya', 'Diya', 'Pihu', 'Myra',
                      'Rahul', 'Priya', 'Amit', 'Sneha', 'Vikash', 'Anita', 'Rohit', 'Kavya', 'Suresh', 'Pooja']
        
        last_names = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel', 'Shah', 'Jain', 'Agarwal', 'Bansal']
        
        mother_names = ['Sunita', 'Priya', 'Kavita', 'Meera', 'Sita', 'Geeta', 'Radha', 'Shanti', 'Lata', 'Maya']
        
        courses = ['BSC IT', 'BSC CS', 'BTech Computer Science', 'BTech Data Science']
        years = ['1st', '2nd', '3rd', '4th', '5th']
        
            print('Creating 200 students...')
        # Create 200 students
        for i in range(1, 201):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            mother_name = random.choice(mother_names)
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.randint(1995, 2005)
            dob = f"{day:02d}{month:02d}{year}"
            
            student = User(
                prn_number=f'PRN2024{i:03d}',
                username=f'student{i}',
                name=f'{first_name} {last_name}',
                email=f'student{i}@college.edu',
                mother_name=mother_name,
                dob=dob,
                phone=f'98765{i+10000:05d}',
                address=f'Address {i}, City, State',
                role='student',
                year=random.choice(years),
                course=random.choice(courses)
            )
            student.set_password(mother_name + dob)
            db.session.add(student)
        
        print('Creating 5 admins...')
        # Create 5 admins with fixed credentials
        admin_data = [
            ('ADM2024001', 'Dr. Admin', 'Usha', '25061975'),
            ('ADM2024002', 'Prof. Admin', 'Lata', '12041978'),
            ('ADM2024003', 'Mr. Admin', 'Sita', '15031980'),
            ('ADM2024004', 'Ms. Admin', 'Maya', '08121982'),
            ('ADM2024005', 'Dr. Head Admin', 'Radha', '22051975')
        ]
        
        for prn, name, mother_name, dob in admin_data:
            admin = User(
                prn_number=prn,
                username=prn.lower(),
                name=name,
                email=f'{prn.lower()}@college.edu',
                mother_name=mother_name,
                dob=dob,
                phone='9999999999',
                address='Admin Office',
                role='admin'
            )
            admin.set_password(mother_name + dob)
            db.session.add(admin)
        
        print('Creating sample books...')
        # Create sample books
        books_data = [
            ('Python Programming', 'John Smith', 5), ('Data Structures', 'Robert Johnson', 4),
            ('Web Development', 'Sarah Wilson', 6), ('Database Systems', 'Mike Brown', 3),
            ('Computer Networks', 'Lisa Davis', 4), ('Operating Systems', 'David Miller', 5),
            ('Software Engineering', 'Emma Taylor', 3), ('Machine Learning', 'James Anderson', 4),
            ('Artificial Intelligence', 'Maria Garcia', 2), ('Cybersecurity', 'Chris Wilson', 3)
        ]
        
        for title, author, copies in books_data:
            book = Book(title=title, author=author, copies_total=copies, copies_available=copies)
            db.session.add(book)
        
        db.session.commit()
        print('✅ Complete library system created with 200 students, 5 admins, and 10 books!')
        print(f"Final user count: {User.query.count()}")
        
        # Print first admin credentials for debugging
        first_admin = User.query.filter_by(role='admin').first()
        if first_admin:
            print(f"First admin: PRN={first_admin.prn_number}, Password={first_admin.mother_name + first_admin.dob}")
    
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)