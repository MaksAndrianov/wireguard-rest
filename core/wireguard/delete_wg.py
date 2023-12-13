import os
import wgconfig
from dotenv import load_dotenv
from core.wireguard.wg import config_location


load_dotenv()
path = os.environ.get("CONFIG_PATH")
client_config_path = os.environ.get("CLIENT_CONFIG_PATH")


def del_wg_interface(interface: str, location: str) -> str:
    conf_file = config_location(location, interface)
    try:
        os.remove(conf_file)
        return [{"device": interface, "state": "Deleted"}]
    except:
        return [{"device": interface, "state": "Not Found"}]


def del_wg_peer(interface: str, public_key: str, location: str) -> str:
    client = public_key.replace('/', '%2F')
    if location is None:
        client_directory = f'{client_config_path}/{client}'
    else:
        client_directory = f"{client_config_path}/{location}/{client}"

    try:
        conf_file = config_location(location, interface)
        wc = wgconfig.WGConfig(conf_file)
        wc.read_file()
        wc.del_peer(public_key)
        wc.write_file()
        try:
            files = os.listdir(client_directory)
            for file in files:
                os.remove(f"{client_directory}/{file}")
            os.rmdir(client_directory)
        except Exception as Error:
            print(Error)
            
        return [{"peer": public_key, "state": "Deleted"}]
    except:
        return [{"peer": interface, "state": "Not Found"}]
