from config import Config
from utils.fileutil import path_of, read_file, write_file, convert_markdown_file_to_html
from utils.domutil import create_script_tag, create_meta_tag


def build_article(page_name, is_edit):
    wiki_prefix = Config.wiki_prefix if Config.wiki_prefix != '/' else ''
    origin = Config.origin + wiki_prefix
    article_url = origin + f'?page={page_name}'
    editor_url = article_url + '&edit'

    wiki_title = Config.wiki_title
    template_name = 'article-editor' if is_edit else 'article'
    template_content = read_file(path_of(
        Config.wiki_template_path, f'{template_name}.html'))

    article_meta: dict = read_file(
        path_of(Config.wiki_article_path, f'{page_name}.yaml'), is_yaml=True)
    article_title = article_meta.get('title')
    article_html = read_file(
        path_of(Config.wiki_article_path, f'{page_name}.html'))

    article_markdown_path = path_of(
        Config.wiki_article_path, f'{page_name}.md')
    article_markdown = read_file(article_markdown_path) if is_edit else ''

    global_menu_content = read_file(
        path_of(Config.wiki_article_path, 'menu.html'))

    script_content = ''
    script_src_map = (
        f'{origin}/js/wiki.js',
    )
    for script_src in script_src_map:
        script_content += create_script_tag(script_src)

    meta_content = ''
    meta_src_map = (
        ('stylesheet', f'{origin}/css/wiki.css'),
    )
    for meta_type, meta_src in meta_src_map:
        meta_content += create_meta_tag(meta_type, meta_src)

    content = replace_content(template_content, (
        ('{% page-title %}', wiki_title),
        ('{% post-name %}', page_name),
        ('{% post-title %}', article_title),
        ('{% post-content %}', article_html),
        ('{% post-source %}', article_markdown),
        ('{% global-menu %}', global_menu_content),
        ('{% metas %}', meta_content),
        ('{% scripts %}', script_content),
        ('{% article-url %}', article_url),
        ('{% editor-url %}', editor_url),
    ))

    return optimize_html(content)


def optimize_html(content, unescape=True, minify=True):
    import html
    import htmlmin

    if minify:
        content = htmlmin.minify(content)

    if unescape:
        content = html.unescape(content)

    return content


def replace_content(content: str, replace_contents: tuple):
    final_content = content
    for keyword, content in replace_contents:
        final_content = final_content.replace(keyword, content)
    return final_content


def update_article(article_name, article_title, article_content):
    markdown_path = path_of(
        Config.wiki_article_path, f'{article_name}.md')
    write_file(markdown_path, article_content)
    convert_markdown_file_to_html(markdown_path)

    meta_path = path_of(
        Config.wiki_article_path, f'{article_name}.yaml')
    meta_data: dict = read_file(meta_path, is_yaml=True)
    meta_data['title'] = article_title
    write_file(meta_path, meta_data, is_yaml=True)
