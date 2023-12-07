import os
import ipaddress
import requests
import wgconfig
import wgconfig.wgexec as wgexec
from dotenv import load_dotenv


from core.wireguard.get_wg import get_wg_peers


load_dotenv()
path = os.environ.get("CONFIG_PATH")
client_config_path = os.environ.get("CLIENT_CONFIG_PATH")
DNS = os.environ.get("DNS")
SERVER_IP = os.environ.get("SERVER_IP")


if SERVER_IP is None:
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    SERVER_IP = data.get('ip')


def create_wg_peer(interface: str, private_key: str, presharedkey: bool):
    conf_file = f"{path}/{interface}.conf"
    wc = wgconfig.WGConfig(conf_file)
    wc.read_file()

    server = wc.get_interface()

    if private_key is None:
        private_key, public_key = wgexec.generate_keypair()
    else: 
        public_key = wgexec.get_publickey(private_key)

    client_directory = public_key.replace('/', '%2F')
    get_peer = get_wg_peers(interface)
    test=get_peer[public_key] if public_key in get_peer else None,

    if os.path.exists(f"{client_config_path}/{client_directory}") or test[0] is not None:
        return 404
    else:    
        os.makedirs(f"{client_config_path}/{client_directory}")

        wc.add_peer(public_key)

        # IP 
        possible_ips = set(ipaddress.IPv4Network(item.get("AllowedIPs")) for item in get_peer.values() if "AllowedIPs" in item)
        all_possible_ips = set(ipaddress.IPv4Network(f"10.0.0.{i}/32") for i in range(2, 254))
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
                f'Endpoint = {SERVER_IP}:{server["ListenPort"]}\n'
                f'PersistentKeepalive = 10\n'
                f'{f"PresharedKey = {key} \n" if presharedkey else ""}'
            )
        
    return f'{client_config_path}/{client_directory}/wgclient.conf', "wgclient.conf"
 