from thor_devkit import cry
from thor_devkit.cry import secp256k1

# bytes
private_key = bytes.fromhex('7582be841ca040aa940fff6c05773129e135623e41acce3e0b8ba520dc1ae26a')
# bytes
msg_hash, _ = cry.keccak256([b'hello world'])

signature = secp256k1.sign(msg_hash, private_key)

public_key = secp256k1.recover(msg_hash, signature)

print(signature)

print(public_key)
