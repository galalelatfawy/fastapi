from typing import Optional, Text
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


@app.get ('/')
def index():
    return {'data': {'name':'Galal'}}

@app.get ('/blog/unpublished')
def unpublished():
    return {'data': 'Unpublished'}

@app.get ('/blog')
def blog(limit: Optional[int]=10,published: Optional [bool]=True, sort: Optional[str] = None):
    if published:

        return {'data': f'Blog List of published {limit} topics'}
    else:
        return {'data': f'Blog List of {limit} topics'}

@app.get ('/blog/{id}')
def blog(id: int):
    return {'name': id}


@app.get ('/blog/{id}/{comment}')
def comment(comment: str):
    return {'data': {'comment':'first comment'}}

class newblog(BaseModel):
    title: str
    description: Optional[str] = None
    body: str


@app.post ('/blog')
def newpost(request: newblog):
    return {'data': f'New post created with title {request.title}'}
