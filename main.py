import uvicorn
import uvicorn.logging

from app.core.app import app as application


async def app(scope, receive, send):
    await application(scope=scope, receive=receive, send=send)


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8080, reload=True)
