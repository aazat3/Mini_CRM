from fastapi import FastAPI


from app.config import settings
from app.routers import operators, sources, contacts, leads, stats


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(operators.router)
app.include_router(sources.router)
app.include_router(contacts.router)
app.include_router(leads.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    return {"service": settings.PROJECT_NAME, "docs": "/docs"}