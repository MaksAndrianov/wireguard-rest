import os
import ipaddress
import requests
import wgconfig
import wgconfig.wgexec as wgexec
from dotenv import load_dotenv

from core.wireguard.wg import genetate_qr
from core.wireguard.get_wg import get_wg_peers, get_wg_interface, config_location


load_dotenv()
path = os.environ.get("CONFIG_PATH")
client_config_path = os.environ.get("CLIENT_CONFIG_PATH")
DNS = os.environ.get("DNS")
SERVER_IP = os.environ.get("SERVER_IP")
# Server env
SERVER_ADDRESS = os.environ.get("ADDRESS")
SERVER_PORT = os.environ.get("PORT")
POSTUP = os.environ.get("POSTUP")
POSTDOWN = os.environ.get("POSTDOWN")


if SERVER_IP is None:
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    SERVER_IP = data.get('ip')


def create_wg_peer(interface: str, serer_ip: str, private_key: str, presharedkey: bool, location: str):
    conf_file = config_location(location, interface)

    wc = wgconfig.WGConfig(conf_file)
    wc.read_file()

    server = wc.get_interface()

    if private_key is None:
        private_key, public_key = wgexec.generate_keypair()
    else: 
        public_key = wgexec.get_publickey(private_key)

    # Put it in a separate function
    client = public_key.replace('/', '%2F')
    if location is None:
        client_directory = client
    else:
        client_directory = f"{location}/{client}"

    get_peer = get_wg_peers(interface, location)
    check=get_peer[public_key] if public_key in get_peer else None,

    if os.path.exists(f"{client_config_path}/{client_directory}") or check[0] is not None:
        return 404
    else:
        # Maybe it needs to be moved to a separate function, as it is done for QR code generation?
        os.makedirs(f"{client_config_path}/{client_directory}")

        wc.add_peer(public_key)

        # IP 
        possible_ips = set(ipaddress.IPv4Network(item.get("AllowedIPs")) for item in get_peer.values() if "AllowedIPs" in item)
        server_gateway_ip = server["Address"]
        ip_prefix = ".".join(server_gateway_ip.split(".")[:-1])
        if serer_ip is None:
            serer_ip = SERVER_IP
    
        all_possible_ips = set(ipaddress.IPv4Network(f"{ip_prefix}.{i}/32") for i in range(2, 254))
        free_ips = all_possible_ips - possible_ips
        first_free_ip = list(free_ips)[-1] if free_ips else None

        wc.add_attr(public_key, "AllowedIPs", first_free_ip)

        if presharedkey:
            key = wgexec.generate_presharedkey()
            wc.add_attr(public_key, "PresharedKey", key)

        wc.write_file()


        with open(f'{client_config_path}/{client_directory}/wgclient.conf', 'w') as file:
            file.write(
                f"[Interface]\n"
                f"PrivateKey = {private_key}\n"
                f"Address = {str(first_free_ip).replace('/32', '/24')}\n"
                f'DNS = {DNS}\n\n'
                f'[Peer]\n'
                f'PublicKey = {wgexec.get_publickey(server["PrivateKey"])}\n'
                f"AllowedIPs = 0.0.0.0/0 \n"
                f'Endpoint = {serer_ip}:{server["ListenPort"]}\n'
                f'PersistentKeepalive = 10\n'
                f'{f"PresharedKey = {key} \n" if presharedkey else ""}'
            )
    genetate_qr(f'{client_config_path}/{client_directory}/wgclient.conf', f'{client_config_path}/{client_directory}')

    return {"detail": "created", "peer": public_key}
 

def create_wg_interface(name: str, server_ip: str, port: int, preup: str, postup: str, predown: str, postdown: str, location: str):
    if location is None:
        conf_file = f"{path}/{name}.conf"
    else:
        conf_file = f"{path}/{location}/{name}.conf"
        os.makedirs(f"{path}/{location}")
    if os.path.exists(conf_file):
        return None
    else:
        private_key, public_key = wgexec.generate_keypair()
        with open(conf_file, 'w') as file:
            file.write(f"[Interface]\n")
            file.write(f"Address = {SERVER_ADDRESS}\n" if server_ip is None else f"Address = {server_ip}\n")
            file.write(f"ListenPort = {SERVER_PORT}\n" if port is None else f"ListenPort = {port}\n")
            file.write(f"PrivateKey = {private_key}\n")
            if preup is not None:
                file.write(f"PreUp = {preup}\n") 
            file.write(f"PostUp = {POSTUP}\n" if postup is None else f"PostUp = {postup}\n")
            if predown is not None:
                file.write(f"PreDown = {predown}\n")
            file.write(f"PostDown = {POSTDOWN}\n" if postdown is None else f"PostDown = {postdown}\n")
        return get_wg_interface(name, location)
