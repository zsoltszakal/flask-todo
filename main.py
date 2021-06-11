from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

# db.create_all()


@app.route("/")
def home():
    all_todos = Todo.query.all()
    return render_template("index.html", all_todos=all_todos)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        new_todo = Todo(
            title=title
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html")


@app.route("/delete")
def delete():
    todo_id = request.args.get("task_id")
    todo_to_delete = Todo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update")
def update():
    todo_id = request.args.get("task_id")
    todo_to_update = Todo.query.get(todo_id)
    todo_to_update.completed = not todo_to_update.completed
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
