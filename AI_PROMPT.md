# 🤖 AI PROMPT TO BUILD THIS LIBRARY MANAGEMENT SYSTEM

## MASTER PROMPT (Copy & Paste to AI)

```
Build a comprehensive Library Management System for educational institutions with the following specifications:

## CORE REQUIREMENTS

### 1. TECHNOLOGY STACK
- Backend: Flask (Python 3.11+)
- Database: SQLAlchemy ORM with SQLite (dev) / PostgreSQL (production)
- Frontend: Bootstrap 5, Bootstrap Icons, Vanilla JavaScript
- Authentication: Flask-Login with password hashing
- Security: Flask-WTF for CSRF protection
- Deployment: Render-ready with build.sh script

### 2. USER SYSTEM
**Two Roles:**
- Students (200+ users)
- Administrators (5+ users)

**Authentication:**
- Login with PRN number (e.g., PRN2024001 for students, ADM2024001 for admins)
- Password format: MotherName + DateOfBirth (e.g., Sunita15081995)
- Secure password hashing with Werkzeug

**User Model Fields:**
- PRN number, username, email, name, mother_name, dob, phone, address
- Role (student/admin), year, course
- Activity tracking: total_books_borrowed, library_hours_this_month, library_hours_this_year

### 3. BOOK MANAGEMENT
**Book Types:**
- Physical books (with copy tracking)
- Virtual books (PDF/DOCX with free access)

**Book Model Fields:**
- Title, author, category, semester, course, ISBN
- copies_total, copies_available
- is_virtual, pdf_file_path, virtual_price, download_price
- is_new_book (auto-expires after 60 days), new_book_expires
- is_prebooking, prebooking_starts, prebooking_slots, prebooking_taken
- created_at timestamp

**Sample Books:** 50+ Mumbai University BSC CS/IT textbooks across 6 semesters

### 4. LOAN SYSTEM
**Rules:**
- 14-day loan period
- Maximum 2 books per student
- ₹5 per day fine for overdue books
- 7-day extension requests (admin approval required)

**Loan Model:**
- user_id, book_id, issue_date, due_date, return_date
- Auto-calculate: is_overdue, days_overdue, fine_amount

### 5. ADVANCED FEATURES

**A. NEW Book System:**
- Mark books as NEW for 2 months
- Display 🆕 badge on book cards
- Auto-expire after 60 days

**B. Pre-booking System:**
- Admin sets limited slots (e.g., 20 slots for 20 books ordered)
- Opens 24 hours before book arrival
- Shows "📅 Pre-Book (15/20 left)" button
- PreBooking model: user_id, book_id, booked_at, status

**C. Reservation System (24-hour):**
- Reserve unavailable books for 24 hours
- Auto-expiry with notifications
- BookReservation model: user_id, book_id, reserved_at, expires_at, status

**D. Virtual Book Library:**
- Free online reading (PDF viewer)
- Free downloads
- Secure file upload (PDF/DOCX/DOC)
- Store in /static/virtual_books/

**E. Intelligent Search:**
- Fuzzy search with typo tolerance
- Levenshtein distance algorithm (60% threshold)
- Multi-strategy: exact match → word matching → fuzzy matching
- Filter by category, type (physical/virtual), semester

**F. Notice Board:**
- Broadcast to all/students/specific users
- Notice model: title, message, created_by, recipient_type, recipient_ids
- Show "NEW" badge for notices < 10 days old

**G. Extension Request System:**
- Students request 1-14 day extensions with reason
- Admin approve/reject with response
- Status expires after 24 hours (approved) or 2 days (rejected)

**H. Excel Export:**
- Auto-export Users, Books, Loans, Notices, Extension Requests, Library Sessions
- CSV format with timestamps
- Separate file viewer application (port 5001)

### 6. ADMIN DASHBOARD FEATURES
- Add/Edit/Delete books (physical & virtual)
- Enable pre-booking with slot configuration
- Mark books as NEW
- Manage users (students & admins)
- View active loans and overdue books
- Approve/reject extension requests
- Manage categories
- Manage 24-hour reservations with notifications
- Track library attendance
- Export data to Excel
- Send targeted notices

### 7. STUDENT DASHBOARD FEATURES
- Browse books with filters (category, type, semester)
- View 🆕 NEW and 📅 Pre-Book badges
- Borrow available books
- Pre-book upcoming books (limited slots)
- Reserve unavailable books (24-hour hold)
- Request loan extensions
- View borrowed books with due dates
- Access virtual books (read/download free)
- View personalized notices

### 8. UI/UX REQUIREMENTS
- Modern, professional design with Bootstrap 5
- Responsive mobile-first layout
- Color-coded badges: NEW (green), Pre-Book (yellow), Available (success), Unavailable (danger)
- Auto-hiding flash messages (2 minutes)
- Stat cards with icons
- Book cards with hover effects
- Dropdown filters for categories and book types

### 9. DATABASE MODELS
Create these SQLAlchemy models:
1. User (with relationships to loans, reservations, prebookings)
2. Book (with availability_status property, is_still_new property)
3. Loan (with is_overdue, days_overdue, fine_amount properties)
4. Notice (with recipients property, is_new property)
5. ExtensionRequest (with status_expiry logic)
6. BookReservation (with is_expired, hours_remaining properties)
7. PreBooking (user_id, book_id, booked_at, status)
8. VirtualBookPurchase (for tracking access)
9. LibrarySession (for attendance tracking)

### 10. SECURITY FEATURES
- CSRF protection on all forms
- Password hashing (Werkzeug)
- Role-based access control (@login_required decorators)
- Secure file upload (werkzeug.utils.secure_filename)
- SQL injection prevention (SQLAlchemy ORM)
- Input validation

### 11. DEPLOYMENT (RENDER)
Create build.sh script that:
- Installs requirements.txt
- Creates database tables
- Initializes with demo data (200 students, 5 admins, 50+ books)
- Sets up environment variables (PORT, FLASK_ENV, SECRET_KEY)

Create render.yaml with web service configuration.

### 12. DEMO DATA
**Students:** 200 users with realistic Indian names
- PRN: PRN2024001 to PRN2024200
- Courses: BSC IT, BSC CS, BTech CS, BTech Data Science
- Years: 1st to 5th

**Admins:** 5 users
- PRN: ADM2024001 to ADM2024005

**Books:** 50+ Mumbai University textbooks
- BSC CS: Semesters 1-6 (Programming, Database, AI/ML, etc.)
- BSC IT: Semesters 1-6 (Web Dev, IoT, Security, etc.)
- Reference books (Algorithms, Design Patterns, Clean Code)

Build this system step by step with production-ready code following Flask best practices.
```

---

## FOLLOW-UP PROMPTS

**Pre-booking System:**
```
Add pre-booking where admin sets limited slots (e.g., 20) and students can pre-book 24 hours before book arrival. Show "Pre-Book (15/20 left)".
```

**Virtual Books:**
```
Add virtual book support with PDF upload, free reading, and free downloads. Store in /static/virtual_books/.
```

**Fuzzy Search:**
```
Implement intelligent search with typo tolerance using Levenshtein distance (60% threshold).
```

**Excel Export:**
```
Create auto-export system generating CSV files with timestamps for all data.
```

**NEW Book System:**
```
Add automatic NEW badge for books that expires after 60 days. Show 🆕 badge on cards.
```

---

## TESTING CREDENTIALS

**Admin:** ADM2024001 / Usha25061975  
**Student:** PRN2024001 / Sunita15081995

---

## LIVE DEMO
- **GitHub:** https://github.com/alok6465/Library-Management-Project-
- **Live Site:** https://library-management-project-uvhi.onrender.com