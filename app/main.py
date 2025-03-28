import uvicorn
import uvicorn.logging

from app.core.app import app as application
from app.core.config import settings


async def app(scope, receive, send):
    await application(scope=scope, receive=receive, send=send)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
