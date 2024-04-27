import os


class Config:

    exec_path: str
    root_path: str
    hostname: str
    port: str
    prefix: str
    origin: str

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
