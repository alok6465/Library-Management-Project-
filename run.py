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
            
            print('Creating Mumbai University BSC CS/IT textbooks...')
            # Mumbai University BSC CS/IT Textbooks
            books_data = [
                # BSC CS Semester 1
                ('Programming with C', 'E. Balagurusamy', 'Programming', 'Sem 1', 'BSC CS', '978-0070141698', 5),
                ('Digital Electronics', 'R.P. Jain', 'Electronics', 'Sem 1', 'BSC CS', '978-0070648906', 4),
                ('Mathematics I', 'B.S. Grewal', 'Mathematics', 'Sem 1', 'BSC CS', '978-8173716751', 6),
                ('Computer Fundamentals', 'P.K. Sinha', 'Computer Science', 'Sem 1', 'BSC CS', '978-8176567640', 4),
                
                # BSC CS Semester 2
                ('Data Structures Using C', 'Reema Thareja', 'Programming', 'Sem 2', 'BSC CS', '978-0198099307', 5),
                ('Computer Organization', 'Carl Hamacher', 'Computer Architecture', 'Sem 2', 'BSC CS', '978-0073380650', 3),
                ('Mathematics II', 'B.V. Ramana', 'Mathematics', 'Sem 2', 'BSC CS', '978-0070681910', 4),
                ('Environmental Studies', 'Erach Bharucha', 'Environmental Science', 'Sem 2', 'BSC CS', '978-8173716638', 5),
                
                # BSC CS Semester 3
                ('Object Oriented Programming with C++', 'E. Balagurusamy', 'Programming', 'Sem 3', 'BSC CS', '978-0070634381', 4),
                ('Database Management Systems', 'Raghu Ramakrishnan', 'Database', 'Sem 3', 'BSC CS', '978-0072465631', 5),
                ('Computer Graphics', 'Donald Hearn', 'Graphics', 'Sem 3', 'BSC CS', '978-0131496705', 3),
                ('Discrete Mathematics', 'Kenneth Rosen', 'Mathematics', 'Sem 3', 'BSC CS', '978-0073383095', 4),
                
                # BSC CS Semester 4
                ('Java Programming', 'Joyce Farrell', 'Programming', 'Sem 4', 'BSC CS', '978-1337397070', 5),
                ('Operating Systems', 'Abraham Silberschatz', 'Operating Systems', 'Sem 4', 'BSC CS', '978-1118063330', 4),
                ('Computer Networks', 'Andrew Tanenbaum', 'Networking', 'Sem 4', 'BSC CS', '978-0132126953', 4),
                ('Software Engineering', 'Roger Pressman', 'Software Engineering', 'Sem 4', 'BSC CS', '978-0078022128', 3),
                
                # BSC CS Semester 5
                ('Web Technologies', 'Uttam K. Roy', 'Web Development', 'Sem 5', 'BSC CS', '978-0198072928', 4),
                ('Artificial Intelligence', 'Stuart Russell', 'AI/ML', 'Sem 5', 'BSC CS', '978-0136042594', 3),
                ('Theory of Computation', 'Michael Sipser', 'Theory', 'Sem 5', 'BSC CS', '978-1133187790', 2),
                ('Mobile Application Development', 'Wei-Meng Lee', 'Mobile Development', 'Sem 5', 'BSC CS', '978-1118301821', 4),
                
                # BSC CS Semester 6
                ('Machine Learning', 'Tom Mitchell', 'AI/ML', 'Sem 6', 'BSC CS', '978-0070428072', 3),
                ('Information Security', 'Mark Stamp', 'Security', 'Sem 6', 'BSC CS', '978-0471738480', 4),
                ('Project Management', 'K. Nagarajan', 'Management', 'Sem 6', 'BSC CS', '978-8122434987', 3),
                
                # BSC IT Semester 1
                ('Programming Logic and Design', 'Joyce Farrell', 'Programming', 'Sem 1', 'BSC IT', '978-1337102070', 5),
                ('Computer Systems Architecture', 'M. Morris Mano', 'Computer Architecture', 'Sem 1', 'BSC IT', '978-0131755635', 4),
                ('Business Communication', 'Meenakshi Raman', 'Communication', 'Sem 1', 'BSC IT', '978-0198066415', 4),
                ('Applied Mathematics I', 'P.N. Wartikar', 'Mathematics', 'Sem 1', 'BSC IT', '978-8184871647', 5),
                
                # BSC IT Semester 2
                ('Object Oriented Programming', 'Robert Lafore', 'Programming', 'Sem 2', 'BSC IT', '978-0672323089', 4),
                ('Microprocessor Architecture', 'Barry B. Brey', 'Computer Architecture', 'Sem 2', 'BSC IT', '978-0135026458', 3),
                ('Applied Mathematics II', 'H.K. Dass', 'Mathematics', 'Sem 2', 'BSC IT', '978-8121926942', 4),
                ('Digital Systems and Logic Design', 'Charles Roth', 'Electronics', 'Sem 2', 'BSC IT', '978-0495668046', 4),
                
                # BSC IT Semester 3
                ('Data Structures and Files', 'Michael J. Folk', 'Programming', 'Sem 3', 'BSC IT', '978-0201557138', 4),
                ('Computer Networks and Data Communication', 'Behrouz Forouzan', 'Networking', 'Sem 3', 'BSC IT', '978-0073376226', 5),
                ('Software Engineering', 'Ian Sommerville', 'Software Engineering', 'Sem 3', 'BSC IT', '978-0133943030', 4),
                ('Applied Mathematics III', 'Grewal B.S.', 'Mathematics', 'Sem 3', 'BSC IT', '978-8173716836', 3),
                
                # BSC IT Semester 4
                ('Database Management Systems', 'Elmasri & Navathe', 'Database', 'Sem 4', 'BSC IT', '978-0133970777', 5),
                ('Internet Programming', 'Deitel & Deitel', 'Web Development', 'Sem 4', 'BSC IT', '978-0132151009', 4),
                ('Operating Systems', 'William Stallings', 'Operating Systems', 'Sem 4', 'BSC IT', '978-0133591620', 4),
                ('Numerical and Statistical Methods', 'P. Kandasamy', 'Mathematics', 'Sem 4', 'BSC IT', '978-8121926942', 3),
                
                # BSC IT Semester 5
                ('Software Project Management', 'Bob Hughes', 'Management', 'Sem 5', 'BSC IT', '978-0077122799', 3),
                ('Internet of Things', 'Arshdeep Bahga', 'IoT', 'Sem 5', 'BSC IT', '978-8173719547', 4),
                ('Advanced Web Programming', 'Chris Bates', 'Web Development', 'Sem 5', 'BSC IT', '978-0470057735', 4),
                ('Enterprise Java', 'Kathy Sierra', 'Programming', 'Sem 5', 'BSC IT', '978-0596009205', 3),
                
                # BSC IT Semester 6
                ('Geographic Information System', 'Kang-tsung Chang', 'GIS', 'Sem 6', 'BSC IT', '978-0073522890', 2),
                ('ERP and Business Intelligence', 'Alexis Leon', 'Business Intelligence', 'Sem 6', 'BSC IT', '978-0070151284', 3),
                ('Cyber Security', 'Nina Godbole', 'Security', 'Sem 6', 'BSC IT', '978-8126556748', 4),
                
                # Additional Reference Books
                ('Introduction to Algorithms', 'Thomas Cormen', 'Algorithms', 'Reference', 'All Courses', '978-0262033848', 3),
                ('Design Patterns', 'Gang of Four', 'Software Design', 'Reference', 'All Courses', '978-0201633610', 2),
                ('Clean Code', 'Robert Martin', 'Programming', 'Reference', 'All Courses', '978-0132350884', 4),
                ('Computer Science Illuminated', 'Nell Dale', 'Computer Science', 'Reference', 'All Courses', '978-1284155617', 3),
                ('The Pragmatic Programmer', 'Andrew Hunt', 'Programming', 'Reference', 'All Courses', '978-0135957059', 2)
            ]
            
            for title, author, category, semester, course, isbn, copies in books_data:
                book = Book(
                    title=title, 
                    author=author, 
                    category=category,
                    semester=semester,
                    course=course,
                    isbn=isbn,
                    copies_total=copies, 
                    copies_available=copies
                )
                db.session.add(book)
            
            db.session.commit()
            print('✅ Complete library system created with 200 students, 5 admins, and 50+ Mumbai University textbooks!')
            print(f"Final user count: {User.query.count()}")
            
            # Print first admin credentials for debugging
            first_admin = User.query.filter_by(role='admin').first()
            if first_admin:
                print(f"First admin: PRN={first_admin.prn_number}, Password={first_admin.mother_name + first_admin.dob}")
        else:
            print(f"Database already has {User.query.count()} users. Skipping data creation.")
    
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)