from fastapi import FastAPI
app = FastAPI()


@app.get ('/')
def index():
    return {'data': {'name':'Galal'}}


@app.get ('/blog/{id}')
def blog(id):
    return {'name': id}

@app.get ('/blog/{id}/{comment}')
def comment(comment):
    return {'data': {'comment':'first comment'}}