from fastapi import FastAPI
from models.database import create_db_and_tables
from routes.routes_auth import router as auth_router
from routes.routes_courses import router as courses_router
from routes.routes_enrollments import router as enrollments_router
from routes.routes_etc import router as etc_router
from routes.routes_role import router as roles_router
from routes.routes_students import router as students_router
from routes.routes_user import router as users_router
from core.redis_client import init_redis_pool, close_redis_pool

app = FastAPI()

@app.on_event("startup")
def on_startup():
    
    create_db_and_tables()

@app.on_event("startup")
async def _startup_redis() -> None:
    # initialize logging first if you do that already
    await init_redis_pool()

app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(users_router)
app.include_router(etc_router)

@app.on_event("shutdown")
async def _shutdown_redis() -> None:
    await close_redis_pool()

@app.get("/")
def home():
    return {"message": "Hello University"}
