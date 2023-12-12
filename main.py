from fastapi import FastAPI
from typing import List, Optional
from core.wireguard import models
from core.wireguard import get_wg, delete_wg, post_wg
from fastapi.responses import FileResponse, JSONResponse
from fastapi import HTTPException

app = FastAPI(
    title="Wireguard Rest API"
)

# GET


@app.get("/interfaces", response_model=List[models.Devices])
def get_interfaces():
    try:
        devices = get_wg.get_wg_interfaces()
        return devices
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/interface/{name}", response_model=models.Device)
def get_interface(
        name: str,
        location: Optional[str] = None
    ):
    try: 
        device = get_wg.get_wg_interface(name, location)
        return device
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/interface/{name}/peer")
def get_peer(
        name: str,
        public_key: str,
        location: Optional[str] = None
    ):
    try:
        peer = get_wg.get_wg_peer(name, public_key, location)
        return(peer)
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/interface/{name}/peers", response_model=models.Peers)
def get_peers(
        name: str,
        location: Optional[str] = None
    ):
    try:
        peers = get_wg.get_wg_peers(name, location)
        return {"peers": peers}
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/interface/{name}/peer/config")
def get_peer_config(
        name: str,
        public_key: str,
        location: Optional[str] = None
    ):
    try:
        config, qr = get_wg.get_wg_peer_config(name, public_key, location)
        return  FileResponse(config, filename="wgclient.conf", media_type="application/octet-stream")
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/interface/{name}/peer/quick")
def get_peer_qr(
        name: str,
        public_key: str,
        location: Optional[str] = None
    ):
    try:
        config, qr = get_wg.get_wg_peer_config(name, public_key, location)
        return  FileResponse(qr, filename="qr.png", media_type="application/octet-stream")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Not found")

# POST


@app.post("/interface/{name}/peer")
def create_peer(
        name: str,
        private_key: Optional[str] = None,
        presharedey: Optional[bool] = None,
        location: Optional[str] = None
    ):
    try:
        peer = post_wg.create_wg_peer(name, private_key, presharedey, location)
        return peer
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.post("/interface/{name}")
def create_interface(
        name: str,
        server_ip: Optional[str] = None,
        port: Optional[int] = None,
        preup: Optional[str] = None,
        postup: Optional[str] = None,
        predown: Optional[str] = None,
        postdown: Optional[str] = None,
        location: Optional[str] = None
    ):
    try:
        device = post_wg.create_wg_interface(name, server_ip, port, preup, postup, predown, postdown, location)
        if device is not None:
            return device
        else:
            return JSONResponse(content={"detail": "Item already exist"}, status_code=409)
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")

# PATCH

# DELETE


@app.delete("/interface/{name}")
def del_interface(
        name: str,
        location: Optional[str] = None
    ):
    try: 
        return delete_wg.del_wg_interface(name, location)
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")


@app.delete("/interface/{name}/peer")
def del_peer(
        name: str,
        public_key: str,
        location: Optional[str] = None
    ):
    try:
        return delete_wg.del_wg_peer(name, public_key, location)
    except Exception as Error:
        print(Error)
        raise HTTPException(status_code=404, detail="Not found")
