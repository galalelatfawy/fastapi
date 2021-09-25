from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session
# from blog import models
from typing import Optional, Text
from fastapi import FastAPI, Depends, status, Response
from pydantic import BaseModel
from sqlalchemy.sql.expression import delete, false
from sqlalchemy.sql.functions import mode
from starlette.routing import NoMatchFound
from . import schemas, models
from .database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post ('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title , body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get ('/blog')
def get_all(db: session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get ('/blog/{id}', status_code=status.HTTP_201_CREATED)
def get_blog(id,response: Response,db: session = Depends(get_db)):
    get_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not get_blog:
        response.status_code = status.HTTP_404_NOT_FOUND
    return get_blog

@app.delete ('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return ' done'

@app.put ('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog id {id} not found")
    blog.update(request)
    db.commit()
    return 'updated'