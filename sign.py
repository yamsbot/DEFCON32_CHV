#!/usr/bin/env python3
import hashlib, os
from tuf.api.metadata import Metadata, Timestamp, MetaFile, Snapshot, Targets, TargetFile
from securesystemslib.signer import CryptoSigner, Signer
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta

with open("keys/private.pem", "rb") as f:
    pkey = load_pem_private_key(f.read(), None)

signer = CryptoSigner(pkey)
pubkey = signer.public_key
exp = datetime.now() + timedelta(days=1)
keyid = b"f1f66ca394996ea67ac7855f484d9871c8fd74e687ebab826dbaedf3b9296d14"
bad_keyid = b"70a11ababc3a62c640e59f5d3d5107e95dd811307294fecd7cf86bea8354747a" 

def hasher(fn):
    with open(fn, "rb") as f:
        data = f.read()
    f.close()
    h = hashlib.new("sha512")
    h.update(data)
    return h.hexdigest()

def keyid_replace(fn):
    with open(fn, "rb") as f:
        data = f.read()
    f.close()
    
    data = data.replace(bad_keyid, keyid)
    
    with open(fn, "wb") as f:
        f.write(data)
    f.close()

# build targets.json
def sign_all():
    tname = "2.targets.json"
    target = Metadata(Targets(version=2, spec_version="1.0", expires=exp, targets={"tcmupdate_v0.2.0.py":TargetFile(length=79, hashes={"sha512":"870cba60f57b8cbee2647241760d9a89f3c91dba2664467694d7f7e4e6ffaca588f8453302f196228b426df44c01524d5c5adeb2f82c37f51bb8c38e9b0cc900"}, path="targets")} ))
    target.sign(signer)
    target.to_file(tname)
    keyid_replace(tname)
    target_hash = hasher(tname)
    target_size = os.path.getsize(tname)

    # build snapshot.json
    sname = "4.snapshot.json"
    snapshot = Metadata(Snapshot(version=4, spec_version="1.0", expires=exp, meta={"targets.json":MetaFile(version=2, length=target_size, hashes={"sha512":target_hash})} ))
    signed_snapshot = Metadata.to_bytes(snapshot.signed)
    snapshot.sign(signer)
    snapshot.to_file(sname)
    keyid_replace(sname)
    snapshot_hash = hasher(sname)
    snapshot_size = os.path.getsize(sname)

    # build timestamp.json
    timestamp = Metadata(Timestamp(version=4, spec_version="1.0", expires=exp, snapshot_meta=MetaFile(version=4, length=snapshot_size, hashes={"sha512":snapshot_hash} )))
    timestamp.sign(signer)
    timestamp.to_file("timestamp.json")
    keyid_replace("timestamp.json")
