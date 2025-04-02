import logging

from fastapi import FastAPI

from app.core.config import settings
from app.presentation.api.v1.lifespan import lifespan
from app.presentation.api.v1.routes import auth, campaign, user

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

api_prefix = settings.API_V1_STR

app.include_router(user.router, prefix=f"{api_prefix}/users", tags=["Users"])
app.include_router(
    campaign.router, prefix=f"{api_prefix}/campaigns", tags=["Campaigns"]
)
app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])

logger.info("Fast Api router initialized")


@app.get("/")
def read_root():
    return {"message": "Welcome to the DDD-style FastAPI ad campaign management 🚀"}
