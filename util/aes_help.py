from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 华米传输加密使用的密钥 固定iv
# 参考自 https://github.com/hanximeng/Zepp_API/blob/main/index.php
HM_AES_KEY = b'xeNtBVqzDc6tuNTh'  # 16 bytes
HM_AES_IV = b'MAAAYAAAAAAAAABg'  # 16 bytes

AES_BLOCK_SIZE = AES.block_size  # 16


def _pkcs7_pad(data: bytes) -> bytes:
    pad_len = AES_BLOCK_SIZE - (len(data) % AES_BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len


def _pkcs7_unpad(data: bytes) -> bytes:
    if not data or len(data) % AES_BLOCK_SIZE != 0:
        raise ValueError(f"invalid padded data length {len(data)}")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES_BLOCK_SIZE:
        raise ValueError(f"invalid padding length: {pad_len}")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("invalid PKCS#7 padding")
    return data[:-pad_len]


def _validate_key(key: bytes):
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")
    if len(key) != 16:
        raise ValueError("key must be 16 bytes for AES-128")


def encrypt_data(plain: bytes, key: bytes, iv: bytes | None = None) -> bytes:
    """
    返回：IV（16B） + ciphertext（bytes） 或者仅ciphertext（当使用固定IV时）
    参数：
      - plain: 明文字节
      - key: 16 字节 AES-128 密钥
      - iv: IV向量，如果为None则生成随机IV
    """
    _validate_key(key)
    if not isinstance(plain, (bytes, bytearray)):
        raise TypeError("plain must be bytes")

    if iv is None:
        # 使用随机IV
        iv = get_random_bytes(AES_BLOCK_SIZE)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = _pkcs7_pad(plain)
        ciphertext = cipher.encrypt(padded)
        return iv + ciphertext
    else:
        # 使用固定IV
        if len(iv) != AES_BLOCK_SIZE:
            raise ValueError(f"IV must be {AES_BLOCK_SIZE} bytes")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = _pkcs7_pad(plain)
        ciphertext = cipher.encrypt(padded)
        return ciphertext


def decrypt_data(data: bytes, key: bytes, iv: bytes | None = None) -> bytes:
    """
    输入：IV（16B） + ciphertext 或者仅ciphertext（当使用固定IV时）
    返回：明文字节（未解码为字符串）
    """
    _validate_key(key)
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")

    if iv is None:
        # 从数据中提取IV（假设前16字节是IV）
        if len(data) < AES_BLOCK_SIZE:
            raise ValueError("data too short")

        iv = data[:AES_BLOCK_SIZE]
        ciphertext = data[AES_BLOCK_SIZE:]

        if len(ciphertext) == 0 or len(ciphertext) % AES_BLOCK_SIZE != 0:
            raise ValueError("invalid ciphertext length")
    else:
        # 使用提供的固定IV
        if len(iv) != AES_BLOCK_SIZE:
            raise ValueError(f"IV must be {AES_BLOCK_SIZE} bytes")
        ciphertext = data
        if len(ciphertext) == 0 or len(ciphertext) % AES_BLOCK_SIZE != 0:
            raise ValueError("invalid ciphertext length")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    return _pkcs7_unpad(decrypted_padded)
