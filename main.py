from fastapi import FastAPI
from typing import List
from core.wireguard import models
from core.wireguard import get_wg, delete_wg


app = FastAPI(
    title="Test"
)

# GET


@app.get("/interfaces", response_model=List[models.Devices])
def get_interfaces():
    devices = get_wg.get_wg_interfaces()
    return devices


@app.get("/interface/{name}", response_model=models.Device)
def get_interface(name: str):
    device = get_wg.get_wg_interface(name)
    return device


@app.get("/interface/{name}/peers", response_model=models.Peers)
def get_peers(name: str):
    peers = get_wg.get_wg_peers(name)
    return {"peers": peers}

# POST

# PATCH

# DELETE


@app.delete("/interface/{name}")
def del_interface(name: str):
    return delete_wg.del_wg_interface(name)


@app.delete("/interface/{name}/peer")
def del_peer(name: str, public_key: str):
    return delete_wg.del_wg_peer(name, public_key)
