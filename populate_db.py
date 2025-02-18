import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from main import engine, SessionLocal, Item

async def insert_sample_data():
    async with SessionLocal() as session:
        async with session.begin():
            session.add_all([
                Item(name="Apple"),
                Item(name="Banana"),
                Item(name="Cherry"),
                Item(name="Date"),
                Item(name="Elderberry"),
                Item(name="Fig"),
                Item(name="Grape"),
                Item(name="Honeydew")
            ])
        await session.commit()

# Run the function to populate the database
asyncio.run(insert_sample_data())
