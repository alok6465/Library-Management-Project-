from app import create_app
from app.extensions import db
from app.models import User, Book, Notice, ExtensionRequest
import random

app = create_app()

def setup_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Sample data
        mother_names = [
            'Sunita', 'Priya', 'Kavita', 'Meera', 'Sita', 'Geeta', 'Radha', 'Shanti', 'Lata', 'Maya',
            'Usha', 'Rekha', 'Nisha', 'Pooja', 'Asha', 'Kiran', 'Mala', 'Sushma', 'Vandana', 'Seema'
        ]

        student_names = [
            'Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Singh', 'Vikash Gupta', 'Anita Yadav',
            'Rohit Verma', 'Kavya Joshi', 'Suresh Reddy', 'Pooja Agarwal', 'Manoj Tiwari', 'Ritu Sharma',
            'Deepak Mishra', 'Swati Pandey', 'Ajay Thakur', 'Neha Kapoor', 'Sanjay Kumar', 'Preeti Singh',
            'Rajesh Rao', 'Divya Nair', 'Arun Jain', 'Shweta Dubey', 'Vinod Sinha', 'Meera Gupta',
            'Kiran Yadav', 'Sachin Patil', 'Nidhi Sharma', 'Ramesh Kumar', 'Sunita Devi', 'Prakash Singh'
        ]

        admin_names = [
            'Dr. Rajesh Kumar', 'Prof. Sunita Sharma', 'Mr. Anil Gupta', 'Ms. Priya Verma', 'Dr. Suresh Patel'
        ]
        
        # Clear existing data
        User.query.delete()
        Book.query.delete()
        
        print("Creating 120 students...")
        # Create 120 students
        for i in range(120):
            prn = f"PRN2024{str(i+1).zfill(3)}"
            name = random.choice(student_names) + f" {i+1}"
            mother_name = random.choice(mother_names)
            dob = f"{random.randint(1,28):02d}{random.randint(1,12):02d}{random.randint(1995,2005)}"
            password = f"{mother_name}{dob}"
            
            user = User(
                prn_number=prn,
                username=f"student{i+1}",
                name=name,
                email=f"student{i+1}@college.edu",
                mother_name=mother_name,
                dob=dob,
                phone=f"98765{str(i+10000)[-5:]}",
                address=f"Address {i+1}, City, State",
                role='student'
            )
            user.set_password(password)
            db.session.add(user)
        
        print("Creating 5 admins...")
        # Create 5 admins
        for i in range(5):
            prn = f"ADM2024{str(i+1).zfill(3)}"
            name = admin_names[i]
            mother_name = random.choice(mother_names)
            dob = f"{random.randint(1,28):02d}{random.randint(1,12):02d}{random.randint(1970,1985)}"
            password = f"{mother_name}{dob}"
            
            user = User(
                prn_number=prn,
                username=f"admin{i+1}",
                name=name,
                email=f"admin{i+1}@college.edu",
                mother_name=mother_name,
                dob=dob,
                phone=f"99999{str(i+10000)[-5:]}",
                address=f"Admin Address {i+1}, City, State",
                role='admin'
            )
            user.set_password(password)
            db.session.add(user)
        
        print("Creating sample books...")
        # Create sample books
        books_data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 5),
            ('To Kill a Mockingbird', 'Harper Lee', 4),
            ('1984', 'George Orwell', 6),
            ('Pride and Prejudice', 'Jane Austen', 3),
            ('The Catcher in the Rye', 'J.D. Salinger', 4),
            ('Lord of the Flies', 'William Golding', 3),
            ('Animal Farm', 'George Orwell', 5),
            ('Brave New World', 'Aldous Huxley', 4),
            ('The Lord of the Rings', 'J.R.R. Tolkien', 2),
            ('Harry Potter Series', 'J.K. Rowling', 7),
            ('The Alchemist', 'Paulo Coelho', 4),
            ('One Hundred Years of Solitude', 'Gabriel García Márquez', 3),
            ('The Kite Runner', 'Khaled Hosseini', 4),
            ('Life of Pi', 'Yann Martel', 3),
            ('The Da Vinci Code', 'Dan Brown', 5),
            ('Programming in C', 'Dennis Ritchie', 8),
            ('Data Structures and Algorithms', 'Thomas Cormen', 6),
            ('Computer Networks', 'Andrew Tanenbaum', 5),
            ('Operating Systems', 'Abraham Silberschatz', 7),
            ('Database Management Systems', 'Raghu Ramakrishnan', 6)
        ]
        
        for title, author, copies in books_data:
            book = Book(
                title=title,
                author=author,
                copies_total=copies,
                copies_available=copies
            )
            db.session.add(book)
        
        db.session.commit()
        
        print("\n[SUCCESS] Database setup complete!")
        print("\n=== SAMPLE LOGIN CREDENTIALS ===")
        print("STUDENTS (first 5):")
        for i in range(5):
            user = User.query.filter_by(role='student').offset(i).first()
            print(f"PRN: {user.prn_number} | Password: {user.mother_name}{user.dob}")
        
        print("\nADMINS:")
        for i in range(5):
            user = User.query.filter_by(role='admin').offset(i).first()
            print(f"PRN: {user.prn_number} | Password: {user.mother_name}{user.dob}")
        
        print(f"\n[INFO] Created: 120 students, 5 admins, {len(books_data)} books")
        print("[NEXT] Now run: python run.py")

if __name__ == '__main__':
    setup_database()