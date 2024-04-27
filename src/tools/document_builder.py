from config import Config
from utils.fileutil import path_of, read_file


def build_article(page_name, is_edit):
    wiki_prefix = Config.wiki_prefix if Config.wiki_prefix != '/' else ''
    origin = Config.origin + wiki_prefix

    wiki_title = Config.wiki_title
    template_content = read_file(path_of(
        Config.wiki_template_path, 'article.html'))

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

    content = replace_content(template_content, (
        ('{% page-title %}', wiki_title),
        ('{% post-title %}', article_title),
        ('{% post-content %}', article_html),
        ('{% global-menu %}', global_menu_content),
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
