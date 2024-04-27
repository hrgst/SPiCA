def create_script_tag(src: str):
    return f'<script src="{src}" defer></script>'


def create_meta_tag(type: str, src: str):
    tag = ''
    if type == 'stylesheet':
        tag = f'<link rel="stylesheet" href="{src}">'
    return tag
