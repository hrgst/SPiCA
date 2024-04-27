import os
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, FileResponse, Response
from config import Config
from utils.fileutil import path_of
from tools.document_builder import build_article

router = APIRouter()
global_prefix = Config.prefix if Config.prefix != '/' else ''
prefix = global_prefix + Config.wiki_prefix


@router.get(prefix)
def get_article(page: str, edit: str = None):

    article_name = page
    is_edit = edit is None

    return HTMLResponse(build_article(article_name, is_edit))


@router.get(prefix+'/{path:path}')
def get_file(path: str):
    filepath = path_of(Config.wiki_static_path, path)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return Response('404 not found', 404)
