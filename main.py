from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def read_root():
    return {"massage": "hello world"}


@app.get("/root")
def root():
    return {"massage": "this is root mesasge"}


@app.get("/posts")
def getPost():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(new_post: Posts):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts/latest")
def getPostLatest():
    post = my_posts[-1]
    return {"data": post}


@app.get("/posts/{id}")
def getPost(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not exists.",
        )

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not exists.",
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def updatePost(id: int, post: Posts):
    index = find_post_index(id)
    print(index)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not exists.",
        )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
