import os
import wgconfig
from dotenv import load_dotenv


load_dotenv()
path = os.environ.get("CONFIG_PATH")


def del_wg_interface(interface: str) -> str:
    conf_file = f"{path}/{interface}.conf"
    try:
        os.remove(conf_file)
        return [{"device": interface, "state": "Deleted"}]
    except:
        return [{"device": interface, "state": "Not Found"}]


def del_wg_peer(interface: str, public_key: str) -> str:
    try:
        conf_file = f"{path}/{interface}.conf"
        wc = wgconfig.WGConfig(conf_file)
        wc.read_file()
        wc.del_peer(public_key)
        wc.write_file()
        return [{"peer": public_key, "state": "Deleted"}]
    except:
        return [{"peer": interface, "state": "Not Found"}]
