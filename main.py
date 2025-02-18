from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database setup (SQLite async)
DATABASE_URL = "sqlite+aiosqlite:///./search.db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Database model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Create the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()  # Ensure DB is created on startup

# Homepage route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Search route (Async database query)
@app.get("/search")
async def search(q: str, db: AsyncSession = Depends(get_db)):
    if not q:
        return JSONResponse(content={"results": []})

    query = select(Item).where(Item.name.ilike(f"%{q}%"))
    result = await db.execute(query)
    items = result.scalars().all()
    return JSONResponse(content={"results": [item.name for item in items]})
