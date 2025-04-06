import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.presentation.api.v1.lifespan import lifespan
from app.presentation.api.v1.routes import auth, campaign, user

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error for {request.url}: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal database error occurred."},
    )

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):

    error_message = str(exc)
    logger.error(f"Unhandled ValueError for {request.url}: {error_message}", exc_info=True)
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail_message = "An internal error occurred due to invalid value."

    if "not found" in error_message.lower():
         status_code = status.HTTP_404_NOT_FOUND
         detail_message = error_message

    return JSONResponse(
        status_code=status_code,
        content={"detail": detail_message},
    )

api_prefix = settings.API_V1_STR

app.include_router(user.router, prefix=f"{api_prefix}/users", tags=["Users"])
app.include_router(
    campaign.router, prefix=f"{api_prefix}/campaigns", tags=["Campaigns"]
)
app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Fast Api router initialized")


@app.get("/")
def read_root():
    return {"message": "Welcome to the DDD-style FastAPI ad campaign management 🚀"}
