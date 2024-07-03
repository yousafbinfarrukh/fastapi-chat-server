from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, auth, groups
from .database import engine
from .models import Base
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,  
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(groups.router)
