from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.forms.post_form import PostCreate, PostResponse, PostUpdate
from database.models import Post
from utils.helpers import get_db

post_router = APIRouter()

@post_router.post("/post/create", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)) ->Post:
    db_post = Post(
        title=post.title,
        text=post.text,
        author_id=post.author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@post_router.get("/post/all", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)) ->List:
    posts = db.query(Post).all()
    return posts

@post_router.delete("/post/{post_id}", response_model=dict)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}

@post_router.put("/post/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_update.title is not None:
        post.title = post_update.title  # type: ignore
    if post_update.text is not None:
        post.text = post_update.text # type: ignore

    db.commit()
    db.refresh(post)
    return post