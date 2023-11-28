import os
import wgconfig
from dotenv import load_dotenv

load_dotenv()
path = os.environ.get("CONFIG_PATH")
client_config_path = os.environ.get("CLIENT_CONFIG_PATH")
DNS = os.environ.get("DNS")


def get_interface(path: str) -> tuple[str, str]:
    wc = wgconfig.WGConfig(path)
    wc.read_file()
    return wc.get_interface(), wc.get_peers(keys_only=False)


def get_name_interface(path: str) -> str:
    file_name = os.path.basename(path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension
