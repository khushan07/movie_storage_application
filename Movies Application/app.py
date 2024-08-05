from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data structure to store movie listings
movies = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "year": 2010, "watch_urls": ["https://www.netflix.com/inception"], "image_url": "https://example.com/inception.jpg"},
    {"id": 2, "title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "year": 1999, "watch_urls": ["https://www.hbo.com/the-matrix"], "image_url": "https://example.com/matrix.jpg"}
]

def get_movie(movie_id):
    for movie in movies:
        if movie['id'] == movie_id:
            return movie
    return None

@app.route('/')
def home():
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = get_movie(movie_id)
    if movie:
        return render_template('movie_detail.html', movie=movie)
    return "Movie not found", 404

@app.route('/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = get_movie(movie_id)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        if 'delete' in request.form:
            global movies
            movies = [m for m in movies if m['id'] != movie_id]
            return redirect(url_for('home'))
        else:
            movie['title'] = request.form.get('title')
            movie['director'] = request.form.get('director')
            movie['year'] = request.form.get('year')
            movie['watch_urls'] = request.form.getlist('watch_urls')
            movie['image_url'] = request.form.get('image_url')
            return redirect(url_for('movie_detail', movie_id=movie_id))

    return render_template('edit_movie.html', movie=movie)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        new_id = max(movie['id'] for movie in movies) + 1 if movies else 1
        title = request.form.get('title')
        director = request.form.get('director')
        year = request.form.get('year')
        watch_urls = request.form.getlist('watch_urls')
        image_url = request.form.get('image_url')

        if title and director and year and watch_urls:
            movies.append({
                "id": new_id, "title": title, "director": director, "year": year, "watch_urls": watch_urls, "image_url": image_url
            })
            return redirect(url_for('home'))

        error = "Please fill out all required fields."
        return render_template('add_movie.html', error=error)

    return render_template('add_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
