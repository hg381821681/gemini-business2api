from typing import Callable, Optional

from core.config import config
from core.proxy_utils import extract_host, no_proxy_matches, parse_proxy_setting
from core.duckmail_client import DuckMailClient
from core.freemail_client import FreemailClient
from core.gptmail_client import GPTMailClient
from core.moemail_client import MoemailClient


def create_temp_mail_client(
    provider: str,
    *,
    domain: Optional[str] = None,
    proxy: Optional[str] = None,
    log_cb: Optional[Callable[[str, str], None]] = None,
):
    provider = (provider or "duckmail").lower()
    if proxy is None:
        proxy = config.basic.proxy_for_auth if config.basic.mail_proxy_enabled else ""
    proxy, no_proxy = parse_proxy_setting(proxy if config.basic.mail_proxy_enabled else "")
    if provider == "moemail":
        if no_proxy_matches(extract_host(config.basic.moemail_base_url), no_proxy):
            proxy = ""
        return MoemailClient(
            base_url=config.basic.moemail_base_url,
            proxy=proxy,
            api_key=config.basic.moemail_api_key,
            domain=domain or config.basic.moemail_domain,
            log_callback=log_cb,
        )
    if provider == "freemail":
        if no_proxy_matches(extract_host(config.basic.freemail_base_url), no_proxy):
            proxy = ""
        return FreemailClient(
            base_url=config.basic.freemail_base_url,
            jwt_token=config.basic.freemail_jwt_token,
            proxy=proxy,
            verify_ssl=config.basic.freemail_verify_ssl,
            log_callback=log_cb,
        )
    if provider == "gptmail":
        if no_proxy_matches(extract_host(config.basic.gptmail_base_url), no_proxy):
            proxy = ""
        return GPTMailClient(
            base_url=config.basic.gptmail_base_url,
            api_key=config.basic.gptmail_api_key,
            proxy=proxy,
            verify_ssl=config.basic.gptmail_verify_ssl,
            log_callback=log_cb,
        )

    if no_proxy_matches(extract_host(config.basic.duckmail_base_url), no_proxy):
        proxy = ""
    return DuckMailClient(
        base_url=config.basic.duckmail_base_url,
        proxy=proxy,
        verify_ssl=config.basic.duckmail_verify_ssl,
        api_key=config.basic.duckmail_api_key,
        log_callback=log_cb,
    )
