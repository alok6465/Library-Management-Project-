"""Update books with better categories

Run this to update existing books with proper categories
"""

from app import create_app, db
from app.models import Book

app = create_app()

with app.app_context():
    # Update existing books with categories
    books = Book.query.all()
    
    category_mapping = {
        'Python': 'Programming',
        'Java': 'Programming',
        'JavaScript': 'Web Development',
        'Data': 'Data Science',
        'Database': 'Database Systems',
        'Web': 'Web Development',
        'Network': 'Computer Networks',
        'Algorithm': 'Algorithms',
        'Structure': 'Data Structures',
        'Machine': 'Machine Learning',
        'AI': 'Artificial Intelligence',
        'HTML': 'Web Development',
        'CSS': 'Web Development',
        'React': 'Web Development',
        'Node': 'Web Development',
        'Django': 'Web Development',
        'Flask': 'Web Development',
    }
    
    for book in books:
        if not book.category or book.category == 'General':
            # Try to assign category based on title
            for keyword, category in category_mapping.items():
                if keyword.lower() in book.title.lower():
                    book.category = category
                    break
            
            # If still no category, assign based on common patterns
            if not book.category or book.category == 'General':
                if any(word in book.title.lower() for word in ['programming', 'code', 'software']):
                    book.category = 'Programming'
                elif any(word in book.title.lower() for word in ['web', 'html', 'css', 'javascript']):
                    book.category = 'Web Development'
                elif any(word in book.title.lower() for word in ['data', 'analytics', 'science']):
                    book.category = 'Data Science'
                elif any(word in book.title.lower() for word in ['math', 'calculus', 'algebra']):
                    book.category = 'Mathematics'
                else:
                    book.category = 'General'
    
    db.session.commit()
    print(f"Updated {len(books)} books with categories!")
    
    # Print category distribution
    from sqlalchemy import func
    categories = db.session.query(Book.category, func.count(Book.id)).group_by(Book.category).all()
    print("\nCategory Distribution:")
    for category, count in categories:
        print(f"  {category}: {count} books")
