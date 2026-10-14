from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from core.database import engine, Base
from api.routes import documents, audit, chat

# Initialize tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}