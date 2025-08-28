from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
from .dependencies import get_query_token, get_token_header
# from .internal import admin
from .routers import chat, files
# , files

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()#dependencies=[Depends(get_query_token)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


app.include_router(chat.router)
app.include_router(files.router)
# app.include_router(files.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}