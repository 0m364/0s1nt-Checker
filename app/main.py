from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.routes import router as api_router
from app.gui.routes import router as gui_router
from app.gui.admin_routes import router as admin_router
from app.middleware import AccessLogMiddleware
from app.core.config import settings
from app.core.logging import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.add_middleware(AccessLogMiddleware)

templates = Jinja2Templates(directory="app/templates")

app.include_router(api_router, prefix="/api")
app.include_router(gui_router)
app.include_router(admin_router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
