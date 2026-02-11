from fastapi import FastAPI
from api.v1.endpoints import auth
from config import firebase

app = FastAPI()

# router registrations
#app.include_router(users.router, prefix="/api/v1")
#app.include_router(children.router, prefix="/api/v1")
#app.include_router(milestones.router, prefix="/api/v1")
#app.include_router(reading_sessions.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


# root health check
@app.get("/")
def root():
    return {"status": "OK"}