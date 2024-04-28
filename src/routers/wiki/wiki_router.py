import os
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from config import Config
from utils.fileutil import path_of, convert_markdown_to_html
from tools.document_builder import build_article, optimize_html, update_article

router = APIRouter()
global_prefix = Config.prefix if Config.prefix != '/' else ''
prefix = global_prefix + Config.wiki_prefix


@router.get(prefix+'/{path:path}')
async def get_file_route(path: str):
    filepath = path_of(Config.wiki_static_path, path)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return Response('404 not found', 404)


@router.get(prefix)
async def get_article_route(page: str, edit: str = None):
    is_edit = not edit is None
    article_name = page

    article_content = None
    try:
        article_content = build_article(article_name, is_edit)
    except FileNotFoundError as e:
        redirect_url = Config.origin + prefix + f'?page={page}&edit'
        return RedirectResponse(redirect_url)

    return HTMLResponse(article_content)


@router.post(prefix+'/preview')
async def get_article_preview_route(req: Request):
    request = await req.json()
    html_content = optimize_html(
        convert_markdown_to_html(request.get('markdown')))
    return JSONResponse({'content': html_content})


@router.post(prefix+'/submit')
async def update_article_route(req: Request):
    request = await req.json()
    article_title = request.get('title')
    article_key = request.get('article')
    article_markdown = request.get('markdown')

    update_article(article_key, article_title, article_markdown)

    is_delete = article_markdown == ''
    redirect_page = 'home' if is_delete else article_key
    redirect_url = Config.origin + prefix + f'?page={redirect_page}'

    return JSONResponse({'redirect': redirect_url})
