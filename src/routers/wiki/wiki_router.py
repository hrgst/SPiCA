from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from config import Config
from tools.document_builder import build_article

router = APIRouter()
global_prefix = Config.prefix if Config.prefix != '/' else ''
prefix = global_prefix + Config.wiki_prefix


@router.get(prefix)
def get_article(page: str, edit: str = None):

    article_name = page
    is_edit = edit is None

    return HTMLResponse(build_article(article_name, is_edit))
