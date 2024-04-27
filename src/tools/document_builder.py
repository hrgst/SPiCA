from config import Config
from utils.fileutil import path_of, read_file


def build_article(page_name, is_edit):
    template_content = read_file(path_of(
        Config.wiki_template_path, 'article.html'))
    return optimize_html(template_content)


def optimize_html(content, unescape=True, minify=True):
    import html
    import htmlmin

    if minify:
        content = htmlmin.minify(content)

    if unescape:
        content = html.unescape(content)

    return content
