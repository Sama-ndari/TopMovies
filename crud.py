import pprint
import requests


def search_movie():
    url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"

    TMDB_API_KEY = '025f292f6727517dc28d44a9a666e9d7'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMjVmMjkyZjY3Mjc1MTdkYzI4ZDQ0YTlhNjY2ZTlkNyIsInN1YiI6IjY1YjhiYWIxNWJlMDBlMDE4MjVhNGJhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HFMO6LLtAIAXOxjQi0umf0XurW3KAVNqJtOaMIj8h24"
    }
    params = {
        "api_key": TMDB_API_KEY,
        "query": 'avengers',
        "include_adult": True
    } 
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    movies = data["results"]
    for movie in movies:
        pprint.pprint(movie)
        # pprint.pprint(movie['overview'])
        # pprint.pprint(movie['release_date'].split('-')[0])
        # pprint.pprint(movie['poster_path'])


def adding_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    TMDB_API_KEY = '025f292f6727517dc28d44a9a666e9d7'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMjVmMjkyZjY3Mjc1MTdkYzI4ZDQ0YTlhNjY2ZTlkNyIsInN1YiI6IjY1YjhiYWIxNWJlMDBlMDE4MjVhNGJhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HFMO6LLtAIAXOxjQi0umf0XurW3KAVNqJtOaMIj8h24"
    }

    params = {
        "api_key": TMDB_API_KEY
    }

    data = requests.get(url, headers=headers, params=params).json()
    title = data['original_title']

    img_url = data['poster_path']

    year = data['release_date'].split('-')[0]

    description = data['overview']

    print(title)
    print(img_url)
    print(year)
    print(description)


# search_movie()

adding_movie(int(299536))


def aa():
    import sqlite3
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import create_engine, Column, Integer, String, Float
    from sqlalchemy.orm import sessionmaker, DeclarativeBase

    def using_cursor():
        db = sqlite3.connect("books-collection.db")
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
        cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
        db.commit()

    class Base(DeclarativeBase):
        pass

    # Create a new Database
    db = SQLAlchemy(model_class=Base)
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books-collection.db'
    db.init_app(app)

    # Create new table

    class Book(db.Model):
        __tablename__ = 'books'

        id = Column(Integer, primary_key=True)
        title = Column(String)
        author = Column(String)
        rating = Column(Float)

        # Optional: this will allow each book object to be identified by its title when printed.
        def __repr__(self):
            return f'<Book {self.title}>'

    with app.app_context():
        db.create_all()

    # Create new record
    new_book = Book(title='The Great Gatsby', author='F. Scott Fitzgerald', rating=6)
    db.session.add(new_book)
    db.session.commit()

    # read all the books
    books = db.session.query(Book).all()
    for book in books:
        print(book.title, book.author)

    # Read A Particular Record By Query
    book = Book.query.filter_by(title="Harry Potter").first()

    # Update A Particular Record By Query
    book_to_update = Book.query.filter_by(title="Harry Potter").first()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

    # Update A Record By PRIMARY KEY
    book_id = 1
    book_to_update = Book.query.get(book_id)
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()

    # Delete A Particular Record By PRIMARY KEY
    book_id = 1
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    db.session.close()  # close the database when you're done
