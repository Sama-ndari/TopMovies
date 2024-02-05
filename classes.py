from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import Column, Integer, String, Float, Enum
import enum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, FloatField
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    Bootstrap(app)
    return app


app = create_app()


# Create a new Database
def database(name):
    db = SQLAlchemy()
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{name}.db'
    db.init_app(app)
    return db


db = database('top10_movies')


def sort():
    all_movies = Movie.query.order_by(Movie.rating).all()
    # This line loops through all the movies
    for i in range(len(all_movies)):
        all_movies[i].ranking = int(len(all_movies) - i)
        db.session.commit()
    movie = Movie.query.order_by(Movie.ranking).all()
    return movie


class StatusEnum(enum.Enum):
    ACTION = 'action'
    NO_ACTION = 'no_action'
    UNKNOWN = 'unknown'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)
    rating = Column(Float, nullable=True)
    ranking = Column(Integer, nullable=True)
    review = Column(String(250), nullable=True)
    status = Column(Enum(StatusEnum), nullable=True)
    img_url = Column(String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


class UpdatingForm(FlaskForm):
    rating = FloatField(label='Your rating Out of 10 e.g. 7.5',
                        validators=[
                            validators.DataRequired(message="Type Something"),
                            validators.NumberRange(min=0.0, max=10.0)
                        ],
                        default=5.0
                        )
    review = StringField('Your Review',
                         validators=[
                             validators.DataRequired(message="Type something")
                         ])
    submit = SubmitField('Done')


class AddingForm(FlaskForm):
    title = StringField(label='Movie Title',
                        validators=[
                            validators.DataRequired(message="Type the name of the movie")
                        ])
    submit = SubmitField("Add Movie")





