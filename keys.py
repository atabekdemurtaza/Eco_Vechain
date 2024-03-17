from thor_devkit import cry
from thor_devkit.cry import secp256k1

private_key = secp256k1.generate_privateKey()

public_key = secp256k1.derive_publicKey(private_key)

_address_bytes = cry.public_key_to_address(public_key)
address = '0x' + _address_bytes.hex()

print(address)

print('is address?', cry.is_address(address))

print( cry.to_checksum_address(address) ) 