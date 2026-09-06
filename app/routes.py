from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app import db
from app.models import Task


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        title = request.form["title"]

        if title.strip():

            task = Task(title=title)

            db.session.add(task)

            db.session.commit()

        return redirect(url_for("main.index"))

    tasks = Task.query.all()

    return render_template(
        "index.html",
        tasks=tasks
    )


@main.route("/complete/<int:task_id>")
def complete(task_id):

    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed

    db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/delete/<int:task_id>")
def delete(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)

    db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/health")
def health():

    return {
        "status": "healthy"
    }