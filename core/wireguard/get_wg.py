import os
import glob
import wgconfig.wgexec as wgexec
from typing import List
from dotenv import load_dotenv

from core.wireguard.models import Devices, Device
from core.wireguard.wg import get_interface, get_name_interface, get_location, config_location


load_dotenv()
path = os.environ.get("CONFIG_PATH")
client_config_path = os.environ.get("CLIENT_CONFIG_PATH")


def get_wg_interfaces() -> List[Devices]:
    conf_files = glob.glob(os.path.join(path, '**/*.conf'), recursive=True)
    devices = []
    for file_path in conf_files:
        interface, peers = get_interface(file_path)
        
        location = get_location(file_path)

        device = Devices(
            device=get_name_interface(file_path),
            location=location,
            public_key=wgexec.get_publickey(interface["PrivateKey"]),
            listen_port=interface["ListenPort"]
        )
        devices.append(device)
    return devices


def get_wg_interface(interface: str, location: str) -> List[Device]:
    conf_file = config_location(location, interface)
    interface, peers = get_interface(conf_file)
    listen_port = interface["ListenPort"]

    return Device(
        public_key=wgexec.get_publickey(interface["PrivateKey"]),
        listen_port=listen_port,
        address=interface["Address"],
        preup=interface["PreUp"] if "PreUp" in interface else None,
        postup=interface["PostUp"] if "PostUp" in interface else None,
        predown=interface["PreDown"] if "PreDown" in interface else None,
        postdown=interface["PostDown"] if "PostDown" in interface else None,
        num_peers=len(peers)
    )


def get_wg_peers(interface: str, location: str) -> str:
    conf_file = config_location(location, interface)
    interface, peers = get_interface(conf_file)
    return peers


def get_wg_peer(interface: str, peer: str, location: str):
    conf_file = config_location(location, interface)
    interface, peers = get_interface(conf_file)
    return peers[peer]


def get_wg_peer_config(interface: str, public_key: str, location: str):
    client = public_key.replace('/', '%2F')

    # Put it in a separate function
    if location is None:
        client_directory = client
    else:
        client_directory = f"{location}/{client}"

    get_peer = get_wg_peers(interface, location)
    check = get_peer[public_key] if public_key in get_peer else None,
    
    if not os.path.exists(f"{client_config_path}/{client_directory}") or check[0] is None:
        return 404
    else: 
        config = f'{client_config_path}/{client_directory}/wgclient.conf'
        qr = f'{client_config_path}/{client_directory}/qr.png'
        return config, qr
