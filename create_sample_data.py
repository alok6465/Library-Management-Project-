from app import create_app
from app.extensions import db
from app.models import User, Book
import random

app = create_app()

# Sample data for realistic names
first_names = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
    'Shaurya', 'Atharv', 'Advik', 'Pranav', 'Vivek', 'Rudra', 'Shlok', 'Kian', 'Aryan', 'Kabir',
    'Ananya', 'Fatima', 'Ira', 'Prisha', 'Anvi', 'Riya', 'Navya', 'Diya', 'Pihu', 'Myra',
    'Sara', 'Aanya', 'Pari', 'Kavya', 'Khushi', 'Avni', 'Aadhya', 'Shanaya', 'Akshara', 'Veda'
]

last_names = [
    'Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel', 'Shah', 'Jain', 'Agarwal', 'Bansal',
    'Mehta', 'Malhotra', 'Chopra', 'Kapoor', 'Arora', 'Joshi', 'Saxena', 'Mittal', 'Goel', 'Tiwari'
]

mother_names = [
    'Sunita', 'Priya', 'Kavita', 'Meera', 'Sita', 'Geeta', 'Nisha', 'Pooja', 'Rekha', 'Seema',
    'Asha', 'Usha', 'Radha', 'Shanti', 'Lata', 'Maya', 'Kiran', 'Sushma', 'Vandana', 'Deepika'
]

courses = ['BSC IT', 'BSC CS', 'BTech Computer Science', 'BTech Data Science']
years = ['1st', '2nd', '3rd', '4th', '5th']

def generate_dob():
    """Generate random DOB in DDMMYYYY format"""
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1995, 2005)
    return f"{day:02d}{month:02d}{year}"

def generate_phone():
    """Generate random phone number"""
    return f"9{random.randint(100000000, 999999999)}"

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("Creating sample users...")
    
    # Create 120 Students
    students_created = []
    for i in range(1, 121):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        mother_name = random.choice(mother_names)
        dob = generate_dob()
        
        student = User(
            prn_number=f'PRN2024{i:03d}',
            username=f'student{i}',
            name=f'{first_name} {last_name}',
            email=f'student{i}@college.edu',
            mother_name=mother_name,
            dob=dob,
            phone=generate_phone(),
            address=f'{random.randint(1, 999)} Street, City-{random.randint(100000, 999999)}',
            role='student',
            year=random.choice(years),
            course=random.choice(courses)
        )
        
        password = mother_name + dob
        student.set_password(password)
        
        db.session.add(student)
        students_created.append({
            'prn': student.prn_number,
            'name': student.name,
            'password': password,
            'year': student.year,
            'course': student.course
        })
    
    # Create 5 Administrators
    admins_created = []
    admin_names = ['Rajesh Kumar', 'Sunita Sharma', 'Amit Patel', 'Neha Gupta', 'Vikash Singh']
    
    for i in range(1, 6):
        mother_name = random.choice(mother_names)
        dob = generate_dob()
        
        admin = User(
            prn_number=f'ADM2024{i:03d}',
            username=f'admin{i}',
            name=admin_names[i-1],
            email=f'admin{i}@college.edu',
            mother_name=mother_name,
            dob=dob,
            phone=generate_phone(),
            address=f'Admin Block {i}, College Campus',
            role='admin'
        )
        
        password = mother_name + dob
        admin.set_password(password)
        
        db.session.add(admin)
        admins_created.append({
            'prn': admin.prn_number,
            'name': admin.name,
            'password': password
        })
    
    # Create sample books
    books_data = [
        ('Python Programming', 'John Smith'),
        ('Data Structures and Algorithms', 'Robert Sedgewick'),
        ('Computer Networks', 'Andrew Tanenbaum'),
        ('Database Systems', 'Ramez Elmasri'),
        ('Operating Systems', 'Abraham Silberschatz'),
        ('Software Engineering', 'Ian Sommerville'),
        ('Web Development', 'Jon Duckett'),
        ('Machine Learning', 'Tom Mitchell'),
        ('Artificial Intelligence', 'Stuart Russell'),
        ('Computer Graphics', 'Donald Hearn'),
        ('Discrete Mathematics', 'Kenneth Rosen'),
        ('Linear Algebra', 'Gilbert Strang'),
        ('Statistics', 'David Freedman'),
        ('Digital Logic Design', 'Morris Mano'),
        ('Computer Architecture', 'John Hennessy'),
        ('Compiler Design', 'Alfred Aho'),
        ('Information Security', 'Mark Stamp'),
        ('Mobile App Development', 'Neil Smyth'),
        ('Cloud Computing', 'Thomas Erl'),
        ('Big Data Analytics', 'Michael Minelli')
    ]
    
    for title, author in books_data:
        book = Book(
            title=title,
            author=author,
            copies_total=random.randint(2, 5),
            copies_available=random.randint(1, 3)
        )
        db.session.add(book)
    
    db.session.commit()
    
    print("\n" + "="*80)
    print("LIBRARY MANAGEMENT SYSTEM - LOGIN CREDENTIALS")
    print("="*80)
    
    print("\nADMINISTRATORS (5 total):")
    print("-" * 50)
    for admin in admins_created:
        print(f"PRN: {admin['prn']} | Name: {admin['name']} | Password: {admin['password']}")
    
    print(f"\nSTUDENTS (120 total) - Showing first 10:")
    print("-" * 50)
    for student in students_created[:10]:
        print(f"PRN: {student['prn']} | Name: {student['name']} | Password: {student['password']} | {student['year']} {student['course']}")
    
    print(f"\n... and {len(students_created)-10} more students (PRN2024011 to PRN2024120)")
    
    print("\nPASSWORD FORMAT:")
    print("-" * 20)
    print("Password = Mother's Name + Date of Birth (DDMMYYYY)")
    print("Example: Mother's Name 'Sunita' + DOB '15081995' = Password 'Sunita15081995'")
    
    print(f"\nSAMPLE QUICK LOGIN:")
    print("-" * 20)
    print(f"Admin: {admins_created[0]['prn']} / {admins_created[0]['password']}")
    print(f"Student: {students_created[0]['prn']} / {students_created[0]['password']}")
    
    print(f"\nDATABASE CREATED SUCCESSFULLY!")
    print(f"- {len(admins_created)} Administrators")
    print(f"- {len(students_created)} Students") 
    print(f"- {len(books_data)} Books")
    print("="*80)