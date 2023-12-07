from fastapi import FastAPI
from typing import List, Optional
from core.wireguard import models
from core.wireguard import get_wg, delete_wg, post_wg
from fastapi.responses import FileResponse

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


@app.post("/interface/{name}/peer")
def create_peer(name: str, private_key: Optional[str] = None, presharedey: Optional[bool] = None ):
    file, filename = post_wg.create_wg_peer(name, private_key, presharedey)
    return FileResponse(file, filename=filename, media_type="application/octet-stream")

# PATCH

# DELETE


@app.delete("/interface/{name}")
def del_interface(name: str):
    return delete_wg.del_wg_interface(name)


@app.delete("/interface/{name}/peer")
def del_peer(name: str, public_key: str):
    return delete_wg.del_wg_peer(name, public_key)
