import os
import glob
import csv
from datetime import datetime
from app.models import User, Book, Loan, Notice, ExtensionRequest, LibrarySession
from app.extensions import db

def create_excel_exports():
    """Export all database tables to Excel files"""
    try:
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(os.getcwd(), 'excel_exports')
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
        
        # Delete old CSV files
        old_files = glob.glob(os.path.join(exports_dir, '*.csv'))
        deleted_count = 0
        for old_file in old_files:
            try:
                os.remove(old_file)
                deleted_count += 1
            except Exception as e:
                print(f"Could not delete {old_file}: {e}")
        
        if deleted_count > 0:
            print(f"Deleted {deleted_count} old export files")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export Users
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                'ID': user.id,
                'PRN Number': user.prn_number,
                'Name': user.name,
                'Email': user.email,
                'Role': user.role,
                'Course': user.course or 'N/A',
                'Year': user.year or 'N/A',
                'Phone': user.phone,
                'Address': user.address,
                'Mother Name': user.mother_name,
                'DOB': user.dob,
                'Books Borrowed': user.total_books_borrowed,
                'Extension Requests': user.total_extension_requests,
                'Library Hours (Month)': user.library_hours_this_month,
                'Library Hours (Year)': user.library_hours_this_year,
                'Created At': user.created_at,
                'Updated At': user.updated_at
            })
        
        users_csv = os.path.join(exports_dir, f'Users_{timestamp}.csv')
        with open(users_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if users_data:
                fieldnames = users_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users_data)
        
        # Export Books
        books = Book.query.all()
        books_data = []
        for book in books:
            books_data.append({
                'ID': book.id,
                'Title': book.title,
                'Author': book.author,
                'Category': book.category,
                'Course': book.course,
                'Semester': book.semester,
                'ISBN': book.isbn,
                'Total Copies': book.copies_total,
                'Available Copies': book.copies_available,
                'Borrowed Copies': book.copies_total - book.copies_available
            })
        
        books_csv = os.path.join(exports_dir, f'Books_{timestamp}.csv')
        with open(books_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if books_data:
                fieldnames = books_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(books_data)
        
        # Export Loans
        loans = Loan.query.all()
        loans_data = []
        for loan in loans:
            user = User.query.get(loan.user_id)
            book = Book.query.get(loan.book_id)
            loans_data.append({
                'ID': loan.id,
                'Student PRN': user.prn_number if user else 'Unknown',
                'Student Name': user.name if user else 'Unknown',
                'Book Title': book.title if book else 'Unknown',
                'Book Author': book.author if book else 'Unknown',
                'Issue Date': loan.issue_date,
                'Due Date': loan.due_date,
                'Return Date': loan.return_date or 'Not Returned',
                'Status': 'Returned' if loan.return_date else 'Active',
                'Is Overdue': 'Yes' if loan.is_overdue else 'No',
                'Days Overdue': loan.days_overdue,
                'Fine Amount': loan.fine_amount
            })
        
        loans_csv = os.path.join(exports_dir, f'Loans_{timestamp}.csv')
        with open(loans_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if loans_data:
                fieldnames = loans_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(loans_data)
        
        # Export Notices
        notices = Notice.query.all()
        notices_data = []
        for notice in notices:
            creator = User.query.get(notice.created_by)
            notices_data.append({
                'ID': notice.id,
                'Title': notice.title,
                'Message': notice.message,
                'Created By': creator.name if creator else 'Unknown',
                'Created Date': notice.created_date,
                'Recipient Type': notice.recipient_type,
                'Recipient IDs': notice.recipient_ids or 'All',
                'Is Read': 'Yes' if notice.is_read else 'No',
                'Days Old': notice.days_old
            })
        
        notices_csv = os.path.join(exports_dir, f'Notices_{timestamp}.csv')
        with open(notices_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if notices_data:
                fieldnames = notices_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(notices_data)
        
        # Export Extension Requests
        extensions = ExtensionRequest.query.all()
        extensions_data = []
        for ext in extensions:
            loan = Loan.query.get(ext.loan_id)
            user = User.query.get(loan.user_id) if loan else None
            book = Book.query.get(loan.book_id) if loan else None
            admin = User.query.get(ext.responded_by) if ext.responded_by else None
            
            extensions_data.append({
                'ID': ext.id,
                'Student PRN': user.prn_number if user else 'Unknown',
                'Student Name': user.name if user else 'Unknown',
                'Book Title': book.title if book else 'Unknown',
                'Requested Days': ext.requested_days,
                'Reason': ext.reason,
                'Status': ext.status,
                'Admin Response': ext.admin_response or 'No Response',
                'Request Date': ext.request_date,
                'Response Date': ext.response_date or 'No Response',
                'Responded By': admin.name if admin else 'No Admin'
            })
        
        extensions_csv = os.path.join(exports_dir, f'Extension_Requests_{timestamp}.csv')
        with open(extensions_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if extensions_data:
                fieldnames = extensions_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(extensions_data)
        
        # Export Library Sessions
        sessions = LibrarySession.query.all()
        sessions_data = []
        for session in sessions:
            user = User.query.get(session.user_id)
            sessions_data.append({
                'ID': session.id,
                'Student PRN': user.prn_number if user else 'Unknown',
                'Student Name': user.name if user else 'Unknown',
                'Check In': session.check_in,
                'Check Out': session.check_out or 'Still In Library',
                'Duration Hours': session.duration_hours or 0
            })
        
        sessions_csv = os.path.join(exports_dir, f'Library_Sessions_{timestamp}.csv')
        with open(sessions_csv, 'w', newline='', encoding='utf-8') as csvfile:
            if sessions_data:
                fieldnames = sessions_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sessions_data)
        
        # Create a summary report
        summary_data = {
            'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Total Students': [User.query.filter_by(role='student').count()],
            'Total Admins': [User.query.filter_by(role='admin').count()],
            'Total Books': [Book.query.count()],
            'Total Loans': [Loan.query.count()],
            'Active Loans': [Loan.query.filter_by(return_date=None).count()],
            'Overdue Loans': [len([loan for loan in Loan.query.filter_by(return_date=None).all() if loan.is_overdue])],
            'Total Notices': [Notice.query.count()],
            'Total Extension Requests': [ExtensionRequest.query.count()],
            'Total Library Sessions': [LibrarySession.query.count()]
        }
        
        summary_csv = os.path.join(exports_dir, f'Summary_Report_{timestamp}.csv')
        with open(summary_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = summary_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Convert to row format
            row_data = {}
            for key, value in summary_data.items():
                row_data[key] = value[0]
            writer.writerow(row_data)
        
        return {
            'success': True,
            'files': [
                users_csv, books_csv, loans_csv, notices_csv, 
                extensions_csv, sessions_csv, summary_csv
            ],
            'timestamp': timestamp
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def auto_export_on_change():
    """Automatically export data when changes occur"""
    try:
        result = create_excel_exports()
        if result['success']:
            print(f"Auto-export completed at {result['timestamp']}")
            return True
        else:
            print(f"Auto-export failed: {result['error']}")
            return False
    except Exception as e:
        print(f"Auto-export error: {str(e)}")
        return False