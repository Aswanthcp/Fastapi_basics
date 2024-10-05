from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "id": 1,
        "title": "post1",
        "content": "content of post1",
    },
    {
        "id": 2,
        "title": "post2",
        "content": "content of post2",
    },
]


@app.get("/")
def read_root():
    return {"massage": "hello world"}


@app.get("/root")
def root():
    return {"massage": "this is root mesasge"}


@app.get("/posts")
def getPost():
    return {"data": my_posts}


@app.post("/posts")
def createPost(new_post: Posts):
    print(new_post)
    print(new_post.model_dump())
    return {"new_post": "new post"}
