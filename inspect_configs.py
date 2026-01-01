# -*- coding: utf8 -*-
import os

from util import push_util
from util import aes_help


def build_inspect_configs_content(config_param, aes_key_param, pat_param):
    if aes_key_param is None or aes_key_param == "":
        aes_content = "未配置AES_KEY"
    else:
        aes_content = f"```\n{aes_key_param}\n```"

    if pat_param is None or pat_param == "":
        pat_content = "未配置PAT"
    else:
        pat_content = f"```\n{pat_param}\n```"
    config_content = f"```json\n{config_param}\n```"
    return f"""## CONFIG:\n{config_content}\n\n## PAT:\n{pat_content}\n\n## AES_KEY:\n{aes_content}"""


def build_inspect_configs_content_for_telegram(config_param, aes_key_param, pat_param):
    if aes_key_param is None or aes_key_param == "":
        aes_content = "<blockquote>未配置AES_KEY</blockquote>\n"
    else:
        aes_content = f"<b>AES_KEY:</b>\n<pre>{aes_key_param}</pre>\n"

    if pat_param is None or pat_param == "":
        pat_content = "<blockquote>未配置PAT</blockquote>\n"
    else:
        pat_content = f"<b>PAT:</b>\n<pre>{pat_param}</pre>\n"
    config_content = f"<b>CONFIG:</b>\n<pre>{config_param}</pre>"
    return f"{aes_content}{pat_content}{config_content}"


def display_content_by_aes(inspect_aes_key, config, aes_key, pat):
    """
    使用AES_KEY进行加密，然后推送到微信
    """
    if config is not None:
        display_encrypted_info("CONFIG", config, inspect_aes_key)
    else:
        print("未配置CONFIG")
    if pat is not None:
        display_encrypted_info("PAT", pat, inspect_aes_key)
    else:
        print("未配置PAT")
    if aes_key is not None:
        display_encrypted_info("AES_KEY", aes_key, inspect_aes_key)
    else:
        print("未配置AES_KEY")
    print(
        "请复制对应的base64值，使用在线base64网站解密提取，或者使用其他通用的aes工具解密，加密方式为CBC，key和iv为你在secrets中所配置的INSPECT_AES_KEY")


def display_encrypted_info(desc, content, key):
    encrypted_content = aes_help.bytes_to_base64(aes_help.encrypt_data(content.encode("utf-8"), key, key))
    print(f"{desc}: {encrypted_content}")


if __name__ == "__main__":
    """
    从环境变量中提取配置信息，加密打印和明文推送微信企业通知
    仅支持微信推送，因为pushplus本质上并不安全
    """
    config = os.environ.get("CONFIG")
    aes_key = os.environ.get("AES_KEY")
    pat = os.environ.get("PAT")
    # 直接打印
    aes_inspect_key = os.environ.get("INSPECT_AES_KEY")
    if aes_inspect_key is not None and aes_inspect_key != "":
        aes_inspect_key = aes_inspect_key.encode('utf-8')
        if len(aes_inspect_key) == 16:
            display_content_by_aes(aes_inspect_key, config, aes_key, pat)
        else:
            print("INSPECT_AES_KEY 长度必须为16位")
    else:
        print("未配置 INSPECT_AES_KEY 跳过配置信息打印")

    # 推送到微信
    wechat_push_key = os.environ.get("INSPECT_WECHAT_HOOK_KEY")
    if wechat_push_key is None or wechat_push_key == "":
        print("未配置 INSPECT_WECHAT_HOOK_KEY 无法推送配置信息")
    else:
        push_util.push_wechat_webhook(wechat_push_key, "提取配置信息",
                                      build_inspect_configs_content(config, aes_key, pat))

    # 推送到telegram
    telegram_bot_token = os.environ.get("INSPECT_TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("INSPECT_TELEGRAM_CHAT_ID")
    if telegram_bot_token is None or telegram_bot_token == "" or telegram_chat_id is None or telegram_chat_id == "":
        print("未配置 INSPECT_TELEGRAM_BOT_TOKEN 或 INSPECT_TELEGRAM_CHAT_ID 跳过telegram推送")
    else:
        push_util.push_telegram_bot(telegram_bot_token, telegram_chat_id,
                                    build_inspect_configs_content_for_telegram(config, aes_key, pat))
