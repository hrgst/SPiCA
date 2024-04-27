import json
import os
from typing import Any
import mistletoe
from mistletoe import HTMLRenderer
import yaml


def convert_markdown_to_html(markdown_content):
    return mistletoe.markdown(markdown_content, renderer=CustomHTMLRenderer)


def convert_markdown_file_to_html(markdown_path, html_path=None):
    if html_path is None:
        html_path = markdown_path.replace('.md', '.html')

    markdown_content = read_file(markdown_path)
    html_content = convert_markdown_to_html(markdown_content)
    write_file(html_path, html_content)


def path_of(*paths: str):
    return os.path.abspath(os.path.join(*paths))


def read_file(
    path: str,
    is_json: bool = False,
    is_yaml: bool = False,
):
    with open(path, mode='r', encoding='utf8') as f:
        if is_json:
            return json.load(f)
        elif is_yaml:
            return yaml.load(f, yaml.SafeLoader)
        else:
            return f.read()


def write_file(
    path: str,
    content: Any,
    is_json: bool = False,
    is_yaml: bool = False,
):
    with open(path, mode='w', encoding='utf8') as f:
        if is_json:
            json.dump(content, f, ensure_ascii=False)
        elif is_yaml:
            yaml.dump(content, f, yaml.SafeDumper, allow_unicode=True)
        else:
            f.write(content)


class CustomHTMLRenderer(HTMLRenderer):
    def render_heading(self, token):
        if token.level == 1:
            return f'<h3>{self.render_inner(token)}</h3>'
        elif token.level == 2:
            return f'<h4>{self.render_inner(token)}</h4>'
        elif token.level == 3:
            return f'<h5>{self.render_inner(token)}</h5>'
        else:
            return f'<p><b>{self.render_inner(token)}<b></p>'
