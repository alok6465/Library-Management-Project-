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
    db.create_all()
    
    # Create demo data if database is empty
    if User.query.count() == 0:
        # Create sample students
        students = [
            ('PRN2024001', 'Rahul Sharma', 'Sunita', '15081995'),
            ('PRN2024002', 'Priya Patel', 'Meera', '22031998'),
            ('PRN2024003', 'Amit Kumar', 'Geeta', '10121997')
        ]
        
        for prn, name, mother_name, dob in students:
            student = User(
                prn_number=prn, username=prn.lower(), name=name,
                email=f'{prn.lower()}@college.edu', mother_name=mother_name,
                dob=dob, phone='9876543210', address='Demo Address',
                role='student', year='2nd', course='BSC IT'
            )
            student.set_password(mother_name + dob)
            db.session.add(student)
        
        # Create sample admin
        admin = User(
            prn_number='ADM2024001', username='adm2024001', name='Dr. Admin',
            email='admin@college.edu', mother_name='Usha', dob='25061975',
            phone='9999999999', address='Admin Office', role='admin'
        )
        admin.set_password('Usha25061975')
        db.session.add(admin)
        
        # Create sample books
        books = [('Python Programming', 'John Smith', 3), ('Web Development', 'Sarah Wilson', 2)]
        for title, author, copies in books:
            book = Book(title=title, author=author, copies_total=copies, copies_available=copies)
            db.session.add(book)
        
        db.session.commit()
        print('Demo data created!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)