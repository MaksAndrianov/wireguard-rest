import os
import glob
import wgconfig
import wgconfig.wgexec as wgexec
from typing import List
from core.wireguard.models import Devices, Device
from dotenv import load_dotenv

load_dotenv()
path = os.environ.get("CONFIG_PATH")


def get_interface(path: str) -> tuple[str, str]:
    wc = wgconfig.WGConfig(path)
    wc.read_file()
    return wc.get_interface(), wc.get_peers(keys_only=False)


def get_name_interface(path: str) -> str:
    file_name = os.path.basename(path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension

# GET


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



def get_wg_interface(name: str) -> List[Device]:
    conf_file = f"{path}/{name}.conf"
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


def get_wg_peers(name: str) -> str:
    conf_file = f"{path}/{name}.conf"
    interface, peers = get_interface(conf_file)
    return peers

# POST

# PATCH

# DELETE


def del_wg_interface(name: str) -> str:
    conf_file = f"{path}/{name}.conf"
    try:
        os.remove(conf_file)
        return [{"device": name, "state": "Deleted"}]
    except:
        return [{"device": name, "state": "Not Found"}]
