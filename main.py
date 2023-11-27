from fastapi import FastAPI
from typing import List
from core.wireguard import models
from core.wireguard import wg


app = FastAPI(
    title="Test"
)

# GET


@app.get("/interfaces", response_model=List[models.Devices])
def get_interfaces():
    devices = wg.get_wg_interfaces()
    return devices


@app.get("/interface/{name}", response_model=models.Device)
def get_interface(name: str):
    device = wg.get_wg_interface(name)
    return device


@app.get("/interface/{name}/peers", response_model=models.Peers)
def get_peers(name: str):
    peers = wg.get_wg_peers(name)
    return {"peers": peers}

# POST

# PATCH

# DELETE


@app.delete("/interface/{name}")
def del_interface(name: str):
    return wg.del_wg_interface(name)
