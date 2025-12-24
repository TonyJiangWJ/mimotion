from util import aes_help

if __name__ == "__main__":
    """
    可以使用这个工具解密aes加密的base64内容
    修改encrypted_data的值和aes_key即可
    """
    encrypted_data = "ud1Ez02Cf5g4RrHFVLkfap/SJkMRfMdnsLRGaTqMacSDBd9YF3a/pHbSwTVgwyt/BfMlSxhyfqNeyzNt7pwEfg=="
    aes_key = b"1231231231234321"
    print("解密内容：", aes_help.decrypt_data(aes_help.base64_to_bytes(encrypted_data), aes_key).decode("utf-8"))
