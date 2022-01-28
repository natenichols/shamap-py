from hashlib import sha512 

def sha512Half(bytes):
    h = sha512()

    h.update(bytearray.fromhex(bytes))
    hash = h.hexdigest().upper()
    return hash[0:64]

def hashTx(tx_blob):
    prefix = '54584E00'
    return sha512Half(prefix + tx_blob)


def nibblet(hash, depth):
    b = int(hash[depth], base=16)
    return b

def bytesToHex(bytes):
    h = []
    for num in bytes:
        hexVal = hex(num).lstrip("0x")
        if len(hexVal) == 1: 
            hexVal = '0' + hexVal
        h.append(hexVal)
    
    return ''.join(h).upper()


def addLengthPrefix(hex): 
    length = len(hex) // 2
    if length <= 192:
        return bytesToHex([int(length)]) + hex
  
    if (length <= 12480):
        prefix = length - 193
        return bytesToHex([int(193 + (prefix >> 8)), int(prefix & int('ff', base=16))]) + hex
  
    if (length <= 918744):
        prefix = length - 12481
        return bytesToHex([int(241 + (prefix >> 16)), int((prefix >> 8) & int('ff', base=16)), int(prefix & int('ff', base=16))]) + hex

    raise 'Variable integer overflow.'

zero256 = ''.zfill(64)

innerPrefix = '4D494E00'