def create_script_tag(src: str):
    ''' Generate script tag. '''
    return f'<script src="{src}" defer></script>'


def create_meta_tag(type: str, src: str):
    ''' Generate meta tag. '''
    tag = f'<link rel="{type}" href="{src}">'
    return tag
