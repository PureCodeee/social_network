from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


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


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type ="photo",
        file_name="dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post



@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}