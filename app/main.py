from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.exceptions import TokenExpiredException, TokenNotFoundException
from app.users.routers import auth_routers, friendship_routers

from app.chat.routers import router as chat_routers

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routers)
app.include_router(friendship_routers)
app.include_router(chat_routers)


@app.exception_handler(TokenNotFoundException)
@app.exception_handler(TokenExpiredException)
async def handle_token_exceptions(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth/login", status_code=302)
