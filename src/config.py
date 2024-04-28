import os


class Config:

    __version__ = '1.0.0'
    __author__ = 'Hiragi Sota'
    __application__ = 'SwiftFlow'

    exec_path: str
    root_path: str
    config_all: dict
    hostname: str
    port: str
    prefix: str
    origin: str
    wiki_prefix: str
    wiki_title: str
    wiki_article_path: str
    wiki_static_path: str
    wiki_template_path: str

    @classmethod
    def init(cls):
        from utils.fileutil import path_of, read_file

        # General paths
        exec_path: str = os.path.dirname(os.path.abspath(__file__))
        root_path: str = path_of(exec_path, '../')
        # Register general paths
        cls.exec_path = exec_path
        cls.root_path = root_path

        # All config
        config_path: str = path_of(root_path, 'settings.yaml')
        config_all: dict = read_file(config_path, is_yaml=True)
        # Register all config
        cls.config_all = config_all

        # Network config
        network_config: dict = config_all.get('network')
        protocol: str = network_config.get('protocol')
        hostname: str = network_config.get('host')
        port: str = network_config.get('port')
        prefix: str = network_config.get('prefix')
        origin: str = f'{protocol}://{hostname}:{port}{prefix if prefix != "/" else ""}'
        # Register network config
        # cls.network_config = network_config
        # cls.protocol = protocol
        cls.hostname = hostname
        cls.port = port
        cls.prefix = prefix
        cls.origin = origin

        # Wiki config
        wiki_config: dict = config_all.get('wiki')
        wiki_prefix: str = wiki_config.get('prefix')
        wiki_title: str = wiki_config.get('title')
        wiki_article_path: str = path_of(
            root_path + wiki_config.get('article'))
        wiki_static_path: str = path_of(
            root_path + wiki_config.get('static'))
        wiki_template_path: str = path_of(
            root_path + wiki_config.get('template'))
        # Create wiki paths
        os.makedirs(wiki_article_path, exist_ok=True)
        os.makedirs(wiki_static_path, exist_ok=True)
        os.makedirs(wiki_template_path, exist_ok=True)
        # Register wiki config
        cls.wiki_prefix = wiki_prefix
        cls.wiki_title = wiki_title
        cls.wiki_article_path = wiki_article_path
        cls.wiki_static_path = wiki_static_path
        cls.wiki_template_path = wiki_template_path
