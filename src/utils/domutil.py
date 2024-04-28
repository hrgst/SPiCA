def create_script_tag(src: str):
    ''' Generate script tag. '''
    return f'<script src="{src}" defer></script>'


def create_meta_tag(type: str, src: str):
    ''' Generate meta tag. '''
    tag = f'<link rel="{type}" href="{src}">'
    return tag


def create_image_gallery_card(image_path: str, image_name: str):
    return f'<div class="image-gallery-card"><figure><img src="{image_path}" alt="{image_name}"></figure><figcaption>{image_name}</figcaption></div>'
