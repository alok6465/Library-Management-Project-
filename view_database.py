from app import create_app
from app.models import User, Book, Loan, Notice, ExtensionRequest, LibrarySession

app = create_app()

with app.app_context():
    print("=== DATABASE CONTENTS ===\n")
    
    # Users
    users = User.query.all()
    print(f"USERS ({len(users)} total):")
    for user in users:
        print(f"  ID: {user.id} | PRN: {user.prn_number} | Name: {user.name} | Role: {user.role}")
    
    # Books
    books = Book.query.all()
    print(f"\nBOOKS ({len(books)} total):")
    for book in books:
        print(f"  ID: {book.id} | Title: {book.title} | Author: {book.author} | Available: {book.copies_available}/{book.copies_total}")
    
    # Loans
    loans = Loan.query.all()
    print(f"\nLOANS ({len(loans)} total):")
    for loan in loans:
        user = User.query.get(loan.user_id)
        book = Book.query.get(loan.book_id)
        status = "Returned" if loan.return_date else "Active"
        print(f"  ID: {loan.id} | User: {user.name} | Book: {book.title} | Status: {status}")
    
    # Notices
    notices = Notice.query.all()
    print(f"\nNOTICES ({len(notices)} total):")
    for notice in notices:
        creator = User.query.get(notice.created_by)
        print(f"  ID: {notice.id} | Title: {notice.title} | Type: {notice.recipient_type} | By: {creator.name}")
    
    # Extension Requests
    extensions = ExtensionRequest.query.all()
    print(f"\nEXTENSION REQUESTS ({len(extensions)} total):")
    for ext in extensions:
        loan = Loan.query.get(ext.loan_id)
        user = User.query.get(loan.user_id)
        print(f"  ID: {ext.id} | User: {user.name} | Status: {ext.status}")
    
    # Library Sessions
    sessions = LibrarySession.query.all()
    print(f"\nLIBRARY SESSIONS ({len(sessions)} total):")
    for session in sessions:
        user = User.query.get(session.user_id)
        print(f"  ID: {session.id} | User: {user.name} | Hours: {session.duration_hours}")