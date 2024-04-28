from config import Config
from utils.fileutil import delete_file, path_of, read_file, write_file, convert_markdown_file_to_html
from utils.domutil import create_script_tag, create_meta_tag, create_image_gallery_card


def build_article(page_name, is_edit):
    ''' Build article HTML. '''

    wiki_prefix = Config.wiki_prefix if Config.wiki_prefix != '/' else ''
    origin = Config.origin + wiki_prefix
    article_url = origin + f'?page={page_name}'
    editor_url = article_url + '&edit'
    global_menu_editor_url = origin + f'?page=menu&edit'

    # Wiki Title
    wiki_title = Config.wiki_title

    # Page template
    template_name = 'article-editor' if is_edit else 'article'
    template_content = read_file(path_of(
        Config.wiki_template_path, f'{template_name}.html'))

    try:
        # Article content
        article_meta: dict = read_file(
            path_of(Config.wiki_article_path, f'{page_name}.yaml'), is_yaml=True)
        article_title = article_meta.get('title')
        article_html = read_file(
            path_of(Config.wiki_article_path, f'{page_name}.html'))

        # Article markdown (if edit mode)
        article_markdown_path = path_of(
            Config.wiki_article_path, f'{page_name}.md')
        article_markdown = read_file(article_markdown_path) if is_edit else ''

    except FileNotFoundError as e:
        # Build edit page if file not found and accessed edit page
        if is_edit:
            article_title = '新規ページ'
            article_html = ''
            article_markdown = ''
        else:
            raise e

    # Global menu content
    global_menu_content = read_file(
        path_of(Config.wiki_article_path, 'menu.html'))

    # Scripts
    script_content = ''
    script_src_map = (
        f'{origin}/js/wiki.js',
    )
    for script_src in script_src_map:
        script_content += create_script_tag(script_src)

    # Metas
    meta_content = ''
    meta_src_map = (
        ('stylesheet', f'{origin}/css/wiki.css'),
        ('icon', f'{origin}/favicon.webp'),
    )
    for meta_type, meta_src in meta_src_map:
        meta_content += create_meta_tag(meta_type, meta_src)

    # Replace infos
    content = replace_content(template_content, (
        ('{% page-title %}', wiki_title),
        ('{% post-name %}', page_name),
        ('{% post-title %}', article_title),
        ('{% post-content %}', article_html),
        ('{% post-source %}', article_markdown),
        ('{% global-menu %}', global_menu_content),
        ('{% metas %}', meta_content),
        ('{% scripts %}', script_content),
        ('{% origin %}', origin),
        ('{% article-url %}', article_url),
        ('{% editor-url %}', editor_url),
        ('{% menu-editor-url %}', global_menu_editor_url)
    ))

    return optimize_html(content)


def build_image_gallery(page: int):
    page_name = '画像'
    wiki_prefix = Config.wiki_prefix if Config.wiki_prefix != '/' else ''
    origin = Config.origin + wiki_prefix
    article_url = '#'
    editor_url = '#'
    global_menu_editor_url = origin + f'?page=menu&edit'

    # Wiki Title
    wiki_title = Config.wiki_title

    # Page template
    template_content = read_file(path_of(
        Config.wiki_template_path, f'article.html'))

    # Article content
    image_gallery_panel = read_file(
        path_of(Config.wiki_template_path, 'image-gallery-panel.html'))

    user_images_path = path_of(Config.wiki_static_path, 'user-images')
    user_images_meta = read_file(path_of(
        user_images_path, 'user-images.json'), is_json=True)
    image_gallery_content = ''
    user_images = user_images_meta.get('images')
    for user_image in user_images:
        image_filename = user_image.get('filename')
        image_path = f'{origin}/user-images/{image_filename}'
        image_gallery_content += create_image_gallery_card(
            image_path, image_filename)

    # Global menu content
    global_menu_content = read_file(
        path_of(Config.wiki_article_path, 'menu.html'))

    # Scripts
    script_content = ''
    script_src_map = (
        f'{origin}/js/wiki.js',
    )
    for script_src in script_src_map:
        script_content += create_script_tag(script_src)

    # Metas
    meta_content = ''
    meta_src_map = (
        ('stylesheet', f'{origin}/css/wiki.css'),
        ('icon', f'{origin}/favicon.webp'),
    )
    for meta_type, meta_src in meta_src_map:
        meta_content += create_meta_tag(meta_type, meta_src)

    # Replace infos
    content = replace_content(template_content, (
        ('{% page-title %}', wiki_title),
        ('{% post-name %}', page_name),
        ('{% post-title %}', page_name),
        ('{% post-content %}', image_gallery_panel),
        ('{% global-menu %}', global_menu_content),
        ('{% metas %}', meta_content),
        ('{% scripts %}', script_content),
        ('{% origin %}', origin),
        ('{% article-url %}', article_url),
        ('{% editor-url %}', editor_url),
        ('{% menu-editor-url %}', global_menu_editor_url),
        ('{% image-gallery-cards %}', image_gallery_content),
    ))
    return content


def optimize_html(content, unescape=True, minify=True):
    ''' Unescape and minimize HTML. '''
    import html
    import htmlmin

    if minify:
        content = htmlmin.minify(content)

    if unescape:
        content = html.unescape(content)

    return content


def replace_content(content: str, replace_contents: tuple):
    ''' Replace function. '''
    final_content = content
    for keyword, content in replace_contents:
        final_content = final_content.replace(keyword, content)
    return final_content


def update_article(article_name, article_title, article_content):
    ''' Update an article. '''

    # Delete function if content is empty
    is_delete = article_content == ''

    # Article paths
    html_path = path_of(
        Config.wiki_article_path, f'{article_name}.html')
    markdown_path = path_of(
        Config.wiki_article_path, f'{article_name}.md')
    meta_path = path_of(
        Config.wiki_article_path, f'{article_name}.yaml')

    # Try to get meta data
    try:
        meta_data: dict = read_file(meta_path, is_yaml=True)
    except FileNotFoundError as e:
        meta_data = {}

    if is_delete:
        # Interrupt deleting if undeletable article
        if not meta_data['deletable']:
            return

        # Delete HTML, markdown and meta
        for delete_path in (markdown_path, meta_path, html_path):
            try:
                delete_file(delete_path)
            except Exception as e:
                pass
    else:
        # Overwrite files if NOT delete mode
        write_file(markdown_path, article_content)
        convert_markdown_file_to_html(markdown_path)

        meta_data['title'] = article_title
        write_file(meta_path, meta_data, is_yaml=True)
