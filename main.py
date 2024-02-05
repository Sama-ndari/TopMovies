import requests
from classes import *

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", movies=sort())


@app.route("/update", methods=['GET', 'POST'])
def update():
    movie_id = request.args.get('id')  # the parameter
    update_form = UpdatingForm()
    if update_form.validate_on_submit():
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = float(update_form.rating.data)
        movie_to_update.review = update_form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    my_movie = Movie.query.get(movie_id)
    return render_template('edit.html', movie=my_movie, form=update_form)


@app.route("/delete")
def delete():
    movie_id = request.args.get('id')  # the parameter
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddingForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        url = "https://api.themoviedb.org/3/search/movie?include_adult=true&language=en-US&page=1"
        TMDB_API_KEY = '025f292f6727517dc28d44a9a666e9d7'
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title,
            # "include_adult": True
        }
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMjVmMjkyZjY3Mjc1MTdkYzI4ZDQ0YTlhNjY2ZTlkNyIsInN1YiI6IjY1YjhiYWIxNWJlMDBlMDE4MjVhNGJhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HFMO6LLtAIAXOxjQi0umf0XurW3KAVNqJtOaMIj8h24"
        }
        data = requests.get(url, params=params, headers=headers).json()["results"]
        return render_template('select.html', movies=data)

    return render_template('add.html', form=add_form)


@app.route('/find')
def find():
    movie_id = request.args.get('id')
    if movie_id:
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
        new_movie = Movie(
                title=data['original_title'],
                year=data['release_date'].split('-')[0],
                description=data['overview'],
                img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}")
        db.session.add(new_movie)
        db.session.commit()
        movie1 = Movie.query.filter_by(title=data['original_title']).first()
        id_ = movie1.id
        return redirect(url_for('update', id=id_))


if __name__ == '__main__':
    app.run(debug=True)
