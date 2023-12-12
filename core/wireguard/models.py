from pydantic import BaseModel
from typing import Optional


class Devices(BaseModel):
    device: str
    location: Optional[str] = None
    public_key: str
    listen_port: int


class Device(BaseModel):
    public_key: str
    listen_port: int
    address: str
    preup: Optional[str] = None
    postup: Optional[str] = None
    predown: Optional[str] = None
    postdown: Optional[str] = None
    num_peers: int


class Peer(BaseModel):
    PublicKey: str
    PresharedKey: Optional[str] = None
    AllowedIPs: str


class Peers(BaseModel):
    peers: dict[str, Peer]
