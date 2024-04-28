import os
from io import BytesIO
from PIL import Image
from typing import Annotated
from fastapi import File
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from config import Config
from utils.fileutil import path_of, convert_markdown_to_html, read_file, write_file, delete_file
from tools.document_builder import build_article, build_image_gallery, optimize_html, update_article

router = APIRouter()
global_prefix = Config.prefix if Config.prefix != '/' else ''
prefix = global_prefix + Config.wiki_prefix


@router.get(prefix+'/{path:path}')
async def get_file_route(path: str):
    ''' Get a static file. '''

    filepath = path_of(Config.wiki_static_path, path)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return Response('404 not found', 404)


@router.get(prefix)
async def get_article_route(page: str, edit: str = None):
    ''' Get an article page. '''

    is_edit = not edit is None
    article_name = page

    article_content = None
    if page == 'image-gallery':
        article_content = build_image_gallery(1)  # TODO:
    else:
        try:
            # Build article HTML
            article_content = build_article(article_name, is_edit)
        except FileNotFoundError as e:
            # Show edit page if not found article
            redirect_url = Config.origin + prefix + f'?page={page}&edit'
            return RedirectResponse(redirect_url)

    return HTMLResponse(article_content)


@router.post(prefix+'/preview')
async def get_article_preview_route(req: Request):
    ''' Return converted HTML from markdown. '''
    request = await req.json()

    # Return content converted to HTML
    html_content = optimize_html(
        convert_markdown_to_html(request.get('markdown')))
    return JSONResponse({'content': html_content})


@router.post(prefix+'/submit')
async def update_article_route(req: Request):
    ''' Update or delete an article. '''
    request = await req.json()

    # Get content information
    article_title = request.get('title')
    article_key = request.get('article')
    article_markdown = request.get('markdown')

    # Update article files
    update_article(article_key, article_title, article_markdown)

    # Redirect to home page if content deleted
    is_delete = article_markdown == ''
    redirect_page = 'home' if is_delete else article_key
    redirect_url = Config.origin + prefix + f'?page={redirect_page}'

    return JSONResponse({'redirect': redirect_url})


@router.post(prefix+'/image/add')
async def add_image(req: Request):
    ''' Update or delete an article. '''
    request = await req.form()

    image_data = request.get('image')
    image_bytes = await image_data.read()
    image = Image.open(BytesIO(image_bytes))

    image_save_dir = path_of(Config.wiki_static_path, 'user-images')

    file_name = request.get('filename')
    webp_file_name = file_name[:file_name.rfind('.')] + '.webp'
    image_file_path = path_of(image_save_dir, webp_file_name)

    if os.path.exists(image_file_path):
        return JSONResponse({'error': 'FileExist'})

    image.save(image_file_path, quality=90)

    images_meta_path = path_of(image_save_dir, 'user-images.json')
    images_meta = read_file(images_meta_path, is_json=True)
    images_meta['images'].append({'filename': webp_file_name})
    write_file(images_meta_path, images_meta, is_json=True)
    return JSONResponse({})


@router.post(prefix+'/image/delete')
async def delete_image(req: Request):
    ''' Update or delete an article. '''
    request = await req.json()

    image_save_dir = path_of(Config.wiki_static_path, 'user-images')

    file_name = request['filename']
    webp_file_name = file_name[:file_name.rfind('.')] + '.webp'
    image_file_path = path_of(image_save_dir, webp_file_name)
    try:
        delete_file(image_file_path)
    except Exception as e:
        pass

    images_meta_path = path_of(image_save_dir, 'user-images.json')
    images_meta = read_file(images_meta_path, is_json=True)
    image_list = images_meta['images']
    delete_index = []
    for n, image_path in enumerate(image_list):
        if file_name == image_path['filename']:
            delete_index.append(n)
    delete_index.sort(reverse=True)
    for index in delete_index:
        image_list.pop(index)
    write_file(images_meta_path, images_meta, is_json=True)

    print(file_name)
    return ''
