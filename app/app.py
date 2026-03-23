from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {"title": "new post", "content": "cool test post"},
    2: {"title": "Weekend Vibes", "content": "Enjoying a sunny Saturday at the park!"},
    3: {"title": "Tech Update", "content": "Just learned about Python generators. Mind = blown!"},
    4: {"title": "Recipe of the Day", "content": "Try this amazing pasta carbonara recipe!"},
    5: {"title": "Fitness Journey", "content": "Day 30 of my workout challenge. Feeling great!"},
    6: {"title": "Book Review", "content": "Just finished 'The Midnight Library'. Highly recommend!"},
    7: {"title": "Travel Tips", "content": "Top 5 places to visit in Japan this spring."},
    8: {"title": "Productivity Hack", "content": "Use the Pomodoro technique to boost focus!"},
    9: {"title": "Movie Night", "content": "Watched 'Dune 2' last night. Amazing visuals!"},
    10: {"title": "Quote of the Day", "content": "The only way to do great work is to love what you do."}
}


@app.get("/posts")
def get_all_posts(limit: int):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts





