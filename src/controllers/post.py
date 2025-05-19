from http import HTTPStatus
from flask import Blueprint, request
from src.app import Post, db
from sqlalchemy import inspect


app = Blueprint("Post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=data["author_id"]
    )
    db.session.add(post)
    db.session.commit()

def _list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    return [
        {   
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author_id": post.author_id,
        }
        for post in posts
    ]

@app.route("/", methods=["GET", "POST"])
def create_and_list():
    if request.method == "POST":
        _create_post()
        return {"message":"Post created"}, HTTPStatus.CREATED
    else:
        return {"Post": _list_post()}
     
@app.route("/<int:author_id>")
def get_user_post(author_id):
    query = db.select(Post).where(Post.author_id == author_id)
    posts = db.session.execute(query).scalars().all()

    return[{
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author_id": post.author_id,
    } 
    for post in posts
    ]

@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return ({
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_id": post.author_id,            
    })

@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT