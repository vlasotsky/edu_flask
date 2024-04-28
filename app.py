from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost/flask_db"
)
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    published = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return "<Book %r>" % self.id


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add-book", methods=["POST", "GET"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        book = Book(title=title, author=author)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect("/books")
        except:
            return "Error while adding a page"
    else:
        return render_template("add-book.html")


@app.route("/books")
def books():
    books = Book.query.order_by(Book.published.desc()).all()
    return render_template("books.html", books=books)


@app.route("/books/<int:id>")
def book_detail(id):
    book = Book.query.get(id)
    return render_template("book_detail.html", book=book)


@app.route("/books/<int:id>/delete")
def book_delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return redirect("/books")
    except:
        return "Error occured while deleting a record"


@app.route("/books/<int:id>/update", methods=["POST", "GET"])
def update_book(id):
    book = Book.query.get(id)

    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]

        try:
            db.session.commit()
            return redirect("/books")
        except:
            return "Error while updating a page"
    else:
        return render_template("book_update.html", book=book)


@app.route("/user/<string:name>/<int:id>/")
def user(name, id):
    return "Hello, " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(debug=True)
