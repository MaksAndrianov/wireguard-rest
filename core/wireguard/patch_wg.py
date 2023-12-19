import os
import wgconfig
from dotenv import load_dotenv

from core.wireguard.wg import config_location

load_dotenv()
path = os.environ.get("CONFIG_PATH")


def disable_peer_wg(interface: str, location: str, public_key: str):
    try:
        conf_file = config_location(location, interface)

        wc = wgconfig.WGConfig(conf_file)
        wc.read_file()

        wc.disable_peer(public_key)
        wc.write_file()
    except Exception as Error:
        print(Error)

def enable_peer_wg(interface: str, location: str, public_key: str):
    try: 
        conf_file = config_location(location, interface)

        wc = wgconfig.WGConfig(conf_file)
        wc.read_file()
        wc.enable_peer(public_key)

        wc.write_file()
    except Exception as Error:
        print(Error)