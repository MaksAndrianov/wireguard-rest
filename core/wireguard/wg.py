import os
import wgconfig
import qrcode
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


def genetate_qr(conf_path, path):
    with open(conf_path, "rb") as file:
        data = file.read()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{path}/qr.png")
    
    return f"{path}/qr.png"