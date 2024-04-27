import os
import sys


def init():
    # Set environment variable
    sys.path.append(
        os.path.dirname(os.path.abspath(__file__)))

    from glob import glob
    from config import Config
    from utils.fileutil import convert_markdown_file_to_html, convert_scss_file_to_css, path_of

    # Initialize config
    Config.init()

    # Convert all markdowns
    for markdown_file in glob(path_of(Config.wiki_article_path, '*.md')):
        convert_markdown_file_to_html(markdown_file)

    # Compile all scss
    for scss_file in glob(path_of(Config.wiki_static_path, '**', '*.scss'), recursive=True):
        scss_basename = os.path.basename(scss_file)
        if not scss_basename.startswith('_'):
            convert_scss_file_to_css(scss_file)


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
