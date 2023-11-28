import os
import glob
import wgconfig.wgexec as wgexec
from typing import List
from dotenv import load_dotenv

from core.wireguard.models import Devices, Device
from core.wireguard.wg import get_interface, get_name_interface


load_dotenv()
path = os.environ.get("CONFIG_PATH")


def get_wg_interfaces() -> List[Devices]:
    conf_files = glob.glob(f"{path}/*.conf")
    devices = []
    for file_path in conf_files:
        interface, peers = get_interface(file_path)
        device = Devices(
            device=get_name_interface(file_path),
            public_key=wgexec.get_publickey(interface["PrivateKey"]),
            listen_port=interface["ListenPort"]
        )
        devices.append(device)
    return devices


def get_wg_interface(interface: str) -> List[Device]:
    conf_file = f"{path}/{interface}.conf"
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


def get_wg_peers(interface: str) -> str:
    conf_file = f"{path}/{interface}.conf"
    interface, peers = get_interface(conf_file)
    return peers