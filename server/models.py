from flask_sqlalchemy import SQLAlchemy,
from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(length=10))
    __table_args__ = (
        UniqueConstraint('name', name='unique_author_name'),
        CheckConstraint('LENGTH(phone_number) = 10', name='valid_phone_number_length')
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name cannot be empty.")
        return name
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    




class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String(length=250), nullable=False)
    summary = Column(String(length=250))
    category = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        CheckConstraint('LENGTH(content) >= 250', name='valid_content_length'),
        CheckConstraint('LENGTH(summary) <= 250', name='valid_summary_length'),
        CheckConstraint('category IN (\'Fiction\', \'Non-Fiction\')', name='valid_category')
    )

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post title cannot be empty.")
        if not any(keyword in title for keyword in ["Won't Believe", 'Secret', 'Top', 'Guess']):
            raise ValueError("Title must be sufficiently clickbait-y. It should contain 'Won\'t Believe', 'Secret', 'Top [number]', or 'Guess'.")
        return title

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Invalid category. Category must be 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters.")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary}, category={self.category})'
