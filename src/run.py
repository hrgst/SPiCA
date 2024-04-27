import os
import sys


def init():
    # Set environment variable
    sys.path.append(
        os.path.dirname(os.path.abspath(__file__)))

    # Initialize config
    from config import Config
    Config.init()


def run():
    from fastapi import FastAPI
    import uvicorn
    from config import Config
    from routers import ALL_ROUTERS

    # Create WebAPI
    app = FastAPI()
    for router in ALL_ROUTERS:
        app.include_router(router)

    # Run API
    try:
        uvicorn.run(app, host=Config.hostname, port=Config.port)
    except KeyboardInterrupt as e:
        pass


if __name__ == '__main__':
    init()
    run()
