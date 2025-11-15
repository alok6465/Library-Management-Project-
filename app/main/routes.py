from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.main import bp
from app.models import User, Book, Loan, Notice, ExtensionRequest, LibrarySession
from sqlalchemy import func, extract

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', title='Library Management System')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    else:
        return redirect(url_for('main.student_dashboard'))

@bp.route('/student-dashboard')
@login_required
def student_dashboard():
    from app.models import Notice
    from datetime import datetime, timedelta
    
    books = Book.query.all()
    my_loans = Loan.query.filter_by(user_id=current_user.id, return_date=None).all()
    
    # Get recent notices for student
    all_notices = Notice.query.filter(
        (Notice.recipient_type == 'all') |
        (Notice.recipient_type == 'student')
    ).all()
    
    specific_notices = Notice.query.filter(
        Notice.recipient_type == 'specific'
    ).all()
    
    student_specific = []
    for notice in specific_notices:
        if notice.recipient_ids and str(current_user.id) in notice.recipient_ids.split(','):
            student_specific.append(notice)
    
    recent_notices = sorted(all_notices + student_specific, key=lambda x: x.created_date, reverse=True)[:5]
    
    return render_template('main/dashboard_student.html', title='Student Dashboard', 
                         books=books, my_loans=my_loans, recent_notices=recent_notices)

@bp.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    from app.models import Notice
    
    books = Book.query.all()
    active_loans = Loan.query.filter_by(return_date=None).all()
    overdue_loans = [loan for loan in active_loans if loan.is_overdue]
    recent_notices = Notice.query.filter_by(created_by=current_user.id).order_by(Notice.created_date.desc()).limit(5).all()
    
    return render_template('main/dashboard_admin.html', title='Admin Dashboard',
                         books=books, active_loans=active_loans, overdue_loans=overdue_loans, recent_notices=recent_notices)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(
            (Book.title.contains(query)) | (Book.author.contains(query))
        ).all()
    else:
        books = []
    
    return render_template('main/search_results.html', title='Search Results', 
                         books=books, query=query)

@bp.route('/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if book.copies_available <= 0:
        flash('Sorry, this book is currently not available.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Check 2-book limit
    current_loans = Loan.query.filter_by(user_id=current_user.id, return_date=None).count()
    if current_loans >= 2:
        flash('You can only borrow maximum 2 books at a time. Please return a book first.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Check if user already has this book
    existing_loan = Loan.query.filter_by(
        user_id=current_user.id, book_id=book_id, return_date=None
    ).first()
    
    if existing_loan:
        flash('You have already borrowed this book.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Create new loan
    loan = Loan(user_id=current_user.id, book_id=book_id)
    book.copies_available -= 1
    
    # Update user activity
    current_user.total_books_borrowed += 1
    
    db.session.add(loan)
    db.session.commit()
    
    flash(f'Successfully borrowed "{book.title}". Due date: {loan.due_date.strftime("%Y-%m-%d")}', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/return/<int:loan_id>')
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    if loan.user_id != current_user.id and current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if loan.return_date:
        flash('This book has already been returned.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Process return
    loan.return_date = datetime.utcnow()
    loan.book.copies_available += 1
    
    # Calculate fine if overdue
    fine = loan.fine_amount
    if fine > 0:
        flash(f'Book returned successfully. Fine: ${fine:.2f} for late return.', 'warning')
    else:
        flash('Book returned successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@bp.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        copies = int(request.form.get('copies', 1))
        
        if title and author:
            book = Book(title=title, author=author, 
                       copies_total=copies, copies_available=copies)
            db.session.add(book)
            db.session.commit()
            flash(f'Book "{title}" added successfully!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Please fill in all required fields.', 'danger')
    
    return render_template('main/add_book.html', title='Add Book')

@bp.route('/delete-book/<int:book_id>')
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    book = Book.query.get_or_404(book_id)
    
    # Check for active loans
    active_loans = Loan.query.filter_by(book_id=book_id, return_date=None).count()
    if active_loans > 0:
        flash(f'Cannot delete book "{book.title}". It has {active_loans} active loan(s).', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    
    # Check for any loan history
    total_loans = Loan.query.filter_by(book_id=book_id).count()
    if total_loans > 0:
        flash(f'Cannot delete book "{book.title}". It has loan history. Consider marking it as unavailable instead.', 'warning')
        return redirect(url_for('main.admin_dashboard'))
    
    # Safe to delete - no loan records
    try:
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting book. Please try again.', 'danger')
    
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/manage-users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    search_query = request.args.get('search', '')
    if search_query:
        users = User.query.filter(
            (User.name.contains(search_query)) | 
            (User.prn_number.contains(search_query)) |
            (User.email.contains(search_query))
        ).all()
    else:
        users = User.query.all()
    
    return render_template('main/manage_users.html', title='Manage Users', 
                         users=users, search_query=search_query)

@bp.route('/extend-loan/<int:loan_id>')
@login_required
def extend_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    if current_user.role != 'admin' and loan.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if loan.return_date:
        flash('Cannot extend returned book.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Extend by 7 days
    from datetime import timedelta
    loan.due_date = loan.due_date + timedelta(days=7)
    db.session.commit()
    
    flash(f'Loan extended until {loan.due_date.strftime("%Y-%m-%d")}', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/toggle-book-availability/<int:book_id>')
@login_required
def toggle_book_availability(book_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    book = Book.query.get_or_404(book_id)
    
    if book.copies_available > 0:
        # Mark as unavailable
        book.copies_available = 0
        flash(f'Book "{book.title}" marked as unavailable.', 'warning')
    else:
        # Mark as available
        book.copies_available = book.copies_total
        flash(f'Book "{book.title}" marked as available.', 'success')
    
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/request-extension/<int:loan_id>', methods=['GET', 'POST'])
@login_required
def request_extension(loan_id):
    from app.models import ExtensionRequest
    
    loan = Loan.query.get_or_404(loan_id)
    
    if loan.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if loan.return_date:
        flash('Cannot extend returned book.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Check if there's already a pending request
    pending_request = ExtensionRequest.query.filter_by(
        loan_id=loan_id, status='pending'
    ).first()
    
    if pending_request:
        flash('You already have a pending extension request for this book.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        reason = request.form.get('reason')
        requested_days = int(request.form.get('requested_days', 0))
        
        if reason and requested_days > 0 and requested_days <= 14:
            extension_request = ExtensionRequest(
                loan_id=loan_id,
                requested_days=requested_days,
                reason=reason
            )
            
            # Update user activity
            current_user.total_extension_requests += 1
            
            db.session.add(extension_request)
            db.session.commit()
            
            flash('Extension request submitted successfully! Admin will review it.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Please provide a valid reason and days (1-14 days).', 'danger')
    
    return render_template('main/request_extension.html', title='Request Extension', loan=loan)

@bp.route('/manage-extensions')
@login_required
def manage_extensions():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    from app.models import ExtensionRequest
    
    pending_requests = ExtensionRequest.query.filter_by(status='pending').all()
    all_requests = ExtensionRequest.query.order_by(ExtensionRequest.request_date.desc()).all()
    
    return render_template('main/manage_extensions.html', title='Manage Extensions',
                         pending_requests=pending_requests, all_requests=all_requests)

@bp.route('/respond-extension/<int:request_id>', methods=['POST'])
@login_required
def respond_extension(request_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    from app.models import ExtensionRequest
    from datetime import timedelta
    
    extension_request = ExtensionRequest.query.get_or_404(request_id)
    action = request.form.get('action')
    admin_response = request.form.get('admin_response', '')
    
    if action == 'approve':
        # Extend the loan
        loan = extension_request.loan
        loan.due_date = loan.due_date + timedelta(days=extension_request.requested_days)
        
        extension_request.status = 'approved'
        extension_request.admin_response = admin_response or 'Extension approved'
        extension_request.response_date = datetime.utcnow()
        extension_request.responded_by = current_user.id
        extension_request.set_status_expiry()
        
        flash(f'Extension approved for {extension_request.requested_days} days.', 'success')
        
    elif action == 'reject':
        if not admin_response:
            flash('Please provide a reason for rejection.', 'danger')
            return redirect(url_for('main.manage_extensions'))
        
        extension_request.status = 'rejected'
        extension_request.admin_response = admin_response
        extension_request.response_date = datetime.utcnow()
        extension_request.responded_by = current_user.id
        extension_request.set_status_expiry()
        
        flash('Extension request rejected.', 'info')
    
    db.session.commit()
    return redirect(url_for('main.manage_extensions'))

@bp.route('/book-details/<int:book_id>')
@login_required
def book_details(book_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    book = Book.query.get_or_404(book_id)
    active_loans = Loan.query.filter_by(book_id=book_id, return_date=None).all()
    loan_history = Loan.query.filter_by(book_id=book_id).order_by(Loan.issue_date.desc()).all()
    
    return render_template('main/book_details.html', title=f'Book Details - {book.title}',
                         book=book, active_loans=active_loans, loan_history=loan_history)

@bp.route('/send-notice', methods=['GET', 'POST'])
@login_required
def send_notice():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        from app.models import Notice
        
        title = request.form.get('title')
        message = request.form.get('message')
        recipient_type = request.form.get('recipient_type')
        recipient_ids = request.form.getlist('recipient_ids')
        
        if title and message:
            recipient_ids_str = ','.join(recipient_ids) if recipient_ids else None
            
            notice = Notice(
                title=title,
                message=message,
                created_by=current_user.id,
                recipient_type=recipient_type,
                recipient_ids=recipient_ids_str
            )
            db.session.add(notice)
            db.session.commit()
            
            if recipient_type == 'specific' and recipient_ids:
                flash(f'Notice sent to {len(recipient_ids)} student(s) successfully!', 'success')
            else:
                flash('Notice sent successfully!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Please fill in all required fields.', 'danger')
    
    students = User.query.filter_by(role='student').all()
    return render_template('main/send_notice.html', title='Send Notice', students=students)

@bp.route('/notices')
@login_required
def view_notices():
    from app.models import Notice
    
    if current_user.role == 'student':
        # Student sees notices for all students and specific notices for them
        all_notices = Notice.query.filter(
            (Notice.recipient_type == 'all') |
            (Notice.recipient_type == 'student')
        ).all()
        
        specific_notices = Notice.query.filter(
            Notice.recipient_type == 'specific'
        ).all()
        
        # Filter specific notices that include this student
        student_specific = []
        for notice in specific_notices:
            if notice.recipient_ids and str(current_user.id) in notice.recipient_ids.split(','):
                student_specific.append(notice)
        
        notices = sorted(all_notices + student_specific, key=lambda x: x.created_date, reverse=True)
    else:
        # Admin sees all notices they created
        notices = Notice.query.filter_by(created_by=current_user.id).order_by(Notice.created_date.desc()).all()
    
    return render_template('main/notices.html', title='Notices', notices=notices)

@bp.route('/send-user-notice/<int:user_id>', methods=['POST'])
@login_required
def send_user_notice(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    from app.models import Notice
    
    user = User.query.get_or_404(user_id)
    title = request.form.get('title')
    message = request.form.get('message')
    
    if title and message:
        notice = Notice(
            title=title,
            message=message,
            created_by=current_user.id,
            recipient_type='specific',
            recipient_ids=str(user_id)
        )
        db.session.add(notice)
        db.session.commit()
        flash(f'Notice sent to {user.name} successfully!', 'success')
    else:
        flash('Please fill in all required fields.', 'danger')
    
    return redirect(request.referrer or url_for('main.admin_dashboard'))

@bp.route('/delete-notice/<int:notice_id>')
@login_required
def delete_notice(notice_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    from app.models import Notice
    
    notice = Notice.query.get_or_404(notice_id)
    
    # Only allow admin to delete their own notices
    if notice.created_by != current_user.id:
        flash('You can only delete notices you created.', 'danger')
        return redirect(url_for('main.view_notices'))
    
    try:
        db.session.delete(notice)
        db.session.commit()
        flash('Notice deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting notice. Please try again.', 'danger')
    
    return redirect(url_for('main.view_notices'))

@bp.route('/manage-students')
@login_required
def manage_students():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    students = User.query.filter_by(role='student').all()
    return render_template('main/manage_students.html', title='Manage Students', students=students)

@bp.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        prn_number = request.form.get('prn_number')
        name = request.form.get('name')
        email = request.form.get('email')
        mother_name = request.form.get('mother_name')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        address = request.form.get('address')
        year = request.form.get('year')
        course = request.form.get('course')
        
        if User.query.filter_by(prn_number=prn_number).first():
            flash('PRN number already exists.', 'danger')
            return render_template('main/add_student.html', title='Add Student')
        
        student = User(
            prn_number=prn_number,
            username=prn_number.lower(),
            name=name,
            email=email,
            mother_name=mother_name,
            dob=dob,
            phone=phone,
            address=address,
            year=year,
            course=course,
            role='student'
        )
        
        password = mother_name + dob
        student.set_password(password)
        
        db.session.add(student)
        db.session.commit()
        
        flash(f'Student {name} added! Password: {password}', 'success')
        return redirect(url_for('main.manage_students'))
    
    return render_template('main/add_student.html', title='Add Student')

@bp.route('/edit-student/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_student(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    student = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.mother_name = request.form.get('mother_name')
        student.dob = request.form.get('dob')
        student.phone = request.form.get('phone')
        student.address = request.form.get('address')
        student.year = request.form.get('year')
        student.course = request.form.get('course')
        
        password = student.mother_name + student.dob
        student.set_password(password)
        
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('main.manage_students'))
    
    return render_template('main/edit_student.html', title='Edit Student', student=student)

@bp.route('/delete-student/<int:user_id>')
@login_required
def delete_student(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    student = User.query.get_or_404(user_id)
    
    active_loans = Loan.query.filter_by(user_id=user_id, return_date=None).count()
    if active_loans > 0:
        flash('Cannot delete student with active loans.', 'danger')
        return redirect(url_for('main.manage_students'))
    
    db.session.delete(student)
    db.session.commit()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('main.manage_students'))



@bp.route('/user-activity')
@login_required
def user_activity():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    monthly_loans = db.session.query(
        User.id, User.name, func.count(Loan.id).label('loans_count')
    ).join(Loan).filter(
        extract('month', Loan.issue_date) == current_month,
        extract('year', Loan.issue_date) == current_year
    ).group_by(User.id).all()
    
    library_hours = User.query.filter(
        User.role == 'student',
        User.library_hours_this_month > 0
    ).order_by(User.library_hours_this_month.desc()).all()
    
    return render_template('main/user_activity.html', title='User Activity',
                         monthly_loans=monthly_loans, library_hours=library_hours)

@bp.route('/library-attendance')
@login_required
def library_attendance():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    students = User.query.filter_by(role='student').all()
    return render_template('main/library_attendance.html', title='Library Attendance', students=students)

@bp.route('/manage-admins')
@login_required
def manage_admins():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    admins = User.query.filter_by(role='admin').all()
    return render_template('main/manage_admins.html', title='Manage Admins', admins=admins)

@bp.route('/add-admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        prn_number = request.form.get('prn_number')
        name = request.form.get('name')
        email = request.form.get('email')
        mother_name = request.form.get('mother_name')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if User.query.filter_by(prn_number=prn_number).first():
            flash('PRN number already exists.', 'danger')
            return render_template('main/add_admin.html', title='Add Admin')
        
        admin = User(
            prn_number=prn_number,
            username=prn_number.lower(),
            name=name,
            email=email,
            mother_name=mother_name,
            dob=dob,
            phone=phone,
            address=address,
            role='admin'
        )
        
        password = mother_name + dob
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        flash(f'Admin {name} added! Password: {password}', 'success')
        return redirect(url_for('main.manage_admins'))
    
    return render_template('main/add_admin.html', title='Add Admin')

@bp.route('/delete-admin/<int:user_id>')
@login_required
def delete_admin(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    admin = User.query.get_or_404(user_id)
    
    if admin.id == current_user.id:
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('main.manage_admins'))
    
    if admin.role != 'admin':
        flash('Invalid user type.', 'danger')
        return redirect(url_for('main.manage_admins'))
    
    db.session.delete(admin)
    db.session.commit()
    
    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('main.manage_admins'))

@bp.route('/add-library-session', methods=['POST'])
@login_required
def add_library_session():
    if current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    student_id = request.form.get('student_id')
    hours = float(request.form.get('hours', 0))
    date = request.form.get('date')
    
    student = User.query.get_or_404(student_id)
    
    # Create library session
    session = LibrarySession(
        user_id=student_id,
        check_in=datetime.strptime(date + ' 09:00:00', '%Y-%m-%d %H:%M:%S'),
        check_out=datetime.strptime(date + ' 09:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(hours=hours),
        duration_hours=hours
    )
    
    # Update student's library hours
    student.library_hours_this_month += hours
    student.library_hours_this_year += hours
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Added {hours} hours for {student.name}'})